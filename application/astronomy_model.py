from PyQt5 import QtCore, QtWidgets, uic
import astronomy


class AstronomyModel(QtCore.QAbstractTableModel):
    def __init__(self, session, type, *args, **kwargs):
        super(AstronomyModel, self).__init__(*args, **kwargs)
        self.session = session
        self.type = type
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
            if field is not None:
                return str(field)
            else:
                return ''

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.header[section]
            elif orientation == QtCore.Qt.Vertical:
                return str(section + 1)
    
    def to_row(self, entity):
        raise NotImplementedError('Model should define conversion to row')

    def add_row(self, parent_window):
        dialog = QtWidgets.QDialog(parent_window)
        uic.loadUi('gui/' + self.form, dialog)
        dialog.open()
        print('Inserting data')

    def removeRow(self, position, parent=QtCore.QModelIndex()):
        print('Removing data')


class AstronomerModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(AstronomerModel, self).__init__(session, astronomy.Astronomer, *args, **kwargs)

    form = 'form-astronomer.ui'
    header = ('Pełne imię', 'Kraj', 'Data urodzenia', 'Data śmierci', 'Nazwa w MPC')
    def to_row(self, astronomer):
        return (astronomer.full_name, astronomer.country, astronomer.birth_date,
            astronomer.death_date, astronomer.name_mpc)

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
