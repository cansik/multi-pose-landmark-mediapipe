from argparse import ArgumentParser

import cv2
import numpy as np


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

