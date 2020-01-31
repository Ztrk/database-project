import configparser
import sys
import sqlalchemy as db
from PyQt5 import QtWidgets
from mainwindow import MainWindow

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    db_config = config['database']
    url = db_config['user'] + ':' + db_config['password'] + '@' + db_config['host']

    engine = db.create_engine('mysql://' + url + '/astronomy')

    Session = db.orm.sessionmaker(bind=engine)
    session = Session()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(session)
    window.show()

    app.exec_()
    session.commit()
