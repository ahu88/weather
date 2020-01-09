import requests
from flask import render_template, request, flash, url_for, redirect
from weather_app import app, db

from weather_app.forms import AddForm, DeleteForm

from weather_app.models import City

from weather_app import app, db

@app.route('/', methods=['GET'])
def index_get():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3bc3653df522d33001dfe694ef6491d4'
    
    form1 = AddForm()
    form2 = DeleteForm()

    cities = City.query.all()


    weather_data = [] #list to hold all weather dictionaries for each city

    for city in cities:

        response = requests.get(url.format(city.name)).json()
        #print(response)

        #dictionary to hold important data from json request
        weather = {
            'city' : city.name,
            'temperature' : response['main']['temp'],
            'description' : response['weather'][0]['description'],
            'icon' : response['weather'][0]['icon']
        }

        weather_data.append(weather)

    #print(weather)

    return render_template('weather.html', weather_data=weather_data, form1=form1, form2=form2)

@app.route('/', methods=['POST'])
def index_post():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3bc3653df522d33001dfe694ef6491d4'
    
    form1 = AddForm()
    form2 = DeleteForm()  

    if form1.submit1.data and form1.validate_on_submit:
        new_city = form1.name.data
        print("yeet", new_city)
        
        response = requests.get(url.format(new_city)).json()
        #print(response)

        if list(response.keys())[0] == "cod":
            flash('Invalid city', 'danger')
        
        else:
            name_tmp = response['name']
            #print("Name", name_tmp)

            temp = City.query.filter_by(name=name_tmp).first()
            
            if temp:
                flash('Duplicate city', 'danger')
            
            else:
                new_city_object = City(name=new_city)
                
                db.session.add(new_city_object)
                db.session.commit()

                flash('City has been added!', 'success')

    if form2.submit2.data and form2.validate_on_submit:
        name_city = form2.name.data
        city = City.query.filter_by(name=name_city).first()

        if city:
            db.session.delete(city)
            db.session.commit()

            flash('City has been deleted!', 'success')

        else:
            flash ('City does not exist', 'danger')

    #make sure all POST requests redirect to a different view upon completion; and not render templates themselves
    return redirect(url_for('index_get'))

@app.route('/delete/<name>', methods=['GET'])
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Deleted {city.name}', 'success')
    return redirect(url_for('index_get'))

"""
from app import db
from app import City

city = City.query.get(5)
db.session.delete(city)
db.session.commit()
City.query.all()
"""