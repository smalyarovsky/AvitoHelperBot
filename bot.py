import config
import condition
import telebot
import requests
import timeК
from lxml import html
from telebot import types
from telebot.util import async_dec
bot = telebot.TeleBot(config.token)
ads_id = set()


@bot.message_handler(commands=['start', 'help'])
def chill(message):
    bot.send_message(message.from_user.id, config.info_message)


@bot.message_handler(commands=['new'])
def chill(message):
    bot.send_message(message.from_user.id, config.new_message)
    condition.waiting_for_link = True


@bot.message_handler(func=lambda message: condition.waiting_for_link)
def chill(message):
    bot.send_message(message.from_user.id, config.got_a_link_message)
    condition.waiting_for_link = False
    condition.have_a_link = True
    config.url = message.text
    scan()


@bot.message_handler(commands=['parse'], func=lambda message: not condition.have_a_link)
def chill(message):
    bot.send_message(message.from_user.id, config.parse_without_link_message)
    condition.waiting_for_link_to_parse = True


@bot.message_handler(commands=['parse'], func=lambda message: condition.have_a_link and not condition.parsing)
def chill(message):
    bot.send_message(message.from_user.id, config.parse_message)
    condition.parsing = True
    infinite_check(message.from_user.id)


@bot.message_handler(commands=['parse'], func=lambda message: condition.parsing)
def chill(message):
    bot.send_message(message.from_user.id, config.parse_when_parsing_message)


@bot.message_handler(func=lambda message: condition.waiting_for_link_to_parse)
def chill(message):
    bot.send_message(message.from_user.id, config.got_a_link_to_parse_message)
    condition.waiting_for_link_to_parse = False
    condition.have_a_link = True
    config.url = message.text
    condition.parsing = True
    scan()
    infinite_check(message.from_user.id)


@bot.message_handler(commands=['stop'], func=lambda message: condition.parsing)
def stop(message):
    condition.parsing = False
    bot.send_message(message.from_user.id, config.end_message)


@bot.message_handler(commands=['stop'], func=lambda message: not condition.parsing)
def stop(message):
    bot.send_message(message.from_user.id, config.end_without_start_message)


def scan():
    global ads_id
    ads_id = set()
    ads = html.fromstring(requests.get(config.url, headers=config.headers).text).findall('.//div[@data-marker="item"]')
    for ad in ads:
        ad_id = ad.get('data-item-id')
        ads_id.add(ad_id)


def parse(user):
    ads = html.fromstring(requests.get(config.url, headers=config.headers).text).findall('.//div[@data-marker="item"]')
    while condition.parsing:
        for ad in ads:
            if not condition.parsing:
                return
            # гады из avito иногда меняют эти пути, так что в случае чего - в первую очередь проверяем их
            ad_id = ad.get('data-item-id')
            title = ad.find('.//h3[@itemprop="name"]').text
            link = ad.find('.//a[@itemprop="url"]').get('href')
            price = ad.find('.//meta[@itemprop="price"]').get('content')
            # гады из avito иногда меняют эти пути, так что в случае чего - в первую очередь проверяем их
            if ad_id in ads_id:
                return
            else:
                ads_id.add(ad_id)
                keyboard = types.InlineKeyboardMarkup()
                url_button = types.InlineKeyboardButton(text="Посмотреть объявление", url="https://www.avito.ru" + link)
                keyboard.add(url_button)
                bot.send_message(user, title + "\nЦена: " + price, reply_markup=keyboard)
        ads = html.fromstring(requests.get(config.url, headers=config.headers).text).findall(
            './/div[@data-marker="item"]')


@async_dec()
def infinite_check(user):
    while condition.parsing:
        parse(user)
        time.sleep(30)


bot.infinity_polling()
