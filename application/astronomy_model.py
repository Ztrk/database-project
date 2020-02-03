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
                return self.get_header()[section]
            elif orientation == QtCore.Qt.Vertical:
                return str(section + 1)

class AstronomerModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(AstronomerModel, self).__init__(session, astronomy.Astronomer, *args, **kwargs)

    def to_row(self, astronomer):
        return (astronomer.full_name, astronomer.country, astronomer.birth_date,
            astronomer.death_date, astronomer.name_mpc)

    def get_header(self):
        return ('Pełne imię', 'Kraj', 'Data urodzenia', 'Data śmierci', 'Nazwa w mpc')


class ObservatoryModel(AstronomyModel):
    def __init__(self, session, *args, **kwargs):
        super(ObservatoryModel, self).__init__(session, astronomy.Observatory, *args, **kwargs)

    def to_row(self, observatory):
        return [observatory.full_name, observatory.name_mpc, observatory.iau_code,
            observatory.country, observatory.latitude, observatory.longitude]

    def get_header(self):
        return ('Pełna nazwa', 'Nazwa w MPC', 'Kod IAU', 'Kraj', 
            'Szerokość geograficzna', 'Długość geograficzna')
