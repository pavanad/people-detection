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

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s (%(name)s) %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        filename="logs/people.log",
        filemode="a",
    )
    logger = logging.getLogger(__name__)
    logger.info("Initializing people detection service")

    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        logger.error("Error trying to open the camera")
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
            logger.error(f"{error}")

    cap.release()

    if DEBUG:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
