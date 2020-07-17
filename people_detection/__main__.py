# -*- coding: utf-8 -*-

import logging
import os
import time

import cv2
from config.settings import RTSP_URL
from services.detection import PeopleDetection


def main():

    people = PeopleDetection()

    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"    
    cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        return

    while True:        
        ret, frame = cap.read()
        detected = people.detect(frame)
        cv2.imshow("Social", detected)        
        cv2.waitKey(1000)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
