import requests
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
#app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '411dcc853ee655596ce1afa6d2da1f2f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#to hash user passwords
bcrypt = Bcrypt(app)

#to manage user sessions
login_manager = LoginManager(app)

login_manager.login_message_category = 'info'

#to avoid circular imports
from weather_app import routes #we need to import routes here so when we run application it can find them

"""
from app import db
from app import City

city = City.query.get(5)
db.session.delete(city)
db.session.commit()
City.query.all()
"""