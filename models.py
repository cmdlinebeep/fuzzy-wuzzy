import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

# Ensure that setup.sh has been sourced. Fail if variables not set
if not os.getenv('DATABASE_URL'):
    raise RuntimeError("Environment variables are not set, did you source setup.sh?")

database_path = os.getenv('DATABASE_URL')

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    '''
    setup_db(app)
    binds a flask application and a SQLAlchemy service
    '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()