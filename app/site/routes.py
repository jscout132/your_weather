from flask import Blueprint, render_template, request, jsonify
import requests
from ..api.open_weather import weather, f_temp, icon, sunrise, sunset, api_key

from models import User, FavoriteCities, login_manager, sqla, cities_schema, city_schema
from forms import AddFavCity, DelFavCity
from helpers import token_required
import flask_login

site = Blueprint('site',__name__, template_folder='site_pages')


@site.route('/')
@site.route('/home')
def home():
    return render_template('index.html', weather=weather, f_temp=int(f_temp), 
                           icon=icon, sunrise=sunrise, sunset=sunset)

@site.route('/about')
def about():
    return render_template('about.html')


# TODO add some qc around the user_input to control for mis spellings- i think google maps will help with that? or the geocoding thing
# TODO add some not allowed to view this page if you aren't logged in to profile and edit
@site.route('/profile', methods = ['POST','GET'])
def profile():
    user = User()
    form = AddFavCity()

    user_input = request.form
    current_id = flask_login.current_user.get_id()
    user_cities = FavoriteCities.query.filter_by(user_id = current_id).all()
    print(user_cities)

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
            if request.method == 'POST':  #and form.validate_on_submit()
                city = user_weather['name']
                user_id = flask_login.current_user.get_id()    
                new_city = FavoriteCities(city = city, user_id = user_id)
                sqla.session.add(new_city)
                sqla.session.commit()
                response = city_schema.dump(new_city)
                print('this is the city schema dump response', print(jsonify(response)))

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


@site.route('/edit/<id>', methods=['DELETE'])
def delete_item(id):
    print('in the delete item def')
    del_city = FavoriteCities.query.get(id)

    sqla.session.delete(del_city)
    sqla.session.commit()
    response = city_schema.dump(del_city)
    return 'Item deleted successfully'

# book_page = Blueprint('book_page', __name__, url_prefix='/books')

# @api.route('/books/<isbn>', methods = ['DELETE'])
# @token_required
# def del_book(current_user_token, isbn):
#     books = Books.query.get(isbn)
#     db.session.delete(books)
#     db.session.commit()
#     response = book_schema.dump(books)
#     return jsonify(response)