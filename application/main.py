import configparser
import sys
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from PyQt5 import QtWidgets, uic

Base = declarative_base()

class AstronomicalObject(Base):
    __tablename__ = 'obiekt_astronomiczny'

    name = db.Column('nazwa', db.String, primary_key=True)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("gui/mainwindow.ui", self)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    db_config = config['database']
    url = db_config['user'] + ':' + db_config['password'] + '@' + db_config['host']

    engine = db.create_engine('mysql://' + url + '/astronomy')

    Session = db.orm.sessionmaker(bind=engine)
    session = Session()

    bodies = session.query(AstronomicalObject)
    for body in bodies:
        print(body.name)
    #session.add(body)
    session.commit()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    window.small_bodies_table.setRowCount(bodies.count())
    for i, body in enumerate(bodies):
        item = QtWidgets.QTableWidgetItem(body.name)
        window.small_bodies_table.setItem(i, 0, item)

    app.exec_()
