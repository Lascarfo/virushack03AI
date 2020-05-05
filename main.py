import os
import shelve
import time
import telebot
import requests
import socks
import socket


from config import *
from keyboards import *
from functions import *



socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket



stage_machine = {}

bot = telebot.TeleBot(token)

def writeIMG(filename, message):
    fileID = message.photo[-1].file_id
    file = bot.get_file(fileID)
    with open('./test/' + filename, 'wb') as handle:
        response = requests.get('https://api.telegram.org/'
        'file/bot{}/{}'.format(token, file.file_path), stream=True)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

def sendmes(text, id):
    try:
        bot.send_message(id, text, parse_mode='Markdown', reply_markup=keyboard_0())
    except:
        time.sleep(1)
        bot.send_message(id, text, parse_mode='Markdown', reply_markup=keyboard_0())


def send_recomendations_mes(id):
    bot.send_message(id,
                    recomendations1,
                     parse_mode='Markdown')
    time.sleep(1.3)
    bot.send_message(id,
                    recomendations2,
                     parse_mode='Markdown')
    time.sleep(1.3)
    bot.send_message(id,
                    recomendations3,
                     parse_mode='Markdown')
    time.sleep(1.3)
    bot.send_message(id,
                     recomendations4,
                     parse_mode='Markdown')
    time.sleep(1.3)
    bot.send_message(id,
                     recomendations5,
                     parse_mode='Markdown')
    send_photo(id)

def send_photo(id):
    bot.send_chat_action(id, 'upload_photo')
    img = open('sample.jpg', 'rb')
    bot.send_photo(id, img)
    img.close()


def send_welcome_mes(id):
    bot.send_message(id,
                    wlc_msg1,
                     parse_mode='Markdown')
    time.sleep(1.3)
    bot.send_message(id,
                    wlc_msg2,
                     parse_mode='Markdown')
    time.sleep(1.3)
    bot.send_message(id,
                    wlc_msg3,
                     parse_mode='Markdown', reply_markup=keyboard_0())
    time.sleep(1.6)
    bot.send_message(id,
                     wlc_msg4,
                     parse_mode='Markdown')


@bot.message_handler(commands=['start'])
def command_start(message, key=0):
    keyboard = keyboard_0()
    print(message)
    if key == 0:
        send_welcome_mes(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=keyboard)
    stage_machine["{}".format(message.from_user.id)] = "0"





@bot.message_handler(content_types=['text'])
def gotten_message(message):
    if message.text == "Кожные заболевания":
        send_recomendations_mes(message.chat.id)
    elif message.text == "Зубные заболевания":
        bot.send_message(message.chat.id, "Разработка модуля начата.\n"
                                          "В скором времени он будет добавлен в сервис.", reply_markup=keyboard_0())
    elif message.text == "Глазные заболевания":
        bot.send_message(message.chat.id, "Данный модуль находится в разработке.", reply_markup=keyboard_0())
    elif message.text == "Психологические заболевания":
        bot.send_message(message.chat.id, "Данный модуль находится в разработке.", reply_markup=keyboard_0())
    else:
        bot.send_message(message.chat.id, "Неверная команда. Выберете команду из меню.", reply_markup=keyboard_0())




@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        writeIMG("scan.png", message)
        print("scan IMG downloaded...")
        s_message = 'Фотография успешно загружена!\n*Стартовал процесс проверки.*'
        sendmes(s_message, message.chat.id)
        result = check_mole()
        if result == 0:
            sendmes("Анализ завершен.\n\
*Все хорошо!*\n\
Я *не обнаружил* признаков меланомы.\n\
*Не смотря на мою оценку, если Вас беспокоит Ваше состояние,\n\
я рекомендую Вам обратиться в поликлинику*.", message.chat.id)
        elif result == 1:
            sendmes("Анализ завершен.\n\
Рекомендую вам *срочно* проконсультироваться со специалистом по поводу этой родинки!", message.chat.id)
        else:
            sendmes("Не удалось обработать изображение.", message.chat.id)

    except Exception as ex:
        print(ex)
        sendmes('Ошибка во время связи с Telegram API', message.chat.id)


bot.skip_pending = False
bot.polling(none_stop=True)



# if __name__ == "__main__":
#
#     try:
#
#     except:
#      #   print('error: {}'.format(sys.exc_info()[0]))
#         time.sleep(5)