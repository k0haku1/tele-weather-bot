import os
from dotenv import load_dotenv
import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime


load_dotenv()
API_KEY = os.getenv('API_KEY')
API_TOKEN = os.getenv('API_TOKEN')

LOCATION_NAME_TO_KEY = {
    "Ulyanovsk" : "Ульяновск, Приволжский федеральный округ, Россия",
    "Saint Petersburg" : "Санкт-Петербург, Северо-Западный федеральный округ, Россия",
    "Moscow" : "Москва, Центральный федеральный округ, Россия"
}

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Дарова заебал")
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for location_name in LOCATION_NAME_TO_KEY.keys():
        markup.add(KeyboardButton(location_name))
    bot.send_message(message.chat.id, "Choose city", reply_markup=markup)

def get_current_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return current_date

@bot.message_handler(func=lambda message : message.text in LOCATION_NAME_TO_KEY.keys())
def send_wather(message):
    location_name = message.text
    date_now = get_current_date()
    weather = get_weather(location = location_name, date=date_now)
    bot.send_message(message.chat.id, f"Weather in {location_name} - ({date_now}) - {weather} °C")

def get_weather(location, date):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date}?key={API_KEY}"
    responce = requests.get(url)
    weather_by_days = responce.json()["days"]

    for weather in weather_by_days:
        temp = far_to_celsius(weather["temp"])

    return temp

def far_to_celsius(temp):
    celsius = (temp - 32) * 5 / 9
    return round(celsius)

bot.polling()