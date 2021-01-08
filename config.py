import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'Your key here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ''' configure these as desired
    MAIL_SERVER : default ‘localhost’
    MAIL_PORT : default 25
    MAIL_USE_TLS : default False
    MAIL_USE_SSL : default False
    MAIL_DEBUG : default app.debug
    MAIL_USERNAME : default None
    MAIL_PASSWORD : default None
    MAIL_DEFAULT_SENDER : default None
    MAIL_MAX_EMAILS : default None
    MAIL_SUPPRESS_SEND : default app.testing
    MAIL_ASCII_ATTACHMENTS : default False
    '''

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.db')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}