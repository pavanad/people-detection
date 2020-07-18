# -*- coding: utf-8 -*-

import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
from numpy.core.numeric import ndarray


class PeopleDetection:

    SCALE = 1.03
    PADDING = (8, 8)
    WIN_STRIDE = (4, 4)

    def __init__(self):
        self.__frame = None
        self.__hog = self.__get_hog_linear_svm()

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

        if self.__frame is not None:
            (rects, weights) = self.__hog.detectMultiScale(
                self.__frame,
                winStride=self.WIN_STRIDE,
                padding=self.PADDING,
                scale=self.SCALE,
            )
            pick = self.__apply_nms(rects)
            self.__draw_boxes(pick)
            print(f"rects: {len(rects)} | pick: {len(pick)}")

    def set_frame(self, frame: ndarray):
        self.frame = frame

    def detect(self, frame: ndarray = None):
        """ Initialize detect people. """
        if frame is not None:
            self.__frame = frame
        self.__detect_people()
        return self.__frame
