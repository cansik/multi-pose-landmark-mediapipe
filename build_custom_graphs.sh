#!/bin/bash

# todo: fill in your directories
mediapipe_dir=""
mp_pose_dir=""

if test -f "config.sh"; then
    source config.sh
fi

pushd () {
    command pushd "$@" > /dev/null
}

popd () {
    command popd "$@" > /dev/null
}


# copy adapted graph file
pushd $mediapipe_dir
echo "copy pbtxts and BUILD configs..."
cp -f $mp_pose_dir/graphs/pose_landmark/*.pbtxt "mediapipe/modules/pose_landmark"
cp -f "$mp_pose_dir/graphs/pose_landmark/BUILD" "mediapipe/modules/pose_landmark/BUILD"

cp -f $mp_pose_dir/graphs/pose_detection/*.pbtxt "mediapipe/modules/pose_detection"
cp -f "$mp_pose_dir/graphs/pose_detection/BUILD" "mediapipe/modules/pose_detection/BUILD"

# build all binarypbs
echo "build..."
bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 --copt -DMESA_EGL_NO_X11_HEADERS --copt -DEGL_NO_X11 mediapipe/modules/pose_detection:pose_detection_cpu
bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 --copt -DMESA_EGL_NO_X11_HEADERS --copt -DEGL_NO_X11 mediapipe/modules/pose_detection:pose_detection_with_roi_cpu
bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 --copt -DMESA_EGL_NO_X11_HEADERS --copt -DEGL_NO_X11 mediapipe/modules/pose_landmark:multi_pose_landmark_cpu

popd

# check error
if [[ $? -ne 0 ]] ; then
	echo "something went wrong!"
    exit 1
fi

# copy all bp's back
echo "copy binarypb back..."
pushd "$mediapipe_dir/bazel-bin/mediapipe/modules"
cp -f pose_detection/*.binarypb "$mp_pose_dir/mediapipe/modules/pose_detection"
cp -f pose_landmark/*.binarypb "$mp_pose_dir/mediapipe/modules/pose_landmark"
popd

echo "done!"
exit 0