from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import requests
from datetime import datetime

from ..api.open_weather import weather, api_key, daily
from ..assets.weekday_dict import weekdays
from models import User, FavoriteCities, login_manager, sqla, cities_schema, city_schema
from forms import AddFavCity, DelFavCity
from helpers import token_required
import flask_login
from flask_login import current_user, login_required

site = Blueprint('site',__name__, template_folder='site_pages')

@site.route('/')
@site.route('/home')
def home():
    day = datetime.now().weekday()
    return render_template('index.html', weather = weather, daily = daily, weekdays = weekdays, day = day)

@site.route('/about')
def about():
    return render_template('about.html')


@site.route('/profile', methods = ['POST','GET'])
@login_required
def profile():
    user = User()
    form = AddFavCity()
    day = datetime.now().weekday()


    # gets the daily forecast for the user's city, entered when creating a profile
    find_user = user.query.get(current_user.id)
    user_profile_city = find_user.user_city
    user_city_weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={user_profile_city}&appid={api_key}&units=imperial').json()
    
    # API errors
    # TODO: build out more specific error responses
    errors =['400','401','404','429','5xx']

    if user_city_weather['cod'] not in errors:
        user_city_weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={user_profile_city}&appid={api_key}&units=imperial').json()
        user_daily = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={user_city_weather["coord"]["lat"]}&lon={user_city_weather["coord"]["lon"]}&appid={api_key}&units=imperial').json()

    else:
        user_daily = ''

    
    current_id = flask_login.current_user.get_id()
    user_cities = FavoriteCities.query.filter_by(user_id = current_id).all()

    if len(user_cities)>0:
        fav_city_weather = [requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={i}&appid={api_key}&units=imperial').json() for i in user_cities]
    
    else:
        fav_city_weather = None


    #holder dictionary to shorten list of variables being passed to profile.html
    holder_dict = {
        'fav_city_weather': fav_city_weather,
        'user_daily': user_daily,
        'form': form,
        'weekdays': weekdays,
        'day': day
    }

    # pulling city entered into search bar
    user_input = request.form
    
    if request.method == 'POST': # and form.validate_on_submit():
        print('in the try if')

        address_list = user_input.getlist('city')
        address = address_list[0].split(',')
        city = address[0]

        new_city = FavoriteCities(city = city, user_id = current_id)
        sqla.session.add(new_city)
        sqla.session.commit()
        response = city_schema.dump(new_city)
        return redirect('/profile')


    return render_template('profile.html', user = user, holder_dict = holder_dict)


@site.route('/edit.html', methods = ['GET','POST','DELETE'])
@login_required
def edit():
    user = User()
    form = DelFavCity()
    current_id = flask_login.current_user.get_id()
    user_cities = FavoriteCities.query.filter_by(user_id = current_id).all()        
    return render_template('edit.html', user = user, form = form, user_cities = user_cities)


@site.route('/edit/<id>', methods = ['DELETE', 'POST'])
def delete_item(id):
    selected_city = FavoriteCities.query.filter_by(id = id).first()
    if request.form.get('_method') == 'DELETE':  #and form.validate_on_submit()
        sqla.session.delete(selected_city)
        sqla.session.commit()
        response = city_schema.dump(selected_city)
        print('item deleted successfully')

    else:
        new_city_name = request.form.get('city_name')
        print('new city name', new_city_name)
        selected_city.city = new_city_name
        sqla.session.commit()

    return redirect(url_for('site.profile'))


@site.route('/maps')
def maps():
    return render_template('maps.html')
