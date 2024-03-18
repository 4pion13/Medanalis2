import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_mail import Mail, Message




app = Flask(__name__)

'''
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Doctor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '3dphystech@gmail.com'  # введите свой адрес электронной почты здесь
app.config['MAIL_DEFAULT_SENDER'] = '3dphystech@gmail.com'  # и здесь
app.config['MAIL_PASSWORD'] = 'ifjc graw qsng lhww'  # введите пароль
UPLOAD_FOLDER='user_directory'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
'''
APP_SETTINGS_CONFIG = os.getenv('APP_SETTINGS')
if APP_SETTINGS_CONFIG is None:
    APP_SETTINGS_CONFIG = 'sweater.config.DevelopConfig'
app.config.from_object(APP_SETTINGS_CONFIG)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'zip'}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)
db.create_all()

from sweater import routes, models