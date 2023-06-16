from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import requests
from datetime import datetime
import requests, json
from random import randint
import flask_login

from flask_login import current_user

from ..assets.city_list import cities
from models import User, FavoriteCities, login_manager, sqla, cities_schema, city_schema

open_weather = Blueprint('open_weather',__name__)

# API key from Open Weather
api_key='e5d87fd9e2a278959ee764883b7aecfc'

city=cities[randint(0,30)]

url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial'

weather_url = requests.get(url)
weather = weather_url.json()

daily_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={weather["coord"]["lat"]}&lon={weather["coord"]["lon"]}&appid={api_key}&units=imperial'
daily_weather = requests.get(daily_url)
daily = daily_weather.json()
