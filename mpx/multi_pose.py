import enum
from typing import NamedTuple

import numpy as np

from mediapipe.calculators.core import constant_side_packet_calculator_pb2
# The following imports are needed because python pb2 silently discards
# unknown protobuf fields.
# pylint: disable=unused-import
from mediapipe.calculators.core import gate_calculator_pb2
from mediapipe.calculators.core import split_vector_calculator_pb2
from mediapipe.calculators.image import warp_affine_calculator_pb2
from mediapipe.calculators.tensor import image_to_tensor_calculator_pb2
from mediapipe.calculators.tensor import inference_calculator_pb2
from mediapipe.calculators.tensor import tensors_to_classification_calculator_pb2
from mediapipe.calculators.tensor import tensors_to_detections_calculator_pb2
from mediapipe.calculators.tensor import tensors_to_landmarks_calculator_pb2
from mediapipe.calculators.tensor import tensors_to_segmentation_calculator_pb2
from mediapipe.calculators.tflite import ssd_anchors_calculator_pb2
from mediapipe.calculators.util import detections_to_rects_calculator_pb2
from mediapipe.calculators.util import landmarks_smoothing_calculator_pb2
from mediapipe.calculators.util import local_file_contents_calculator_pb2
from mediapipe.calculators.util import logic_calculator_pb2
from mediapipe.calculators.util import non_max_suppression_calculator_pb2
from mediapipe.calculators.util import rect_transformation_calculator_pb2
from mediapipe.calculators.util import thresholding_calculator_pb2
from mediapipe.calculators.util import visibility_smoothing_calculator_pb2
from mediapipe.framework.tool import switch_container_pb2
# pylint: enable=unused-import

from mediapipe.python.solutions import download_utils
# pylint: disable=unused-import
from mediapipe.python.solutions.pose_connections import POSE_CONNECTIONS

# pylint: enable=unused-import
from mpx.solution_base import SolutionBase

BINARYPB_FILE_PATH = 'mediapipe/modules/pose_landmark/multi_pose_landmark_cpu.binarypb'


class MultiPose(SolutionBase):

    def __init__(self,
                 static_image_mode=False,
                 model_complexity=1,
                 smooth_landmarks=True,
                 enable_segmentation=False,
                 smooth_segmentation=True,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        super().__init__(
            binary_graph_path=BINARYPB_FILE_PATH,
            side_inputs={

            },
            calculator_params={
            })

        def process(self, image: np.ndarray) -> NamedTuple:
            results = super().process(input_data={'image': image})
            return results
