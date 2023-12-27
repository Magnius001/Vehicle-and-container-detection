# Define class for the camera thread.
import threading
import cv2

from src import plate_to_text



# Defining all types of yolo models
PLATE_REGION = 0
PLATE_OCR = 1

class Master_stream_thread(threading.Thread):

    def __init__(self, stream_name, stream_url, models : dict, truck_detected : threading.Event):
        threading.Thread.__init__(self)
        self.stream_name = stream_name
        self.stream_url = stream_url
        self.models = models
        self.truck_detected = truck_detected

    def run(self):
        print("Starting " + self.stream_name)
        self.launch_stream()

    def launch_stream(self):
        cv2.namedWindow(self.stream_name)
        cam = cv2.VideoCapture(self.stream_url)
        # gui_.launch_gui(self.truck_detected)
        if cam.isOpened():
            rval, frame = cam.read()
        else:
            rval = False

        while rval:
            result = plate_to_text.detect(frame, self.models[PLATE_REGION], self.models[PLATE_OCR])
            if result is not None:
                print("Truck detected \n")
                # If a truck is detected, set event's internal flag to true -> let the supporting threads call the model
                self.truck_detected.set()
            else:
                print("No truck \n")
                self.truck_detected.clear()
            cv2.imshow(self.stream_name, frame)
            rval, frame = cam.read()
            key = cv2.waitKey(20)
            if key == 27:  # Press ESC to exit/close each window.
                break
        cv2.destroyWindow(self.stream_name)

# Define class for the camera thread.
class Support_stream_thread(threading.Thread):

    def __init__(self, stream_name, stream_url, models : dict, truck_arrive : threading.Event):
        threading.Thread.__init__(self)
        self.stream_name = stream_name
        self.stream_url = stream_url
        self.models = models
        self.truck_detected = truck_arrive

    def run(self):
        print("Starting " + self.stream_name)
        self.launch_stream()

    def launch_stream(self):
        cv2.namedWindow(self.stream_name)
        cam = cv2.VideoCapture(self.stream_url)
        if cam.isOpened():
           rval, frame = cam.read()
        else:
            rval = False

        while rval:
            if self.truck_detected.is_set() is True:
                # If truck is detected, then call the model, if not, continue
                cv2.rectangle(frame, (0,0), (10, 20), (0, 0, 255), -1)
                # result = plate_to_text.detect(frame, self.models[PLATE_REGION], self.models[PLATE_OCR])
            cv2.imshow(self.stream_name, frame)
            rval, frame = cam.read()
            key = cv2.waitKey(20)
            if key == 27:  # Press ESC to exit/close each window.
                break
        cv2.destroyWindow(self.stream_name)
