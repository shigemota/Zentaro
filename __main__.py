from views import *
from app import app

if __name__ == '__main__':
    db.bind(**app.config['PONY'])
    db.generate_mapping(create_tables=True)
    app.run(port=8080, host='127.0.0.1')
