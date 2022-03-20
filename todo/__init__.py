import logging
import logging.config

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB = 'sqlite:///tasks.db'

logging.config.fileConfig(
    fname='./todo/logger.conf', disable_existing_loggers=False
)

logger = logging.getLogger('todo')

app = Flask('todo')

# create_table = not os.path.exists('./tasks.db')
create_table = True

app.config['SQLALCHEMY_DATABASE_URI'] = DB
engine = create_engine(DB)
Base = declarative_base()
Session = sessionmaker(engine)
