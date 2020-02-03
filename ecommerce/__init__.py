import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy.orm import relationship, join
from flask_debug import Debug
from sqlalchemy import func, or_
from flask_marshmallow import Marshmallow
from decimal import *

login_manager = LoginManager()

app = Flask(__name__)

# Often people will also separate these into a separate config.py file
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app,db)
Debug(app)
ma = Marshmallow(app)

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when Xthey need to login.
login_manager.login_view = "index"