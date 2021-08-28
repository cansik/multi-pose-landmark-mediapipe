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

### About
Based on [mediapipe-osc](https://github.com/cansik/mediapipe-osc/).