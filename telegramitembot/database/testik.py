import telebot
from telebot import types
import sqlite3 as sq
import cv2 as cv2
import folium
import base64
from folium import IFrame
from folium import plugins
from cv2 import cv2

bot = telebot.TeleBot('2108542703:AAGWaPn8DKxgLc-3wt_gSKpPFE4ahoffGI0')
users = dict()
m = folium.Map(location=[55.7644348, 37.592083], zoom_start=11)
con = sq.connect("/Users/eugeneadylin/Desktop/telegramitembot/database/mostymsc.db", check_same_thread=False)
cur = con.cursor()

@bot.message_handler(commands=['start'])
def start(message):
    telegram_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("отправить фото")
    markup.add(item1)
    bot.send_message(message.chat.id,
                     "здравствуйте", reply_markup=markup)
    if telegram_id not in users.keys():
        users[str(telegram_id)] = 0

@bot.message_handler(content_types=['text'])
def otvet(message):
    if message.text == 'отправить фото':
        users[str(message.from_user.id)] = 1
        print(users)
        bot.send_message(message.chat.id, 'отправте ваше фото')
    if message.text == 'завершить':
        user_id = message.from_user.id
        cur.execute(
            "INSERT INTO photos_from_users(latitude, longtitude, link, user_id) VALUES (?, ?, ?, ?)",
            (users[str(str(message.from_user.id) + 'latitude')], users[str(str(message.from_user.id) + 'longitude')], users[str(str(message.from_user.id) + '_image_path')], user_id,))
        con.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("отправить фото")
        markup.add(item1)
        bot.send_message(message.chat.id,
                         "фото сохранено", reply_markup=markup)


@bot.message_handler(content_types=["photo"])
def photo(message):
    if users[str(message.from_user.id)] == 1:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = file_info.file_path
        print(src)
        print(downloaded_file)
        with open("/Users/eugeneadylin/Desktop/telegramitembot/photos_from_u", 'wb') as new_file:
            new_file.write(downloaded_file)
        users[str(str(message.from_user.id) + '_image_path')] = src
        users[str(message.from_user.id)] = 2
        bot.send_message(message.chat.id, 'отправте геотег')

@bot.message_handler(content_types=["location"])
def location(message):
    if users[str(message.from_user.id)] == 2:
        latitude = message.location.latitude
        longitude = message.location.longitude
        users[str(str(message.from_user.id) + 'latitude')] = latitude
        users[str(str(message.from_user.id) + 'longitude')] = longitude

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("завершить")
        markup.add(item1)
        bot.send_message(message.chat.id, 'нажмите завершить', reply_markup=markup)



bot.polling(none_stop=True)