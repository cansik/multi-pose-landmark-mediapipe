import argparse

import cv2
from mediapipe.python.solutions.drawing_utils import DrawingSpec

import mediapipe as mp
from mpx import multi_pose
from utils import get_video_input, draw_pose_rect, TimeInstrument, draw_opac_rect

debug_on = False
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

time_instrument = TimeInstrument()


def sec_len(it):
    if it:
        return len(it)
    else:
        return "-"


def draw_infos(image, pose_count):
    ih, iw = image.shape[:2]
    rw, rh = 290, 20

    # show infos
    draw_opac_rect(image, 0, ih - rh, rw, rh)
    cv2.putText(image, "FPS: %.0f Latency: %.2fms Poses: %s"
                % (time_instrument.fps, time_instrument.latency, pose_count),
                (7, ih - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (55, 55, 55), 1, cv2.LINE_AA)


def detect_and_annotate(pose, mp_drawing, connections, image, flip=False):
    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    if flip:
        image = cv2.flip(image, 1)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    try:
        time_instrument.start()
        results = pose.process(image)
        time_instrument.stop()
    except RuntimeError as ex:
        print(f"Error: ${ex}")
        exit(1)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # annotate landmarks
    if results.multi_pose_landmarks:
        for i, landmarks in enumerate(results.multi_pose_landmarks):
            color = colors[i]
            mp_drawing.draw_landmarks(image, landmarks, connections,
                                      connection_drawing_spec=DrawingSpec(color=color, thickness=2))

    draw_infos(image, sec_len(results.multi_pose_landmarks))

    if debug_on:
        # annotate pose_rects_from_body_detections / pose_rects
        if results.pose_rects:
            for i, rect in enumerate(results.pose_rects):
                draw_pose_rect(image, rect, color=(255, 0, 0))
                cv2.circle(image, (round(rect.x_center * image.shape[1]),
                                   round(rect.y_center * image.shape[0])), 20, (255, 0, 0), 1)

            if results.pose_rects_from_landmarks:
                for i, rect in enumerate(results.pose_rects_from_landmarks):
                    draw_pose_rect(image, rect, color=(0, 255, 0))
                    cv2.circle(image, (round(rect.x_center * image.shape[1]),
                                       round(rect.y_center * image.shape[0])), 20, (255, 0, 0), 1)

        body_detections = results.body_detections
        if body_detections:
            pass

        print(f"prev_pose_rects_from_landmarks: {sec_len(results.prev_pose_rects_from_landmarks)}\t"
              f"body_detections: {sec_len(results.body_detections)}\t"
              f"pose_rects_from_body_detections: {sec_len(results.pose_rects_from_body_detections)}\t"
              f"pose_rects: {sec_len(results.pose_rects)}\t"
              f"multi_pose_landmarks: {sec_len(results.multi_pose_landmarks)}\t"
              f"pose_rects_from_landmarks: {sec_len(results.pose_rects_from_landmarks)}")

    return image


def main():
    # read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="0",
                        help="The video input path or video camera id (device id).")
    parser.add_argument("--model-complexity", default=1, type=int,
                        help="Set model complexity (0=Light, 1=Full, 2=Heavy).")
    parser.add_argument("--no-smooth-landmarks", action="store_false", help="Disable landmark smoothing.")
    parser.add_argument("--static-image-mode", action="store_true", help="Enables static image mode.")
    parser.add_argument("--enable-segmentation", action="store_true", help="Enables segmentation.")
    parser.add_argument("-mdc", "--min-detection-confidence", type=float, default=0.5,
                        help="Minimum confidence value ([0.0, 1.0]) for the detection to be considered successful.")
    parser.add_argument("-mtc", "--min-tracking-confidence", type=float, default=0.5,
                        help="Minimum confidence value ([0.0, 1.0]) to be considered tracked successfully.")
    parser.add_argument("-mst", "--min-similarity-threshold", type=float, default=0.5,
                        help="Min IoU similarity to be the same pose rect.")
    parser.add_argument("--max-num-poses", type=int, default=2, help="Max poses to be detected.")

    parser.add_argument("--image", default=None, type=str, help="Input image path.")

    parser.add_argument("--wait", action="store_true", help="Wait for use input to capture next frame.")
    parser.add_argument("--debug", action="store_true", help="Show debug output.")
    args = parser.parse_args()

    # parse arguments
    flip_input = args.input.isnumeric()

    wait_time = 1
    if args.wait:
        wait_time = None

    global debug_on
    debug_on = args.debug

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
        min_tracking_confidence=args.min_tracking_confidence,
        max_num_poses=args.max_num_poses,
        min_similarity_threshold=args.min_similarity_threshold)

    if args.image:
        # inference on a single image
        image = cv2.imread(args.image)
        image = detect_and_annotate(pose, mp_drawing, connections, image)
        cv2.imshow('MediaPipe Multi Pose', image)
        cv2.waitKey()

        pose.close()
        exit(0)

    cap = cv2.VideoCapture(get_video_input(args.input))

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        image = detect_and_annotate(pose, mp_drawing, connections, image, flip=flip_input)

        cv2.imshow('MediaPipe Multi Pose', image)
        if cv2.waitKey(wait_time) & 0xFF == 27:
            break
    pose.close()
    cap.release()


if __name__ == "__main__":
    main()
