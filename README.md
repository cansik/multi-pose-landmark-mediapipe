# Multi Pose MediaPipe
[MediaPipe](https://google.github.io/mediapipe/) multi pose detection example.

### Install & Run

Currently, this is only tested on Windows and MacOS. It's recommended to use Python3 (`>3.7`) and a virtual environment.

```bash
python install -r requirements.txt
```

To run an example use the basic python command to start up the script.

```bash
# start pose detection with webcam
python pose.py

# start pose detection with video
python pose.py --input yoga.mp4
```

### How to build pbbinary

```
sudo apt update && sudo apt install bazel-3.7.2
sudo ln -s /usr/bin/bazel-3.7.2 /usr/bin/bazel
```

```
sudo apt install python3-pip
pip install numpy
```

```
sudo apt-get install libegl1-mesa-dev
```

```
bazel build -c opt --copt -DMESA_EGL_NO_X11_HEADERS --copt -DEGL_NO_X11 mediapipe/modules/pose_detection:pose_detection_cpu
```

### About
Based on [mediapipe-osc](https://github.com/cansik/mediapipe-osc/).