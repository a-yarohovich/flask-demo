import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard key'
    USER_ADMIN = os.environ.get('ADMIN')
    # email server
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SENDER = 'demo.flask.app@gmail.com'

    @staticmethod
    def init_app(app):
        pass


class DelevopmentConfig(Config):
    DEBUG = True
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
