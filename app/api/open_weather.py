import requests, json
from random import randint
import datetime

from ..assets.city_list import cities
from ..assets.weather_id import weather_ids
# TODO eventually maybe put all of the things you need to export in a dictionary and only import 
# that into the routes page

# API key from Open Weather
api_key='e5d87fd9e2a278959ee764883b7aecfc'

city=cities[randint(0,30)]
url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial'

weather_url = requests.get(url)
weather = weather_url.json()
f_temp = weather['main']['temp']
weather_id = weather['weather'][0]['main']

# TODO figure out what icon isn't rendering
icon = ''
if weather_id.lower() in weather_ids:
    icon = weather_ids[weather_id.lower()]

# TODO work out how to display sunset and sunrise times
sunrise = datetime.datetime.fromtimestamp(weather['sys']['sunrise'])
sunset = datetime.datetime.fromtimestamp(weather['sys']['sunset'])

