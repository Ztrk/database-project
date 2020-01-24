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

    def to_row(self):
        return [self.full_name, self.country, self.birth_date,
            self.death_date, self.name_mpc]

class Observatory(Base):
    __tablename__ = 'obserwatorium'

    iau_code = db.Column('kod_iau', db.String, primary_key=True)
    latitude = db.Column('szerokosc_geograficzna', db.Numeric)
    longitude = db.Column('dlugosc_geograficzna', db.Numeric)
    country = db.Column('kraj', db.String)
    full_name = db.Column('pelna_nazwa', db.String)
    name_mpc = db.Column('nazwa_mpc', db.String)

    def to_row(self):
        return [self.full_name, self.name_mpc, self.iau_code,
            self.country, self.latitude, self.longitude]

class Constellation(Base):
    __tablename__ = 'konstelacja'

    iau_abbreviation = db.Column('skrot_iau', db.String, primary_key=True)
    name = db.Column('nazwa', db.String)
    brightest_star = db.Column('najjasniejsza_gwiazda', db.String)

    def to_row(self):
        return [self.name, self.iau_abbreviation, self.brightest_star]


class AstronomicalObject(Base):
    __tablename__ = 'obiekt_astronomiczny'

    name = db.Column('nazwa', db.String, primary_key=True)

    def to_row(self):
        return [self.name, self.name]

class Catalogue(Base):
    __tablename__ = 'katalog'

    name = db.Column('nazwa', db.String, primary_key=True)
    abbreviation = db.Column('skrot', db.String)
    publishing_year = db.Column('rok_wydania', db.Date)

    def to_row(self):
        return [self.name, self.abbreviation, self.publishing_year]

class Observation(Base):
    __tablename__ = 'obserwacja'

    date = db.Column('data', db.DateTime, primary_key=True)
    astronomical_object = db.Column('obiekt_astronomiczny', db.String, primary_key=True)
    observatory = db.Column('obserwatorium', db.String, primary_key=True)
    astronomer = db.Column('astronom', db.String, primary_key=True)
    is_discovery = db.Column('czy_odkrycie', db.Boolean)

    def to_row(self):
        return [self.astronomical_object, self.astronomer, self.observatory,
            self.date, self.is_discovery]
