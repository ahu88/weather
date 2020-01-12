import requests
from flask import render_template, request, flash, url_for, redirect
from weather_app import app, db

from weather_app.forms import AddForm, DeleteForm, LoginForm, RegistrationForm

from weather_app.models import City, User, cities

from weather_app import app, db, bcrypt

from flask_login import login_user, current_user, logout_user, login_required

@app.route("/home")
@app.route('/', methods=['GET'])
def index_get():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3bc3653df522d33001dfe694ef6491d4'
    
    form1 = AddForm()
    form2 = DeleteForm()

    #do user authentication here?????????????????????????????
    #i.e. only add cities corresponding to the logged in user

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

    return render_template('home.html', weather_data=weather_data, form1=form1, form2=form2)

@app.route('/', methods=['POST'])
def index_post():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3bc3653df522d33001dfe694ef6491d4'
    
    form1 = AddForm()
    form2 = DeleteForm()  

    if not current_user.is_authenticated:
        flash('You must be logged in', 'danger')

    if form1.submit1.data and form1.validate_on_submit:
        new_city = form1.name.data
        #print("yeet", new_city)
        
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

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index_get'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form = form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index_get'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        #checks if user exists and password is correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect (url_for('index_get'))
            flash('Logged in!', 'success')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index_get'))

"""
from weather_app import db
from weather_app.models import City

city = City.query.get(5)
db.session.delete(city)
db.session.commit()
City.query.all()
"""