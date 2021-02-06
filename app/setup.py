import re
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
import codigo

global bot
global TOKEN 
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():

    # Obtém mensagem em JSON e a transforma em um objeto Telegram

    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat_id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()

    if text == "/start":

        bot_welcome = """

        Bem vindo ao assistente de composições analíticas da SEDUC, digite o código desejado. Tabelas disponíveis: Sinapi DEZ/2020 e Composições SEDUC"""

        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    else:
        try:
            text = text.upper()

            if text in codigo.SINAPI:
                answer = codigo.SINAPI[text]          
            else:
                answer = "Código não encontrado"
            bot.sendMessage(chat_id=chat_id, text=answer, reply_to_message_id=msg_id)
            

        except Exception:

            bot.sendMessage(chat_id=chat_id, text="""Código não encontrado nas tabelas de referência SINAPI DEZ/20 e COMP SEDUC, tente novamente. Ex: Sinapi 93281, COMP 001""", reply_to_message_id=msg_id)

    return "ok"

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "Webhook setup was successful"
    else:
        return "Webhook setup failed"

@app.route('/')
def index():
    return '.'
if __name__ == '__main__':
    app.run(threaded=True)

