class Config(object):
    SECRET_KEY = 'any-secret-key-you-choose'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '3dphystech@gmail.com'  # введите свой адрес электронной почты здесь
    MAIL_DEFAULT_SENDER = '3dphystech@gmail.com'  # и здесь
    MAIL_PASSWORD = 'ifjc graw qsng lhww'  # введите пароль
    UPLOAD_FOLDER = 'user_directory'

class DevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Doctor.db'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://rnovikov:Qwerty123@192.168.68.67/fistech'