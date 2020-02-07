import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Astronomer(Base):
    __tablename__ = 'astronom'

    full_name = db.Column('pelne_imie', db.String, primary_key=True)
    birth_date = db.Column('data_urodzenia', db.Date)
    death_date = db.Column('data_zgonu', db.Date)
    country = db.Column('kraj', db.String)
    name_mpc = db.Column('imie_mpc', db.String)


class Observatory(Base):
    __tablename__ = 'obserwatorium'

    iau_code = db.Column('kod_iau', db.String, primary_key=True)
    latitude = db.Column('szerokosc_geograficzna', db.Numeric)
    longitude = db.Column('dlugosc_geograficzna', db.Numeric)
    country = db.Column('kraj', db.String)
    full_name = db.Column('pelna_nazwa', db.String)
    name_mpc = db.Column('nazwa_mpc', db.String)


class Constellation(Base):
    __tablename__ = 'konstelacja'

    iau_abbreviation = db.Column('skrot_iau', db.String, primary_key=True)
    name = db.Column('nazwa', db.String)
    brightest_star = db.Column('najjasniejsza_gwiazda', db.String)


class AstronomicalObject(Base):
    __tablename__ = 'obiekt_astronomiczny'

    name = db.Column('nazwa', db.String, primary_key=True)


class GalaxyGroup(AstronomicalObject):
    __tablename__ = 'grupa_galaktyk'

    name = db.Column('nazwa', db.String, db.ForeignKey('obiekt_astronomiczny.nazwa'), primary_key=True)
    right_ascension = db.Column('rektasencja', db.Numeric)
    declination = db.Column('deklinacja', db.Numeric)
    distance = db.Column('dystans', db.Numeric)
    radial_velocity = db.Column('predkosc_radialna', db.Numeric)


class Galaxy(AstronomicalObject):
    __tablename__ = 'galaktyka'

    name = db.Column('nazwa', db.String, db.ForeignKey('obiekt_astronomiczny.nazwa'), primary_key=True)
    galaxy_type = db.Column('typ', db.String)
    right_ascension = db.Column('rektasencja', db.Numeric)
    declination = db.Column('deklinacja', db.Numeric)
    apparent_magnitude = db.Column('wielkosc_obserwowana', db.Numeric)
    absolute_magnitude = db.Column('wielkosc_absolutna', db.Numeric)
    distance = db.Column('dystans', db.Numeric)
    diameter = db.Column('srednica', db.Numeric)
    galaxy_group = db.Column('grupa_galaktyk', db.String)
    orbited_galaxy = db.Column('orbitowana_galaktyka', db.String)
    constellation = db.Column('konstelacja', db.String)


class Star(AstronomicalObject):
    __tablename__ = 'gwiazda'

    name = db.Column('nazwa', db.String, db.ForeignKey('obiekt_astronomiczny.nazwa'), primary_key=True)
    spectral_type = db.Column('typ_widmowy', db.String)
    right_ascension = db.Column('rektasencja', db.Numeric)
    declination = db.Column('deklinacja', db.Numeric)
    apparent_magnitude = db.Column('wielkosc_obserwowana', db.Numeric)
    absolute_magnitude = db.Column('wielkosc_absolutna', db.Numeric)
    distance = db.Column('dystans', db.Numeric)
    parallax = db.Column('paralaksa', db.Numeric)
    mass = db.Column('masa', db.Numeric)
    radius = db.Column('promien', db.Numeric)
    galaxy = db.Column('galaktyka', db.String)
    constellation = db.Column('konstelacja', db.String)


class SmallBody:
    pass


class Satellite:
    pass


class MeteorShower(AstronomicalObject):
    __tablename__ = 'roj_meteorow'

    name = db.Column('nazwa', db.String, db.ForeignKey('obiekt_astronomiczny.nazwa'), primary_key=True)
    begin_date = db.Column('data_poczatku', db.Date)
    end_date = db.Column('data_konca', db.Date)
    peak_date = db.Column('data_maksimum', db.Date)
    right_ascension = db.Column('rektasencja', db.Numeric)
    declination = db.Column('deklinacja', db.Numeric)
    velocity = db.Column('predkosc', db.Numeric)
    zhr = db.Column('zhr', db.Numeric)
    activity = db.Column('aktywnosc', db.String)


class Catalogue(Base):
    __tablename__ = 'katalog'

    name = db.Column('nazwa', db.String, primary_key=True)
    abbreviation = db.Column('skrot', db.String)
    publishing_year = db.Column('rok_wydania', db.SmallInteger)


class Observation(Base):
    __tablename__ = 'obserwacja'

    date = db.Column('data', db.DateTime, primary_key=True)
    astronomical_object = db.Column('obiekt_astronomiczny', db.String, primary_key=True)
    observatory = db.Column('obserwatorium', db.String, primary_key=True)
    astronomer = db.Column('astronom', db.String, primary_key=True)
    is_discovery = db.Column('czy_odkrycie', db.Boolean)
