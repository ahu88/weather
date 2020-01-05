#runs the application
#import from __init__.py file within the package (app = Flask(__name__))
from weather_app import app

if __name__ == "__main__":
    app.run(debug=True)

"""
from weather_app import db
from weather_app.models import City

city = City.query.get(5)
db.session.delete(city)
db.session.commit()
City.query.all()

City.query.delete()
db.session.commit()

exit()
"""