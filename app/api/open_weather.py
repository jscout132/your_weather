import requests, json
from random import randint
import datetime

from ..assets.city_list import cities
# TODO eventually maybe put all of the things you need to export in a dictionary and only import 
# that into the routes page

# API key from Open Weather
api_key='e5d87fd9e2a278959ee764883b7aecfc'

city=cities[randint(0,30)]

url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial'

weather_url = requests.get(url)
weather = weather_url.json()

daily_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={weather["coord"]["lat"]}&lon={weather["coord"]["lon"]}&appid={api_key}&units=imperial'
daily_weather = requests.get(daily_url)
daily = daily_weather.json()


# TODO build out functionality to tell the current day then add 4 days to accompany the daily forecast section
# TODO maybe have it enlarge when you click on a certain day?