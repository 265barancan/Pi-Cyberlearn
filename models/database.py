import sqlite3
from flask import g
from werkzeug.local import LocalProxy
from config import Config

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(
            Config.DATABASE_URI,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        db.row_factory = sqlite3.Row
    return db

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

db = LocalProxy(get_db)

def init_db(app):
    app.teardown_appcontext(close_db)
    
    with app.app_context():
        # Create tables if they don't exist
        with app.open_resource('schema.sql', mode='r') as f:
            get_db().cursor().executescript(f.read())
        get_db().commit()
