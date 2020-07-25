# -*- coding: utf-8 -*-

import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = False

CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
RTSP_URL = os.getenv("RTSP_URL")

# set true USE_ROI if you want to use
# a region of interest for the camera

USE_ROI = True

COORD_ROI = {
    "camera1": {
        "x": 0,
        "y": 25,
        "width": 250,
        "height": 214
    }
}