import time
from argparse import ArgumentParser

import cv2
import numpy as np


def draw_opac_rect(image, x, y, w, h):
    sub_img = image[y:y + h, x:x + w]
    white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255
    res = cv2.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)
    image[y:y + h, x:x + w] = res


def draw_pose_rect(image, rect, color=(255, 0, 255), thickness=2):
    image_width = image.shape[1]
    image_height = image.shape[0]

    world_rect = [(rect.x_center * image_width, rect.y_center * image_height),
                  (rect.width * image_width, rect.height * image_height),
                  rect.rotation]

    box = cv2.boxPoints(world_rect)
    box = np.int0(box)
    cv2.drawContours(image, [box], 0, color, thickness)


def get_video_input(input_value):
    if input_value.isnumeric():
        print("using camera %s as input device..." % input_value)
        return int(input_value)

    print("using video '%s' as input..." % input_value)
    return input_value


class TimeInstrument:
    def __init__(self):
        self._start_time = 0
        self._end_time = 0

        self.fps = 0
        self.latency = 0

    def start(self):
        self._start_time = time.time()

    def stop(self):
        prev = self._end_time
        self._end_time = time.time()

        self.fps = 1.0 / (self._end_time - prev)
        self.latency = self._end_time - self._start_time

    def reset(self):
        self._start_time = 0
        self._end_time = 0
        self.fps = 0
        self.latency = 0
