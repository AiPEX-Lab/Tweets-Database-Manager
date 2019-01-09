from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import config
from sqlalchemy.ext.declarative import declarative_base


def _init_base():
    """
    This is a base wrapper
    :return: base object
    """
    Base = declarative_base()
    return Base


def _init_engine():
    """
    This is a create_engine wrapper
    :return: engine object
    """
    engine = create_engine(config['testing'].TEST_DATABASE_URL)
    return engine


def _init_session():
    """
    This is a sessionmaker wrapper
    :return: engine object
    """
    Session = sessionmaker()
    # Session = sessionmaker(bind=engine)
    return Session


class Manager(object):
    """
    This is a db_manager with wrapper functions
    :return: engine object
    """

    engine = _init_engine()
    Session = _init_session()
    Base = _init_base()

    def __init__(self):
        Manager.engine.connect()
        Manager.Session.configure(bind=Manager.engine)

    def create_all(self):
        # care
        from app.db_models import Tweet
        Manager.Base.metadata.create_all(Manager.engine)

    def drop_all(self):
        from app.db_models import Tweet
        Manager.Base.metadata.drop_all(Manager.engine)

    def reset_db(self):
        self.drop_all()
        self.create_all()
