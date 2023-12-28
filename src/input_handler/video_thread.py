import sys
import threading
import cv2
import datetime
import pathlib
import os
# sys.path.append('src\input_handler')
from input_handler.get_images import load_images_from
# sys.path.append('src\output_handler')
from output_handler import save_image
from detection_models import plate_to_text
from utils_ import my_utils

# Defining all types of yolo models
PLATE_REGION = 0
PLATE_OCR = 1

# Define class for the camera thread.
class CamThread(threading.Thread):

    def __init__(self, stream_name, stream_url, models : dict):
        threading.Thread.__init__(self)
        self.previewname = stream_name
        self.camid = stream_url
        self.models = models

    def run(self):
        print("Starting " + self.previewname)
        previewcam(self.previewname, self.camid)

    def previewcam(self):
        cv2.namedWindow(self.stream_name)
        cam = cv2.VideoCapture(self.stream_url)
        if cam.isOpened():
           rval, frame = cam.read()
        else:
            rval = False

        while rval:
            result = plate_to_text.detect(frame, self.models[PLATE_REGION], self.models[PLATE_OCR])
            cv2.imshow(self.stream_name, frame)
            rval, frame = cam.read()
            key = cv2.waitKey(20)
            if key == 27:  # Press ESC to exit/close each window.
                break
        cv2.destroyWindow(self.stream_name)

# Function to preview the camera.
def previewcam(stream_name, stream_url):
    cv2.namedWindow(stream_name)
    cam = cv2.VideoCapture(stream_url)
    if cam.isOpened():
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(stream_name, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # Press ESC to exit/close each window.
            break
    cv2.destroyWindow(stream_name)

# Create different threads for each video stream, then start it.
thread1 = CamThread("Driveway", 'rtsp://username:SuperSecurePassword@192.168.1.2/Streaming/Channels/102')
thread2 = CamThread("Front Door", 'rtsp://username:SuperSecurePassword@192.168.1.2/Streaming/Channels/202')
thread3 = CamThread("Garage", 'rtsp://username:SuperSecurePassword@192.168.1.2/Streaming/Channels/302')
thread1.start()
thread2.start()
thread3.start()