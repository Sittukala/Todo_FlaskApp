from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY']= '074b612fe673756471f26c8766a45a1c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.static_folder = 'static'
database = SQLAlchemy(app)
crypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flask_lenddirect import routelinks