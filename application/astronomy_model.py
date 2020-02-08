from PyQt5 import QtCore
from utils import to_text
import astronomy


class AstronomyModel(QtCore.QAbstractTableModel):
    def __init__(self, session, type, *args, **kwargs):
        super(AstronomyModel, self).__init__(*args, **kwargs)
        self.session = session
        self.type = type
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
            return len(self.header)

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

    def add_row(self, entity):
        try:
            self.session.add(entity)
            self.session.commit()

            row_count = self.rowCount(QtCore.QModelIndex())
            self.beginInsertRows(QtCore.QModelIndex(), row_count, row_count)
            self.fetch_items()
            self.endInsertRows()
        except:
            self.session.rollback()
            raise

    def edit_row(self, position):
        try:
            self.session.commit()
            self.fetch_items()
        except:
            self.session.rollback()
            raise

    def remove_row(self, position):
        try:
            self.session.delete(self.rows[position])
            self.session.commit()
            self.beginRemoveRows(QtCore.QModelIndex(), position, position)
            self.fetch_items()
            self.endRemoveRows()
        except:
            self.session.rollback()
            raise


class AstronomerModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(AstronomerModel, self).__init__(session, astronomy.Astronomer, *args, **kwargs)

    header = ('Pełne imię', 'Kraj', 'Data urodzenia', 'Data śmierci', 'Nazwa w MPC')
    def to_row(self, astronomer):
        return (astronomer.full_name, astronomer.country, astronomer.birth_date,
            astronomer.death_date, astronomer.name_mpc)


class ObservatoryModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(ObservatoryModel, self).__init__(session, astronomy.Observatory, *args, **kwargs)

    header = ('Pełna nazwa', 'Nazwa w MPC', 'Kod IAU', 'Kraj', 
        'Szerokość geograficzna', 'Długość geograficzna')
    def to_row(self, observatory):
        return (observatory.full_name, observatory.name_mpc, observatory.iau_code,
            observatory.country, observatory.latitude, observatory.longitude)


class ConstellationModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(ConstellationModel, self).__init__(session, astronomy.Constellation, *args, **kwargs)

    header = ('Nazwa', 'Skrót IAU', 'Najjaśniejsza gwiazda')
    def to_row(self, constellation):
        return (constellation.name, constellation.iau_abbreviation, constellation.brightest_star)


class GalaxyGroupModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(GalaxyGroupModel, self).__init__(session, astronomy.GalaxyGroup, *args, **kwargs)

    header = ('Nazwa', 'Rektasencja', 'Deklinacja', 'Dystans', 'Prędkość radialna')
    def to_row(self, object):
        return (object.name, object.right_ascension, object.declination,
            object.distance, object.radial_velocity)


class GalaxyModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(GalaxyModel, self).__init__(session, astronomy.Galaxy, *args, **kwargs)

    header = ('Nazwa', 'Typ', 'Rektasencja', 'Deklinacja', 'Wielkość obserwowana', 'Wielkość absolutna',
        'Dystans', 'Średnica', 'Konstelacja', 'Orbitowana galaktyka', 'Grupa galaktyk')
    def to_row(self, object):
        return (object.name, object.galaxy_type, object.right_ascension, object.declination, 
            object.apparent_magnitude, object.absolute_magnitude, object.distance, 
            object.diameter, object.constellation, object.orbited_galaxy, object.galaxy_group)


class StarModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(StarModel, self).__init__(session, astronomy.Star, *args, **kwargs)

    header = ('Nazwa', 'Typ widmowy', 'Rektasencja', 'Deklinacja', 'Wielkość obserwowana', 
        'Wielkość absolutna', 'Dystans', 'Paralaksa', 'Masa', 'Promień', 'Konstelacja', 'Galaktyka')
    def to_row(self, object):
        return (object.name, object.spectral_type, object.right_ascension, object.declination,
            object.apparent_magnitude, object.absolute_magnitude, object.distance, object.parallax,
            object.mass, object.radius, object.constellation, object.galaxy)


class SmallBodyModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(SmallBodyModel, self).__init__(session, astronomy.SmallBody, *args, **kwargs)

    header = ('Nazwa', 'Typ', 'Średnica', 'Masa', 'Temperatura', 'Okres orbitalny',
        'Ekscentryczność', 'Półoś wielka', 'Inklinacja', 'Orbitowane ciało')
    def to_row(self, object):
        if object.orbited_star is not None:
            orbited_body = object.orbited_star 
        else:
            orbited_body = object.orbited_small_body
        return (object.name, object.type, object.diameter, object.mass, object.temperature, 
            object.period, object.eccentricity, object.semi_major_axis, object.inclination, orbited_body)


class SatelliteModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(SatelliteModel, self).__init__(session, astronomy.Satellite, *args, **kwargs)

    header = ('Nazwa', 'Rodzaj', 'Kraj', 'Data startu', 'Data zniszczenia', 'Okres orbitalny', 
        'Apocentrum', 'Perycentrum', 'Inklinacja', 'Orbitowane ciało')
    def to_row(self, object):
        if object.orbited_star is not None:
            orbited_body = object.orbited_star 
        else:
            orbited_body = object.orbited_small_body
        return (object.name, object.type, object.country, object.start_date, object.end_date,
            object.period, object.apoapsis, object.periapsis, object.inclination, orbited_body)


class MeteorShowerModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(MeteorShowerModel, self).__init__(session, astronomy.MeteorShower, *args, **kwargs)

    header = ('Nazwa', 'Data początku', 'Data końca', 'Data maksimum', 'Rektasencja', 'Deklinacja',
        'Prędkość', 'ZHR', 'Aktywność')
    def to_row(self, object):
        return (object.name, object.begin_date.strftime('%d.%m'), object.end_date.strftime('%d.%m'), 
            object.peak_date.strftime('%d.%m'), object.right_ascension, object.declination, 
            object.velocity, object.zhr, object.activity)


class CatalogueModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(CatalogueModel, self).__init__(session, astronomy.Catalogue, *args, **kwargs)

    header = ('Nazwa', 'Skrót', 'Rok wydania')
    def to_row(self, catalogue):
        return (catalogue.name, catalogue.abbreviation, catalogue.publishing_year)


class ObservationModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(ObservationModel, self).__init__(session, astronomy.Observation, *args, **kwargs)

    header = ('Obiekt', 'Astronom', 'Obserwatorium', 'Data', 'Czy odkrycie')
    def to_row(self, observation):
        return (observation.astronomical_object, observation.astronomer, observation.observatory,
            observation.date, observation.is_discovery)
