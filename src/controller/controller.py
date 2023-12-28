from collections import namedtuple
import queue
import sys
import threading
import cv2
import datetime
import pathlib
import os
# sys.path.append('src\input_handler')
from input_handler.get_images import load_images_from
# sys.path.append('src\output_handler')
from detection_models import plate_to_text
from utils_ import my_utils
from stream_processing import stream_thread
from my_gui import gui_

# Defining all types of yolo models
PLATE_REGION = 0
PLATE_OCR = 1
CONTAINER_1_CODE = 2
CONTAINER_2_CODE = 3

class Controller():
    def __init__(self, stream_names: list[str], stream_urls: list[str]) -> None:
        # Init yolo models
        self.models = {}
        # Used for getting the plate
        self.models[PLATE_REGION] = my_utils.setup_yolo_model("yolov5", r"weights\best_plate_5l.pt")
        self.models[PLATE_OCR] = my_utils.setup_yolo_model("yolov5", r"weights\best_character_10e.pt")
        # Used for getting the container's code
        self.models[CONTAINER_1_CODE] = my_utils.setup_yolo_model("yolov5", r"weights\code_ocr.pt")
        self.models[CONTAINER_2_CODE] = my_utils.setup_yolo_model("yolov5", r"weights\code_ocr.pt")

        # Creat event flag for when a truck is present in the lane
        self.truck_detected = threading.Event
        self.front_cam_buffer = queue.Queue[tuple]
        self.back_cam_buffer = queue.Queue[tuple]
        self.con1_cam_buffer = queue.Queue[tuple]
        self.con2_cam_buffer = queue.Queue[tuple]

        # Create threads to handle multiple camera streams
        self.front_cam = stream_thread.Master_stream_thread(stream_names[0], stream_urls[0], self.models[PLATE_REGION], self.models[PLATE_OCR], self.truck_detected, self.cam_buffer)
        self.back_cam = stream_thread.Support_stream_thread(stream_names[1], stream_urls[1], None, self.truck_detected, self.back_cam_buffer)
        self.con1_cam = stream_thread.Support_stream_thread(stream_names[2], stream_urls[2], self.models[CONTAINER_1_CODE], self.truck_detected, self.con1_cam_buffer)
        self.con2_cam = stream_thread.Support_stream_thread(stream_names[3], stream_urls[3], self.models[CONTAINER_2_CODE], self.truck_detected, self.con2_cam_buffer)

        # Init GUI
        self.app = gui_.App()
        self.app.after(1000, self.flush_buffer)

    def flush_buffer(self):
        frames = []
        if not self.front_cam_buffer.empty():
            frames.append(self.front_cam_buffer.get())
        if not self.back_cam_buffer.empty():
            frames.append(self.back_cam_buffer.get())
        if not self.con1_cam_buffer.empty():
            frames.append(self.con1_cam_buffer.get())
        if not self.con2_cam_buffer.empty():
            frames.append(self.con2_cam_buffer.get())
        self.app.update_camera_display(frames)
