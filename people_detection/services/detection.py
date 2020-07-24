# -*- coding: utf-8 -*-

from datetime import datetime

import cv2
import imutils
import numpy as np
from imutils.object_detection import non_max_suppression
from numpy.core.numeric import ndarray

from config.settings import COORD_ROI, USE_ROI

from .bot import BotTelegram


class PeopleDetection:

    SCALE = 1.05
    PADDING = (8, 8)
    WIN_STRIDE = (4, 4)

    MIN_WIDTH = 400
    MIN_DETECT_FRAMES = 10
    MIN_NOTIFICATION_SECONDS = 60

    def __init__(self):
        self.__frame = None
        self.__original = None
        self.__detect_counter = 0
        self.__bot = BotTelegram()
        self.__hog = self.__get_hog_linear_svm()
        self.__last_notification = datetime.now()

    def __get_hog_linear_svm(self) -> cv2.HOGDescriptor:
        """ Initialize the HOG descriptor/person detector. """
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        return hog

    def __apply_nms(self, rects: ndarray) -> ndarray:
        """ Apply non-maxima suppression to the bounding boxes using a
        fairly large overlap threshold to try to maintain overlapping
        boxes that are still people.
        """
        rects_nm = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects_nm, probs=None, overlapThresh=0.65)
        return pick

    def __draw_boxes(self, pick: ndarray):
        """ Draw the original bounding boxes. """
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(self.__frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

    def __detect_people(self):
        """ Detect people in the image. """

        if self.__frame is None:
            return

        timestamp = datetime.now()
        (rects, weights) = self.__hog.detectMultiScale(
            self.__frame,
            winStride=self.WIN_STRIDE,
            padding=self.PADDING,
            scale=self.SCALE,
        )
        if not len(rects):
            return

        pick = self.__apply_nms(rects)
        self.__draw_boxes(pick)

        # check to see if enough time has passed between notifications
        diff_time = timestamp - self.__last_notification
        if diff_time.seconds >= self.MIN_NOTIFICATION_SECONDS:
            self.__detect_counter += 1
            if self.__detect_counter >= self.MIN_DETECT_FRAMES:
                self.__detect_counter = 0
                self.__last_notification = timestamp
                self.__bot.send_photo(self.__original)

    def __get_roi(self, frame):
        """ Get the region of interest of the camera. """
        coord = COORD_ROI.get("camera1")
        return frame[
            coord["y"] : coord["y"] + coord["height"],
            coord["x"] : coord["x"] + coord["width"],
        ]

    def set_frame(self, frame: ndarray):
        """ Set frame and get roi of the camera. """
        self.__frame = self.__get_roi(frame) if USE_ROI else frame
        self.__original = imutils.resize(frame, width=self.MIN_WIDTH)

    def detect(self, frame: ndarray = None):
        """ Initialize detect people. """

        if frame is not None:
            self.set_frame(frame)

        self.__detect_people()
        return self.__frame
