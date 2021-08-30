import argparse

import cv2

import mediapipe as mp
from mpx import multi_pose
from utils import add_default_args, get_video_input


def main():
    # read arguments
    parser = argparse.ArgumentParser()
    add_default_args(parser)
    parser.add_argument("--model-complexity", default=1, type=int,
                        help="Set model complexity (0=Light, 1=Full, 2=Heavy).")
    parser.add_argument("--no-smooth-landmarks", action="store_false", help="Disable landmark smoothing.")
    parser.add_argument("--static-image-mode", action="store_true", help="Enables static image mode.")
    parser.add_argument("--image", default=None, type=str, help="Input image path.")
    args = parser.parse_args()

    # setup camera loop
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = multi_pose

    # fix bug which occurs because draw landmarks is not adapted to upper pose
    connections = mp_pose.POSE_CONNECTIONS

    pose = mp_pose.MultiPose(
        smooth_landmarks=args.no_smooth_landmarks,
        static_image_mode=args.static_image_mode,
        model_complexity=args.model_complexity,
        min_detection_confidence=args.min_detection_confidence,
        min_tracking_confidence=args.min_tracking_confidence)

    if args.image:
        # inference on a single image
        image = cv2.imread(args.image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_pose_landmarks:
            for landmarks in results.multi_pose_landmarks:
                mp_drawing.draw_landmarks(image, landmarks, connections)

        cv2.imshow('MediaPipe Multi Pose', image)
        cv2.waitKey()

        pose.close()
        exit(0)

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
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_pose_landmarks:
            for landmarks in results.multi_pose_landmarks:
                mp_drawing.draw_landmarks(image, landmarks, connections)

        cv2.imshow('MediaPipe Multi Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    pose.close()
    cap.release()


if __name__ == "__main__":
    main()
