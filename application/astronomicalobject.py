import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AstronomicalObject(Base):
    __tablename__ = 'obiekt_astronomiczny'

    name = db.Column('nazwa', db.String, primary_key=True)

    def to_row(self):
        return [self.name, self.name]
