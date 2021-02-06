from settings import *
import os
import re
from flask import Flask, request
import telegram
import codigo


global bot
global TOKEN 

TOKEN = os.getenv("bot_token")
URL = os.getenv("URL")
bot = telegram.Bot(token=TOKEN)

server = Flask(__name__)


@server.route('/{}'.format(TOKEN), methods=['POST'])
def respond():

    # Obtém mensagem em JSON e a transforma em um objeto Telegram
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat_id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    bot_reply = ""

    if text == "/start":
        bot_reply = """Bem vindo ao assistente de composições analíticas da
        SEDUC, digite o código desejado. Tabelas disponíveis: Sinapi DEZ/2020
        e Composições SEDUC"""
    else:
        try:
            text = text.upper()

            if text in codigo.SINAPI:
                bot_reply = codigo.SINAPI[text]
            else:
                bot_reply = "Código não encontrado"

        except Exception:
            bot_reply = """Código não encontrado nas tabelas de referência
            SINAPI DEZ/20 e COMP SEDUC, tente novamente. Ex: Sinapi 93281, COMP 001"""

    bot.sendMessage(chat_id=chat_id, text=bot_reply, reply_to_message_id=msg_id)

    return "ok"


@server.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "Webhook setup was successful"
    else:
        return "Webhook setup failed"


@server.route('/')
def index():
    return '.'
if __name__ == '__main__':
    server.run(threaded=True)

