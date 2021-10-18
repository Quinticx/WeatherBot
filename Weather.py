from pyowm.owm import OWM
import os
import requests
import json
import pytz
from geopy.geocoders import Nominatim

owm = OWM(os.environ['OWM_API_KEY'])
mgr = owm.weather_manager()
geolocator = Nominatim(user_agent="geoapiExercises")

def toCentralTime(timestamp):
    cst = pytz.timezone('US/Central')
    fmt = '%d-%m-%Y %H:%M:%S'
    return timestamp.astimezone(cst).strftime(fmt)


def sunriseSunsetTime(timestamp):
    cst = pytz.timezone('US/Central')
    fmt = '%H:%M:%S'
    return timestamp.astimezone(cst).strftime(fmt)

def getWeather(zipcode):
    """ Returns a weather object"""
    api_key = os.environ["OWM_API_KEY"]
    location = geolocator.geocode(zipcode)
    data = location.raw
    lat = data['lat']
    lon = data['lon']
    response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units=imperial")
    weather = json.loads(response.text)
    return weather


def getRadar():
    """ Returns a radar gif for the KLSX radar station"""
    # TODO: Grab closest station's radar for a given zipcode
    response = requests.get('https://radblast-aa.wunderground.com/cgi-bin/radar/WUNIDS_map?station=LSX&brand=wui&num=10&delay=60&type=NCR&frame=0&scale=4.999&noclutter=0&t=1621025493&showstorms=0&map.x=400&map.y=240&centerx=400&centery=240&transx=0&transy=0&showlabels=1&severe=1&rainsnow=1&lightning=1')
    with open('radar.gif','wb') as f:
        f.write(response.content)
    
    return 'radar.gif'
    
def getForecast(zipcode):
    """ Returns a forecast object"""
    api_key = os.environ["OWM_API_KEY"]
    location = geolocator.geocode(zipcode)
    data = location.raw
    lat = data['lat']
    lon = data['lon']
    #url = 'http://api.openweathermap.org/data/2.5/forecast?zip=' + zipcode + '&units=imperial&appid=' + api_key
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=imperial'
    forecast = requests.get(url).json()
    return forecast