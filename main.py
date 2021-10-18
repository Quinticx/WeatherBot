import discord
import os
import time
import discord.ext
import Weather
import requests
import pytz
from geopy.geocoders import Nominatim
from datetime import datetime
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, check
#^ basic imports for other features of discord.py and python ^

client = discord.Client()
client = commands.Bot(command_prefix='!')
botname = "Radar"
color = 0x006994
geolocator = Nominatim(user_agent="geoapiExercises")

@client.event
async def on_ready():
    print("bot online")


@client.command()
async def Help(ctx):
    embed = discord.Embed(title="Help",description=f"{botname}'s Commands",color=color)
    embed.add_field(name="!weather",value=f"Gives current weather conditions and temperature for a given zipcode. !weather 62025 would return the weather for Edwardsville, IL for.",inline=False)
    embed.add_field(name="!radar",value=f"Returns gif of current radar.",inline=False)
    embed.add_field(name="!forecast",value=f"Gives 6 day forecast for a given zipcode. !forecast 62025 would return the forecast for Edwardsville, IL for example.",inline=False)
    embed.add_field(name="!nerdstats",value=f"Gives more detailed weather information for current zipcode. !nerdstats 62025 would give detailed statistics for Edwardsville, IL for example.",inline=False)
    embed.add_field(name="!walerts",value=f"Gives information about current weather alerts such as Flood, Severe Storm, and Tornado Watches/Warnings if any are present for zipcode. !walerts 62025 would give any weather alerts for Edwardsville, IL for example",inline=False)
    await ctx.send(embed=embed)


@client.command()
async def weather(ctx, zipcode):
    w = Weather.getWeather(zipcode)
    icon = w['current']['weather'][0]['icon']
    response = requests.get(f"https://openweathermap.org/img/wn/{icon}@2x.png")
    with open('icon.png', 'wb') as f:
        f.write(response.content)
        if w['current']['weather'][0]['main'] == 'Clouds':
                current = 'Cloudy'
                emoji = '<:scatteredcloudsday:866018074552172554>'
        elif w['current']['weather'][0]['main'] == 'Thunderstom':
                current = 'Thunderstorms'
                emoji = '<:thunderstormday:866018075068596254>'
        elif w['current']['weather'][0]['main'] == 'Drizzle':
                current = 'Drizzling'
                emoji = ' <:rainday:866016681704030208>'
        elif w['current']['weather'][0]['main'] == 'Fog':
                current = 'Foggy'
                emoji = ' <:mistday:866018074666467328>'
        elif w['current']['weather'][0]['main'] == 'Mist':
                current = 'Misting'
                emoji = ' <:mistday:866018074666467328>'
        elif w['current']['weather'][0]['main'] == 'Tornado':
                current = 'Tornadic -- Seek Shelter Immediately'
                emoji = '<:cloud_tornado:>'
        elif w['current']['weather'][0]['main'] == 'Rain':
                current = 'Raining'
                emoji = '<:showerrainday:866018074556629013>'
        elif w['current']['weather'][0]['main'] == 'Snow':
                current = 'Snowing'
                emoji = '<:snowday:866018074557546577>'
        elif w['current']['weather'][0]['main'] == 'Haze':
                current = 'Hazy'
                emoji = ' <:mistday:866018074666467328>'
        else:
                current = w['current']['weather'][0]['main']
                emoji = '<:clearday:866018074360283136>'

        await ctx.send(
            f"Current weather for {zipcode} is {current} with {w['current']['weather'][0]['description']}{emoji}. It is currently {w['current']['temp']:.1f}°F and feels like {w['current']['feels_like']:.1f}°F.")


@client.command()
async def radar(ctx):
        radar = Weather.getRadar()
        await ctx.send(file=discord.File(radar))


@client.command()
async def nerdstats(ctx, zipcode):
        w = Weather.getWeather(zipcode)
        sunutcTime = datetime.fromtimestamp(w['current']['sunrise'])
        suncst = Weather.sunriseSunsetTime(sunutcTime)
        setutcTime = datetime.fromtimestamp(w['current']['sunset'])
        setcst = Weather.sunriseSunsetTime(setutcTime)
        await ctx.send(
            f"```Humidity: {w['current']['humidity']}% \nPressure: {w['current']['pressure']} mbar \nUV Index: {w['current']['uvi']} \nWind Speed: {w['current']['wind_speed']} mph \nVisibility: {(w['current']['visibility']/1000)*0.62137:.2f} mi \nDew Point: {w['current']['dew_point']}°F \nMoon Phase: {w['daily'][0]['moon_phase']} \nSunrise: {suncst} AM \nSunset: {setcst} PM```")


@client.command()
async def walerts(ctx, zipcode):
        w = Weather.getWeather(zipcode)
        if w['alerts']:
                await ctx.send(
                    f"There is a {w['alerts'][0]['event']} in affect. ```{w['alerts'][0]['description']}```"
                )
        else:
                await ctx.send(f"There are no alerts for {zipcode}")


@client.command()
async def forecast(ctx, zipcode):
    f = Weather.getForecast(zipcode)
    results = {}
    for x in f['list']:
        utcTime = datetime.fromtimestamp(x['dt'])
        cst = Weather.toCentralTime(utcTime)
        if cst[0:10] not in results:
            results[cst[0:10]] = [x['main']['temp_max'], x['weather'][0]['main']]

    to_send = f'Forecast for {zipcode}\n'
    to_send += '   Date   | Temp (°F) |  Weather\n'
    to_send += '--------------------------------\n'

    for key, value in results.items():
        to_send += '{0} |   {1}   | {2}\n'.format(key, int(value[0]+16), value[1])

    await ctx.send(to_send)


client.run(os.getenv("TOKEN"))