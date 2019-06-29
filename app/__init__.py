# -*- coding: utf8 -*-
"""
app
~~~

Main application of syllabus project
"""

import os
from flask import Flask
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from configparser import ConfigParser


def dbconnect(engine=None) -> Session:
    engine = engine or create_engine(__db_uri__,
                                     echo=config.getboolean('postgresql', 'debug'))
    session_factory = sessionmaker(bind=engine)
    return session_factory()


app = Flask(__name__)
app.secret_key = os.urandom(32)

APP_PATH = os.path.dirname(app.root_path)

config = ConfigParser()
config.read(os.path.join(APP_PATH, 'config.ini'))

__db_uri__ = URL(
    drivername='postgresql',
    host=config.get('postgresql', 'host', fallback='localhost'),
    port=config.get('postgresql', 'port', fallback='5432'),
    username=config.get('postgresql', 'user'),
    password=quote_plus(config.get('postgresql', 'password')),
    database=config.get('postgresql', 'database')
)

engine = create_engine(__db_uri__, echo=config.getboolean('postgresql', 'debug'))
SessionFactory = sessionmaker(bind=engine)
Base = declarative_base()

from .models import *

Base.metadata.create_all(bind=engine)
db = dbconnect(engine)  # type: Session

from . import utils
from . import views
from .api import *

api.add_resource(Sessions, '/s/<int:course_id>')
api.add_resource(Assessments, '/a/<int:course_id>')
api.add_resource(Outcomes, '/o/<int:course_id>')
