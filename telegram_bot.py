# -*- coding: utf-8 -*-

'''
Dev Patrick Ferro Ribeiro
Jun 15 2019

Bot Dungeon Master For Telegram
'''

import json
import requests
import schedule
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from emoji import emojize
from random import randint

#Config
TOKEN = "TOKEN_BOT"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
CHAT_ID = GROUP_ID
CHAT_ID_ROOT = ADMIN_ID

#Emojis
EMOJI_INFO = emojize(':information_source:', use_aliases=True)

#APIs Integration
API1 = "https://economia.awesomeapi.com.br/all/USD-BRL,EUR-BRL,BTC-BRL,ETH-BRL"
API3 = "http://apiadvisor.climatempo.com.br/api/v1/weather/locale/6993/current?token=TOKEN"
API4 = "https://newsapi.org/v2/top-headlines?sources=google-news-br&apiKey=TOKEN"

#Requisition to telegram URL
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

#Convert content response to json
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

#Convert content response to json for APIs
def get_api_response(url):
    js = get_json_from_url(url)
    return js

#Conection to receive new messages
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

#Return number of last id
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

#Return last message and id_user or id_group
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

#Generate randon message
def get_messages(number):
    return {
        1: "O lar é o reflexo do coração, um reflexo que vocês estão começando a entender.",
        2: "Algumas vezes o melhor jeito de convencer alguém que está errado é deixá-lo seguir seu caminho.",
        3: "Quando tudo parecer perdido, procure o que reflete o que são e aquilo que mais desejam.",
        4: "A cada ato de bravura, vocês crescerão mais e mais e serão recompensados a tempo",
        5: "As pessoas podem ser muitas coisas. Às vezes o seu pior inimigo pode ser o seu maior aliado.",
        6: "Aqueles que experimentam o poder uma vez nunca mais serão os mesmos.",
        7: "Não é importante a rapidez com que se aprende, mas que se aprenda.",
        8: "Uma pequena boa ação pode levar a uma grande recompensa.",
        9: "Todas as coisas são possíveis para os que têm o coração livre da maldade."
    }.get(number, 'Saudações, jovens pupilos.')

#Requisition to money API and return message
def get_money_api_requisition():
    js = get_api_response(API1)
    if len(js["USD"]) > 0:
        response_text = EMOJI_INFO + " Câmbio \n" + js["USD"]["code"] + " - R$: {0:.2f}\n".format(float(js["USD"]["bid"].replace(',', '.')))
    if len(js["EUR"]) > 0:
        response_text += js["EUR"]["code"] + " - R$: {0:.2f}\n".format(float(js["EUR"]["bid"].replace(',', '.')))
    if len(js["BTC"]) > 0:
        response_text += js["BTC"]["code"] + ' - R$: ' + js["BTC"]["bid"] + "\n"
    if len(js["ETH"]) > 0:
        response_text += js["ETH"]["code"] + ' - R$: ' + js["ETH"]["bid"] + "\n"
    return response_text

#Requisition to weather API and return message
def get_weather_api_requisition():
    js = get_api_response(API3)
    response_text = EMOJI_INFO + " Clima Em " + js["name"] + " " + js["state"] + "\nCondição: " + js["data"]["condition"] + "\nTemperatura: {}°C \nSensação: {}°C \nHumidade: {}% \nVento: {}km/h".format(js["data"]["temperature"], js["data"]["sensation"], js["data"]["humidity"], js["data"]["wind_velocity"])
    return response_text

#Requisition to news API and return top 5 articles
def get_news_api_requisition():
    js = get_api_response(API4)
    send_message_day(EMOJI_INFO + " Top 5 Notícias No Brasil")
    for index, article in enumerate(js["articles"]):
        if index >= 5:
            break
        else:
            send_message_day(article["url"])

#Verify comand to response
def messages(x):
    return {
        '/frases': get_messages(randint(1,9)),
        '/clima': get_weather_api_requisition(),
        '/moedas': get_money_api_requisition(),
        '/saudacao': "Saudações, jovens pupilos",
        '/sobre': "https://riberman.github.io/"
    }.get(x, 'Desculpe, não entendi seu comando meu caro.')

#Send message to chat_id
def send_message(text, chat_id):
    text = messages(text.lower())
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

#Send message to main group_id
def send_message_day(text):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, CHAT_ID)
    get_url(url)

#Verify and send message to chat_id or group if is root
def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            if update["message"]["chat"]["id"] == CHAT_ID_ROOT:
                send_message_day(text)
            else:
                send_message(text, chat)
        except Exception as e:
            print(e)

#Messages in week
def get_monday():
    msg = "Bom dia Pessoal, tenham todos uma ótima semana."
    send_message_day(msg)


def get_tuesday():
    msg = "Bom dia, boa terça-feira."
    send_message_day(msg)


def get_wednesday():
    msg = "Bom dia Pessoal, é meio da semana, estamos quase lá, bom trabalho."
    send_message_day(msg)


def get_thursday():
    msg = "Bom dia, já estou sentido a presença do final de semana."
    send_message_day(msg)


def get_friday():
    msg = "Bom dia Pessoal, espero que tenham tido uma semana produtiva, e se não tiveram, vocês possuem apenas 15h e 59min para isso. Vamos Lá..."
    send_message_day(msg)


def get_friday_two():
    msg = "Um ótimo final de semana a todos, e bom descanço.\nNos vemos segunda novamente."
    send_message_day(msg)

#Schedule jobs
schedule.every().monday.at("08:00").do(get_monday)
schedule.every().monday.at("08:10").do(get_news_api_requisition)
schedule.every().tuesday.at("08:00").do(get_tuesday)
schedule.every().tuesday.at("08:10").do(get_news_api_requisition)
schedule.every().wednesday.at("08:00").do(get_wednesday)
schedule.every().wednesday.at("08:10").do(get_news_api_requisition)
schedule.every().thursday.at("08:00").do(get_thursday)
schedule.every().thursday.at("08:10").do(get_news_api_requisition)
schedule.every().friday.at("08:00").do(get_friday)
schedule.every().friday.at("08:10").do(get_news_api_requisition)
schedule.every().friday.at("18:00").do(get_friday_two)
schedule.every().saturday.at("10:00").do(get_news_api_requisition)
schedule.every().sunday.at("10:00").do(get_news_api_requisition)
#End messages week

#Main to execute all
def main():
    last_update_id = None
    while True:
        schedule.run_pending()
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(1)


if __name__ == '__main__':
    main()
