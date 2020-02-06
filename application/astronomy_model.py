import datetime
from PyQt5 import QtCore, QtWidgets, uic
from sqlalchemy.orm.exc import FlushError
from sqlalchemy.exc import DataError, DatabaseError
import astronomy


def from_text(text):
    if text == '':
        return None
    return text

def to_text(value):
    if value is None:
        return ''
    if isinstance(value, datetime.date):
        return value.strftime('%d.%m.%Y')
    return str(value)

def text_to_date(text):
    if text == '':
        return None
    return datetime.datetime.strptime(text, '%d.%m.%Y').date()

def get_error_message(code, message):
    if code == 1048: # ER_BAD_NULL_ERROR
        column = message.split("'")[1]
        return 'Kolumna ' + column + ' nie może być pusta'
    elif code == 1364: # ER_NO_DEFAULT_FOR_FIELD
        column = message.split("'")[1]
        return 'Kolumna ' + column + ' nie może być pusta'
    else:
        return message


class AstronomyModel(QtCore.QAbstractTableModel):
    def __init__(self, session, type, *args, **kwargs):
        super(AstronomyModel, self).__init__(*args, **kwargs)
        self.session = session
        self.type = type
        self.edited_entity = None
        self.dialog = None
        self.fetch_items()

    def fetch_items(self):
        self.query = self.session.query(self.type)
        self.rows = self.query.all()

    def rowCount(self, parent):
        return len(self.rows)

    def columnCount(self, parent):
        if len(self.rows) > 0:
            return len(self.to_row(self.rows[0]))
        else:
            return 0

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            entity = self.rows[index.row()]
            field = self.to_row(entity)[index.column()]
            return to_text(field)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.header[section]
            elif orientation == QtCore.Qt.Vertical:
                return str(section + 1)
    
    def to_row(self, entity):
        raise NotImplementedError('Model should define conversion to row')

    def add_row(self, parent_window):
        self.dialog = QtWidgets.QDialog(parent_window)
        uic.loadUi('gui/' + self.form, self.dialog)
        self.dialog.button_box.accepted.connect(self.on_accepted)
        self.dialog.open()

    def edit_row(self, position, parent_window):
        self.dialog = QtWidgets.QDialog(parent_window)
        uic.loadUi('gui/' + self.form, self.dialog)
        self.edited_entity = self.rows[position]
        self.fill_form(self.edited_entity)
        self.dialog.button_box.accepted.connect(self.on_accepted)
        self.dialog.open()
    
    def on_accepted(self):
        try:
            if self.edited_entity is not None:
                self.on_edit_accepted()
            else:
                self.on_add_accepted()
        except ValueError as error:
            self.session.rollback()
            print(error)
            self.dialog.error_label.setText('Data powinna być w formacie dd.mm.yyyy')
        except FlushError as error:
            self.session.rollback()
            print(error)
            self.dialog.error_label.setText('Obiekt o tej samej nazwie już jest w bazie danych')
        except (DataError, DatabaseError) as error:
            self.session.rollback()
            print(error)
            self.dialog.error_label.setText(get_error_message(error.orig.args[0], error.orig.args[1]))
    
    def on_add_accepted(self):
        entity = self.type()
        self.set_object_from_form(entity)
        self.session.add(entity)
        self.session.commit()

        row_count = self.rowCount(QtCore.QModelIndex())
        self.beginInsertRows(QtCore.QModelIndex(), row_count, row_count)
        self.fetch_items()
        self.endInsertRows()
        self.dialog.accept()

    def on_edit_accepted(self):
        self.set_object_from_form(self.edited_entity)
        self.session.commit()
        self.fetch_items()
        self.dialog.accept()
        self.edited_entity = None

    def remove_row(self, position):
        try:
            self.session.delete(self.rows[position])
            self.session.commit()
            self.beginRemoveRows(QtCore.QModelIndex(), position, position)
            self.fetch_items()
            self.endRemoveRows()
        except (FlushError, DataError, DatabaseError) as error:
            self.session.rollback()
            print(error)


class AstronomerModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(AstronomerModel, self).__init__(session, astronomy.Astronomer, *args, **kwargs)

    form = 'form-astronomer.ui'
    header = ('Pełne imię', 'Kraj', 'Data urodzenia', 'Data śmierci', 'Nazwa w MPC')
    def to_row(self, astronomer):
        return (astronomer.full_name, astronomer.country, astronomer.birth_date,
            astronomer.death_date, astronomer.name_mpc)

    def set_object_from_form(self, entity):
        entity.full_name = from_text(self.dialog.full_name_edit.text())
        entity.country = from_text(self.dialog.country_edit.text())
        entity.birth_date = text_to_date(self.dialog.birth_date_edit.text())
        entity.death_date = text_to_date(self.dialog.death_date_edit.text())
        entity.name_mpc = from_text(self.dialog.name_mpc_edit.text())
    
    def fill_form(self, entity):
        self.dialog.full_name_edit.setText(entity.full_name)
        self.dialog.country_edit.setText(entity.country)
        self.dialog.birth_date_edit.setText(to_text(entity.birth_date))
        self.dialog.death_date_edit.setText(to_text(entity.death_date))
        self.dialog.name_mpc_edit.setText(entity.name_mpc)


class ObservatoryModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(ObservatoryModel, self).__init__(session, astronomy.Observatory, *args, **kwargs)

    form = 'form-observatory.ui'
    header = ('Pełna nazwa', 'Nazwa w MPC', 'Kod IAU', 'Kraj', 
        'Szerokość geograficzna', 'Długość geograficzna')
    def to_row(self, observatory):
        return [observatory.full_name, observatory.name_mpc, observatory.iau_code,
            observatory.country, observatory.latitude, observatory.longitude]


class ConstellationModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(ConstellationModel, self).__init__(session, astronomy.Constellation, *args, **kwargs)

    form = 'form-constellation.ui'
    header = ('Nazwa', 'Skrót IAU', 'Najjaśniejsza gwiazda')
    def to_row(self, constellation):
        return [constellation.name, constellation.iau_abbreviation, constellation.brightest_star]

    def set_object_from_form(self, entity):
        entity.iau_abbreviation = from_text(self.dialog.iau_abbreviation_edit.text())
        entity.name = from_text(self.dialog.name_edit.text())
        entity.brightest_star = from_text(self.dialog.brightest_star_edit.text())
    
    def fill_form(self, entity):
        self.dialog.iau_abbreviation_edit.setText(entity.iau_abbreviation)
        self.dialog.name_edit.setText(entity.name)
        self.dialog.brightest_star_edit.setText(entity.brightest_star)


class GalaxyGroupModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(GalaxyGroupModel, self).__init__(session, astronomy.AstronomicalObject, *args, **kwargs)

    form = 'form-galaxy-group.ui'
    header = ('Nazwa', 'Rektasencja', 'Deklinacja', 'Dystans', 'Prędkość kątowa')
    def to_row(self, small_body):
        return [small_body.name, small_body.name]

class GalaxyModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(GalaxyModel, self).__init__(session, astronomy.AstronomicalObject, *args, **kwargs)

    header = ('Nazwa', 'Typ', 'Dystans', 'Wielkość gwiazdowa (obserwowalna)', 'Wielkość gwiazdowa (absolutna)',
        'Średnica', 'Konstelacja', 'Orbitowana galaktyka', 'Grupa galaktyk')
    def to_row(self, small_body):
        return [small_body.name, small_body.name]

class StarModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(StarModel, self).__init__(session, astronomy.AstronomicalObject, *args, **kwargs)

    header = ('Nazwa', 'Typ widmowy', 'Rektasencja', 'Deklinacja', 'Wielkość gwiazdowa (obserwowalna)', 
        'Wielkość gwiazdowa (absolutna)', 'Paralaksa', 'Dystans', 'Masa', 'Promień', 'Galaktyka', 'Konstelacja')
    def to_row(self, small_body):
        return [small_body.name, small_body.name]

class SmallBodyModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(SmallBodyModel, self).__init__(session, astronomy.AstronomicalObject, *args, **kwargs)

    header = ('Nazwa', 'Typ', 'Średnica', 'Masa', 'Średnia temperatura', 'Okres orbitalny', 'Ekscentryczność'
        'Półoś wielka', 'Inklinacja', 'Długość węzła wstępującego', 'Argument perycentrum',
        'Anomalia średnia', 'Epoka', 'Orbituje')
    def to_row(self, small_body):
        return [small_body.name, small_body.name]

class SatelliteModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(SatelliteModel, self).__init__(session, astronomy.AstronomicalObject, *args, **kwargs)

    header = ('Nazwa', 'Rodzaj', 'Kraj', 'Data startu', 'Data zniszczenia', 'Okres orbitalny', 'Apocentrum', 
        'Perycentrum', 'Inklinacja', 'Orbituje')
    def to_row(self, small_body):
        return [small_body.name, small_body.name]

class MeteorShowerModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(MeteorShowerModel, self).__init__(session, astronomy.AstronomicalObject, *args, **kwargs)

    header = ('Nazwa', 'Data początku', 'Data końca', 'Data maksimum', 'Rektasencja', 'Deklinacja',
        'Prędkość', 'ZHR', 'Aktywność')
    def to_row(self, small_body):
        return [small_body.name, small_body.name]

class CatalogueModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(CatalogueModel, self).__init__(session, astronomy.Catalogue, *args, **kwargs)

    header = ('Nazwa', 'Skrót', 'Rok wydania')
    def to_row(self, catalogue):
        return [catalogue.name, catalogue.abbreviation, catalogue.publishing_year]

class ObservationModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(ObservationModel, self).__init__(session, astronomy.Observation, *args, **kwargs)

    header = ('Obiekt', 'Astronom', 'Obserwatorium', 'Data', 'Czy odkrycie')
    def to_row(self, observation):
        return [observation.astronomical_object, observation.astronomer, observation.observatory,
            observation.date, observation.is_discovery]
