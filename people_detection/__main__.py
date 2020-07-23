# -*- coding: utf-8 -*-

import logging
import os
import time

import cv2

from config.settings import DEBUG, RTSP_URL
from services.bot import BotTelegram
from services.detection import PeopleDetection
from services.messages import Messages


def main():

    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

    cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        BotTelegram().send_message(Messages.ERROR_CONNECTION)
        return

    people = PeopleDetection()

    while True:
        try:
            ret, frame = cap.read()
            detected = people.detect(frame)

            if DEBUG:
                cv2.imshow("People detect", detected)
                key = cv2.waitKey(1)
                if key == 27:
                    break
        except Exception as error:
            print(f"Error: {error}")
    cap.release()

    if DEBUG:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
