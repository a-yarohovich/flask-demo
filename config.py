import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard key'
    USER_ADMIN = os.environ.get('ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DelevopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = ''
    MAIL_PORT = 1111
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = 'subj'
    MAIL_SENDER = 'a.ya'
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = '00hnb98A'
    MYSQL_DATABASE_DB = 'demo'
    MYSQL_DATABASE_HOST = 'localhost'


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'develop': DelevopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DelevopmentConfig
}
