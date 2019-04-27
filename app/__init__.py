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
from .utils import config

app = Flask(__name__)
app.secret_key = os.urandom(32)

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

from . import models

Base.metadata.create_all(bind=engine)
db = SessionFactory()  # type: Session

from . import views
