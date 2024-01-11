# REAL TIME VEHICLE AND CONTAINER DETECTION SYSTEM
## Status: Developing
This project take video streams and perform truck detection, plate and container's codes OCR by using Yolov5 models.

In its current state, the project only serves as a proof-of-concept only, so the efficiency and error rate for object detections are questionable.

Plan for improvements:
- Improve all Yolo model, or converting it to the newest Yolo version
- Improve GUI performance, the current GUI is running at 1 fps
- Improve overall code structure to allow better data transfer from object detection part to GUI
- Improve stability and robustness as the current program will not responding due to infinite while loop when the video stream stopped or interrupted
## How to run
### Installing libraries
All required modules have been listed in the requirements.txt folder in root directory.
To install them with pip:
```
pip install -r requirements.txt
```