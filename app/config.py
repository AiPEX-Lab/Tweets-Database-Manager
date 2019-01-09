import os


class Config:
    DIALECT = 'mysql'
    DRIVER = 'mysqlconnector'
    USERNAME = 'root'
    PASSWORD = 'root'
    HOST = 'localhost'  
    PORT = '3306'


class TestingConfig(Config):
    TESTING = True
    DATABASE = 'tw_test'
    TEST_DATABASE_URL = '{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
        Config.DIALECT, Config.DRIVER, Config.USERNAME, Config.PASSWORD, Config.HOST, Config.PORT, DATABASE
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or TEST_DATABASE_URL


config = {
    'testing': TestingConfig,
    'default': TestingConfig
}

