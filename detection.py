import argparse
import math

import cv2
import mediapipe as mp

from mpx.pose_detection import PoseDetection
from utils import add_default_args, get_video_input


def distance(p1, p2) -> float:
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


def main():
    # read arguments
    parser = argparse.ArgumentParser()
    add_default_args(parser)
    parser.add_argument("--no-smooth-landmarks", action="store_false", help="Disable landmark smoothing.")
    parser.add_argument("--static-image-mode", action="store_true", help="Enables static image mode.")
    args = parser.parse_args()

    # setup camera loop
    mp_drawing = mp.solutions.drawing_utils

    detection = PoseDetection(
        static_image_mode=args.static_image_mode,
        min_detection_confidence=args.min_detection_confidence)

    cap = cv2.VideoCapture(get_video_input(args.input))

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = detection.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.detections:
            for det in results.detections:
                mp_drawing.draw_detection(image, det)

                # Key point 0 - mid hip center
                # Key point 1 - point that encodes size & rotation (for full body)
                # Key point 2 - mid shoulder center
                # Key point 3 - point that encodes size & rotation (for upper body)

                # draw body circle
                mid_hip_center = det.location_data.relative_keypoints[0]
                full_body_info = det.location_data.relative_keypoints[1]

                center = (round(mid_hip_center.x * image.shape[1]), round(mid_hip_center.y * image.shape[0]))
                info = (round(full_body_info.x * image.shape[1]), round(full_body_info.y * image.shape[0]))

                radius = round(distance(center, info))
                cv2.circle(image, center, radius, (0, 0, 255), 1)

        cv2.imshow('MediaPipe Multi Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    detection.close()
    cap.release()


if __name__ == "__main__":
    main()
