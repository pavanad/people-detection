# -*- coding: utf-8 -*-

import logging
import time

import cv2

from config.settings import RTSP_URL
from services.detection import PeopleDetection


def main():

    people = PeopleDetection()

    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        detected = people.detect(frame)
        cv2.imshow("Social", detected)
        cv2.waitKey(1000)


if __name__ == "__main__":
    main()
