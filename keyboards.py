import os
import shelve
import time
import telebot
import requests
import socks
import socket
from telebot.types import LabeledPrice, ShippingOption



def keyboard_0():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('Кожные заболевания', 'Зубные заболевания')
    keyboard.row('Глазные заболевания', 'Психологические заболевания')

    return keyboard
