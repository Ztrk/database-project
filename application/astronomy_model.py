from PyQt5 import QtCore
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

class AstronomerModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(AstronomerModel, self).__init__(session, astronomy.Astronomer, *args, **kwargs)

    header = ('Pełne imię', 'Kraj', 'Data urodzenia', 'Data śmierci', 'Nazwa w mpc')
    def to_row(self, astronomer):
        return (astronomer.full_name, astronomer.country, astronomer.birth_date,
            astronomer.death_date, astronomer.name_mpc)



class ObservatoryModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(ObservatoryModel, self).__init__(session, astronomy.Observatory, *args, **kwargs)

    header = ('Pełna nazwa', 'Nazwa w MPC', 'Kod IAU', 'Kraj', 
        'Szerokość geograficzna', 'Długość geograficzna')
    def to_row(self, observatory):
        return [observatory.full_name, observatory.name_mpc, observatory.iau_code,
            observatory.country, observatory.latitude, observatory.longitude]


class ConstellationModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(ConstellationModel, self).__init__(session, astronomy.Constellation, *args, **kwargs)

    header = ('Nazwa', 'Skrót IAU', 'Najjaśniejsza gwiazda')
    def to_row(self, constellation):
        return [constellation.name, constellation.iau_abbreviation, constellation.brightest_star]

class SmallBodyModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(SmallBodyModel, self).__init__(session, astronomy.AstronomicalObject, *args, **kwargs)

    header = ('Nazwa', 'Nazwa')
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
