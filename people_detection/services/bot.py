# -*- coding: utf-8 -*-

from io import BytesIO

import cv2
import telegram
from numpy.core.numeric import ndarray

from config.settinfs import CHAT_ID, TELEGRAM_TOKEN


class BotTelegram:
    def __init__(self):
        self.__chat_id = CHAT_ID
        self.__bot = telegram.Bot(token=TELEGRAM_TOKEN)

    def __ndarray_to_buffer(self, photo: ndarray) -> BytesIO:
        _, buffer = cv2.imencode(".jpg", photo)
        return BytesIO(buffer)

    def set_chat_id(self, chat_id: int):
        self.__chat_id = chat_id

    def send_message(self, text: str):
        self.__bot.send_message(chat_id=self.__chat_id, text=text)

    def send_photo(self, photo: ndarray):
        photo_buff = self.__ndarray_to_buffer(photo)
        self.__bot.send_photo(chat_id=self.__chat_id, photo=photo_buff)

    def send_message_and_photo(self, text: str, photo: ndarray):
        self.send_message(text)
        self.send_photo(photo)
