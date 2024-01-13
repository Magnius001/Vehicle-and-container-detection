# Define class for the camera thread.
import os
import queue
import threading
import cv2
import time

from detection_models import plate_to_text, code_to_text

class Master_stream_thread(threading.Thread):

    def __init__(self, stream_name, stream_url, plate_region, plate_ocr, truck_detected : threading.Event, buffer: queue.Queue[tuple]):
        threading.Thread.__init__(self)
        self.stream_name = stream_name
        self.stream_url = stream_url
        self.plate_region_model = plate_region
        self.plate_ocr_model = plate_ocr
        self.truck_detected = truck_detected
        self.buffer = buffer
        self.stop_flag = False

    def run(self):
        print("Starting " + self.stream_name)
        self.launch_stream()

    def launch_stream(self):
        cam = cv2.VideoCapture(self.stream_url)
        if cam.isOpened():
            rval, frame = cam.read()
        else:
            rval = False

        while rval:
            result = plate_to_text.detect(frame, self.plate_region_model, self.plate_ocr_model)
            metadata = ''
            if result is not None:
                # If a truck is detected, set event's internal flag to true -> let the supporting threads call the model
                self.truck_detected.set()
                metadata = result[1]
            else:
                self.truck_detected.clear()

            # if not self.buffer.full():
            #     self.buffer.put((frame,metadata))
            try:
                self.buffer.put((frame,metadata), block=False)
            except:
                pass
            time.sleep(0.1)
            rval, frame = cam.read()
            if self.stop_flag is True:
                cam.release()
                os._exit(1)

    def stop_stream(self):
        self.stop_flag = True

# Define class for the camera thread.
class Support_stream_thread(threading.Thread):

    # Support thread only accept one model only
    def __init__(self, stream_name, stream_url, model, truck_arrive : threading.Event, buffer : queue.Queue):
        threading.Thread.__init__(self)
        self.stream_name = stream_name
        self.stream_url = stream_url
        self.model = model
        self.truck_detected = truck_arrive
        self.buffer = buffer
        self.stop_flag = False

    def run(self):
        print("Starting " + self.stream_name)
        self.launch_stream()

    def launch_stream(self):
        # cv2.namedWindow(self.stream_name)
        cam = cv2.VideoCapture(self.stream_url)
        if cam.isOpened():
           rval, frame = cam.read()
        else:
            rval = False

        while rval:
            if self.truck_detected.is_set() is True:
                # If truck is detected, then call the model, if not, continue
                # Visual indicator of truck detected
                cv2.rectangle(frame, (0,0), (10, 20), (0, 0, 255), -1)
                # Calling the model
                result = code_to_text.detect(frame, self.model)
                if result is not None:
                    frame = result[0]
            # if not self.buffer.full():
            #     self.buffer.put((frame,self.stream_name))
            try:
                self.buffer.put((frame,self.stream_name), block=False)
            except:
                pass
            time.sleep(0.1)
            rval, frame = cam.read()
            if self.stop_flag is True:
                cam.release()
                os._exit(1)

    def stop_stream(self):
        self.stop_flag = True