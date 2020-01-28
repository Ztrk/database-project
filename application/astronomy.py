import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Constellation(Base):
    __tablename__ = 'konstelacja'

    iau_abbrevation = db.Column('skrot_iau', db.String, primary_key=True)
    name = db.Column('nazwa', db.String)
    brightest_star = db.Column('najjasniejsza_gwiazda', db.String)

    def to_row(self):
        return [self.iau_abbrevation, self.name, self.brightest_star]


class AstronomicalObject(Base):
    __tablename__ = 'obiekt_astronomiczny'

    name = db.Column('nazwa', db.String, primary_key=True)

    def to_row(self):
        return [self.name, self.name]
