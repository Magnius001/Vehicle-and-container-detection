from collections import namedtuple
import queue
import threading
from input_handler.get_images import load_images_from
from utils_ import my_utils
from stream_processing import stream_thread
from my_gui import gui_

# Defining all types of yolo models
PLATE_REGION = 0
PLATE_OCR = 1
CONTAINER_1_CODE = 2
CONTAINER_2_CODE = 3
# Defining gui refresh rate
UPDATE_INTERVAL = 15 #ms

# Responsible for controlling the threads, GUI, transfering data from streams to GUI, storing models
class Controller():
    # Initialize the class with a list of camera names and urls, current version only support 4 cams
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
        self.truck_detected = threading.Event()
        # Create single element queue for each cameras
        self.front_cam_buffer = queue.Queue(maxsize=1)
        self.back_cam_buffer = queue.Queue(maxsize=1)
        self.con1_cam_buffer = queue.Queue(maxsize=1)
        self.con2_cam_buffer = queue.Queue(maxsize=1)

        # Create threads to handle multiple camera streams
        self.front_cam = stream_thread.Master_stream_thread(stream_names[0], stream_urls[0], self.models[PLATE_REGION], self.models[PLATE_OCR], self.truck_detected, self.front_cam_buffer)
        self.back_cam = stream_thread.Master_stream_thread(stream_names[1], stream_urls[1], self.models[PLATE_REGION], self.models[PLATE_OCR], threading.Event(), self.back_cam_buffer)
        # self.back_cam = stream_thread.Support_stream_thread(stream_names[1], stream_urls[1], None, self.truck_detected, self.back_cam_buffer)
        self.con1_cam = stream_thread.Support_stream_thread(stream_names[2], stream_urls[2], self.models[CONTAINER_1_CODE], self.truck_detected, self.con1_cam_buffer)
        self.con2_cam = stream_thread.Support_stream_thread(stream_names[3], stream_urls[3], self.models[CONTAINER_2_CODE], self.truck_detected, self.con2_cam_buffer)

        # Start capturing camera streams
        self.front_cam.start()
        self.back_cam.start()
        self.con1_cam.start()
        self.con2_cam.start()

        # Init GUI
        self.app = gui_.App()
        # self.app.bind('<KeyPress>', self.close_gui())
        self.app.after(UPDATE_INTERVAL, self.update_gui)
        self.app.mainloop()
        print("Stopping threads...\n")
        self.front_cam.stop_stream()
        self.back_cam.stop_stream()
        self.con1_cam.stop_stream()
        self.con2_cam.stop_stream()

    # Schedule tasks to run every 50ms, getting data from stream threads and update GUI
    def update_gui(self):
        results = []
        print("Updating...\n")
        if self.front_cam_buffer.qsize != 0:
            results.append(self.front_cam_buffer.get())
        if self.back_cam_buffer.qsize != 0:
            results.append(self.back_cam_buffer.get())
        if self.con1_cam_buffer.qsize != 0:
            results.append(self.con1_cam_buffer.get())
        if self.con2_cam_buffer.qsize != 0:
            results.append(self.con2_cam_buffer.get())
        frames = []
        for result in results:
            frames.append(result[0]) 
        self.app.update_camera_display(frames)

        self.app.update_status(self.truck_detected.is_set())

        if results[0][1] is None:
            self.app.update_plate("")
        else:
            self.app.update_plate(results[0][1])
            
        self.app.after(UPDATE_INTERVAL, self.update_gui)

    def close_gui(self):
        self.app.destroy()