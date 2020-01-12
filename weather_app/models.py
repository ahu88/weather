#database models
from weather_app import db, login_manager

from flask_login import UserMixin

#decorated function from LoginManager to reload user from user_id stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

cities = db.Table('cities',
    db.Column('city_id', db.Integer, db.ForeignKey('city.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    #"user_cities is essentially now an attribute/column under User"
    cities_rel = db.relationship('User', secondary=cities, backref=db.backref('user_cities', lazy='dynamic'))

    #user1.user_cities.append(city1)
    #db.session.commit()

    #for city in user.user_cities():
    #   print city.name

    def __repr__(self):
        return f"City('{self.name}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) #hashed password is 60 chars
    
    

    #how our object is printed when we print it
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

#Association table (many-to-many relationship)
#not a model since we won't modify it
