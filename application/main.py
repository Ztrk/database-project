import sqlalchemy as db
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    db_config = config['database']
    url = db_config['user'] + ':' + db_config['password'] + '@' + db_config['host']

    engine = db.create_engine('mysql://' + url + '/astronomy', echo = True)
    engine.connect()
