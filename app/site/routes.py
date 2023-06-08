from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import requests
from datetime import datetime

from ..api.open_weather import weather, api_key, daily
from ..assets.weekday_dict import weekdays
from models import User, FavoriteCities, login_manager, sqla, cities_schema, city_schema
from forms import AddFavCity, DelFavCity
from helpers import token_required
import flask_login

site = Blueprint('site',__name__, template_folder='site_pages')


@site.route('/')
@site.route('/home')
def home():
    day = datetime.now().weekday()
    return render_template('index.html', weather = weather, daily = daily, weekdays = weekdays, day = day)

@site.route('/about')
def about():
    return render_template('about.html')


# TODO add some qc around the user_input to control for mis spellings- i think google maps will help with that? or the geocoding thing
# TODO add some not allowed to view this page if you aren't logged in to profile and edit
# TODO see if i can just use weather instead of the entire requests.get for fav_city_weather
@site.route('/profile', methods = ['POST','GET'])
def profile():
    user = User()
    form = AddFavCity()

    user_input = request.form
    current_id = flask_login.current_user.get_id()
    user_cities = FavoriteCities.query.filter_by(user_id = current_id).all()

    if len(user_cities)>0:
        fav_city_weather = [requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={i}&appid={api_key}&units=imperial').json() for i in user_cities]
    
    else:
        fav_city_weather = None

    if 'user_input' not in user_input:
        return render_template('profile.html', user=user, user_input = user_input, 
                               form = form, user_cities = user_cities, fav_city_weather = fav_city_weather)
        
    else:
        for k,v in user_input.items():
            weather_url = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={v}&appid={api_key}&units=imperial')
            user_weather = weather_url.json()

        try:
            # TODO figure out why form.validate_on_submit() isn't working
            if request.method == 'POST' and form.validate_on_submit():
                user_id = flask_login.current_user.get_id()    
                new_city = FavoriteCities(city = user_weather['name'], user_id = user_id)
                print('this is the favorite cities', FavoriteCities())
                sqla.session.add(new_city)
                sqla.session.commit()
                response = city_schema.dump(new_city)
                # idk why jsonify(response) is None
                print('this is the city schema dump response', jsonify(response))

                return render_template('profile.html', user = user, user_input = user_input, user_weather = user_weather, 
                                       form = form, user_cities = user_cities, fav_city_weather = fav_city_weather)
            
        except:
            raise Exception('invalid form information')

        return render_template('profile.html', user = user, user_input = user_input, user_weather = user_weather, 
                               form = form, user_cities = user_cities, fav_city_weather = fav_city_weather)


# TODO test edit page without any favorited cities   
@site.route('/edit.html', methods = ['GET','POST','DELETE'])
def edit():
    user = User()
    form = DelFavCity()
    current_id = flask_login.current_user.get_id()
    user_cities = FavoriteCities.query.filter_by(user_id = current_id).all()        
    return render_template('edit.html', user = user, form = form, user_cities = user_cities)


@site.route('/edit/<id>', methods = ['DELETE', 'POST'])
def delete_item(id):
    selected_city = FavoriteCities.query.filter_by(id = id).first()
    print('in the delete items')
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
