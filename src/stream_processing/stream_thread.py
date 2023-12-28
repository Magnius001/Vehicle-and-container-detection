# Define class for the camera thread.
import queue
import threading
import cv2

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
            result = plate_to_text.detect(frame, self.plate_region_model, self.plate_ocr_model)
            if result is not None:
                # print("Truck detected \n")
                # If a truck is detected, set event's internal flag to true -> let the supporting threads call the model
                self.truck_detected.set()
                self.buffer.put((result[0],self.stream_name))
            else:
                # print("No truck \n")
                self.truck_detected.clear()
            # cv2.imshow(self.stream_name, frame)
            # rval, frame = cam.read()
            # key = cv2.waitKey(20)
            # if key == 27:  # Press ESC to exit/close each window.
            #     break
        cv2.destroyWindow(self.stream_name)

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
                # Visual indicator of truck detected
                cv2.rectangle(frame, (0,0), (10, 20), (0, 0, 255), -1)
                # Calling the model
                result = code_to_text.detect(frame, self.model, None)
                self.buffer.put((result[0], self.stream_name))
            # cv2.imshow(self.stream_name, frame)
            # rval, frame = cam.read()
            # key = cv2.waitKey(20)
            # if key == 27:  # Press ESC to exit/close each window.
            #     break
        cv2.destroyWindow(self.stream_name)
