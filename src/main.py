# import sys
# import threading
# import cv2
# import datetime
# import pathlib
# import os
# # sys.path.append('src\input_handler')
# from input_handler.get_images import load_images_from
# # sys.path.append('src\output_handler')
# from output_handler import save_image
# from detection_models import plate_to_text
# from utils_ import my_utils
# # from my_gui import gui_
import os
import sys
from controller import controller

# # Defining all types of yolo models
# PLATE_REGION = 0
# PLATE_OCR = 1

# CURRENT_WORKING_DIRECTORY = pathlib.Path.cwd()

# def process_on_folder(folder_path : str, models : dict, iteration_limits : int):
#     all_images_file_name = load_images_from(folder_path)

#     counter = 0
#     for image_file_name in all_images_file_name:
#         # Processing for one image
#         result = plate_to_text.detect(cv2.imread(image_file_name), models[PLATE_REGION], models[PLATE_OCR])
#         # No plate detected, continue to next image
#         if result is None:
#             continue
#         # Saving results
#         folder_name = '{date: %d-%m-%Y_%H-%M-%S}'.format(date = datetime.datetime.now())
#         path = os.path.join(CURRENT_WORKING_DIRECTORY, 'saved_images', '{date: %d-%m-%Y}'.format(date = datetime.datetime.now()))
#         save_image.save_one_image(result[0], path)
#         # Counting
#         counter+=1
#         # Break after exceeding iteration limits
#         if (counter > iteration_limits):
#             break
#     print("\n {} of {} images have detected objects".format(counter, len(all_images_file_name)))

# def process_on_video(video_path : str, models : dict):
#     video_stream = cv2.VideoCapture(video_path)
#     while video_stream.isOpened():
#         flag, frame = video_stream.read()
#         if not flag:
#             break
#         result = plate_to_text.detect(frame, models[PLATE_REGION], models[PLATE_OCR])
#         # If no plate is detected, then display the original frame
#         # Displaying frame
#         cv2.imshow('Frame', result[0]) 
#         # Press Q on keyboard to exit 
#         if cv2.waitKey(20) & 0xFF == ord('q'): 
#             break
#     video_stream.release()

# def process_on_stream(stream_url : str, window_name : str, models : dict):
#     video_stream = cv2.VideoCapture(stream_url)
#     while video_stream.isOpened():
#         flag, frame = video_stream.read()
#         if not flag:
#             break
#         result = plate_to_text.detect(frame, models[PLATE_REGION], models[PLATE_OCR])
#         # If no plate is detected, then display the original frame
#         # Displaying frame
#         cv2.imshow('Frame', result[0]) 
#         # Press Q on keyboard to exit 
#         if cv2.waitKey(20) & 0xFF == ord('q'): 
#             break
#     video_stream.release()

# # Define class for the camera thread.
# class Master_stream_thread(threading.Thread):

#     def __init__(self, stream_name, stream_url, models : dict, truck_detected : threading.Event):
#         threading.Thread.__init__(self)
#         self.stream_name = stream_name
#         self.stream_url = stream_url
#         self.models = models
#         self.truck_detected = truck_detected


#     def run(self):
#         print("Starting " + self.stream_name)
#         self.launch_stream()

#     def launch_stream(self):
#         cv2.namedWindow(self.stream_name)
#         cam = cv2.VideoCapture(self.stream_url)
#         # gui_.launch_gui(self.truck_detected)
#         if cam.isOpened():
#             rval, frame = cam.read()
#         else:
#             rval = False

#         while rval:
#             result = plate_to_text.detect(frame, self.models[PLATE_REGION], self.models[PLATE_OCR])
#             if result is not None:
#                 print("Truck detected \n")
#                 # If a truck is detected, set event's internal flag to true -> let the supporting threads call the model
#                 self.truck_detected.set()
#             else:
#                 print("No truck \n")
#                 self.truck_detected.clear()
#             cv2.imshow(self.stream_name, frame)
#             rval, frame = cam.read()
#             key = cv2.waitKey(20)
#             if key == 27:  # Press ESC to exit/close each window.
#                 break
#         cv2.destroyWindow(self.stream_name)

# # Define class for the camera thread.
# class Support_stream_thread(threading.Thread):

#     def __init__(self, stream_name, stream_url, models : dict, truck_arrive : threading.Event):
#         threading.Thread.__init__(self)
#         self.stream_name = stream_name
#         self.stream_url = stream_url
#         self.models = models
#         self.truck_detected = truck_arrive

#     def run(self):
#         print("Starting " + self.stream_name)
#         self.launch_stream()

#     def launch_stream(self):
#         cv2.namedWindow(self.stream_name)
#         cam = cv2.VideoCapture(self.stream_url)
#         if cam.isOpened():
#            rval, frame = cam.read()
#         else:
#             rval = False

#         while rval:
#             if self.truck_detected.is_set() is True:
#                 # If truck is detected, then call the model, if not, continue
#                 cv2.rectangle(frame, (0,0), (10, 20), (0, 0, 255), -1)
#                 # result = plate_to_text.detect(frame, self.models[PLATE_REGION], self.models[PLATE_OCR])
#             cv2.imshow(self.stream_name, frame)
#             rval, frame = cam.read()
#             key = cv2.waitKey(20)
#             if key == 27:  # Press ESC to exit/close each window.
#                 break
#         cv2.destroyWindow(self.stream_name)

def main():
    # Getting all images from folder
    # all_images_file_name = load_images_from(r"E:\Internship\Common_resources\TV6-1.v1i.yolov5pytorch\train\images")
    # all_images_file_name = load_images_from(r"E:\Internship\Common_resources\easyscale-front-top-cw.v12i.yolov5pytorch\test\images")
    # all_images_file_name = load_images_from(r"D:\Download\Sample collector\images")

    # # Truck detected event
    # truck_detected = threading.Event()
    # truck_detected.clear()
    # # Setup models
    # models = {}
    # models[PLATE_REGION] = my_utils.setup_yolo_model("yolov5", r"weights\best_plate_5l.pt")
    # models[PLATE_OCR] = my_utils.setup_yolo_model("yolov5", r"weights\best_character_10e.pt")
    # # process_on_folder(r"D:\Download\Sample collector\images", models, 100)
    # # process_on_video(r"C:\Users\Asus\Videos\Captures\Photos 2023-12-21 14-52-11.mp4", models)
    # # process_on_stream(r"rtsp://admin:A@12345678@172.16.17.111:554/media/video2&172.16.17.111:80/LAPI/V1.0/Channels/1", "test", models)
    # # thread2 = CamThread("Back plate", r"rtsp://admin:A@12345678@172.16.17.112:554/media/video2&172.16.17.112:80/LAPI/V1.0/Channels/1", models)
    # # thread3 = CamThread("Back container", r"rtsp://admin:A@12345678@172.16.17.117:554/media/video2&172.16.17.117:80/LAPI/V1.0/Channels/1", models)
    # support_threads = []
    # support_threads.append(Support_stream_thread("Back plate", r"E:\Recordings\Screen Recordings\2023-10-30 13-01-56.mkv", models, truck_detected))
    # # support_threads.append(Support_stream_thread("Back plate", r"rtsp://admin:A@12345678@172.16.17.112:554/media/video2&172.16.17.112:80/LAPI/V1.0/Channels/1", models, truck_detected))
    # # support_threads.append(Support_stream_thread("Back container", r"rtsp://admin:A@12345678@172.16.17.117:554/media/video2&172.16.17.117:80/LAPI/V1.0/Channels/1", models, truck_detected))

    # # master_thread = Master_stream_thread("Front plate", r"rtsp://admin:A@12345678@172.16.17.111:554/media/video2&172.16.17.111:80/LAPI/V1.0/Channels/1", models, truck_detected)
    # master_thread = Master_stream_thread("Front plate", r"E:\Recordings\Screen Recordings\2023-12-22 10-32-05.mkv", models, truck_detected)
    # master_thread.start()

    # for thread in support_threads:
    #     thread.start()
    stream_names = ['FRONT', 'BACK', 'CON1', 'CON2']
    stream_urls = []
    stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.111:554/media/video2&172.16.17.111:80/LAPI/V1.0/Channels/1")
    stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.112:554/media/video2&172.16.17.112:80/LAPI/V1.0/Channels/1")
    stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.117:554/media/video2&172.16.17.117:80/LAPI/V1.0/Channels/1")
    stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.117:554/media/video2&172.16.17.117:80/LAPI/V1.0/Channels/1")
    # stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.114:554/media/video2&172.16.17.114:80/LAPI/V1.0/Channels/1/Media/Video/Streams/0/Snapshot")
    # stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.114:554/media/video2&172.16.17.114:80/LAPI/V1.0/Channels/1/Media/Video/Streams/0/Snapshot")
    # stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.114:554/media/video2&172.16.17.114:80/LAPI/V1.0/Channels/1/Media/Video/Streams/0/Snapshot")
    # stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.114:554/media/video2&172.16.17.114:80/LAPI/V1.0/Channels/1/Media/Video/Streams/0/Snapshot")
    # stream_urls.append(r"E:\Recordings\Screen Recordings\2023-12-28 15-27-35.mkv")
    # stream_urls.append(r"E:\Recordings\Screen Recordings\2023-12-28 15-27-35.mkv")
    # stream_urls.append(r"E:\Recordings\Screen Recordings\2023-12-28 15-27-35.mkv")
    # stream_urls.append(r"E:\Recordings\Screen Recordings\2023-12-28 15-27-35.mkv")
    new_app = controller.Controller(stream_names, stream_urls)
    print("Exiting...\n")
    os._exit(1)

if __name__ == "__main__":
    main()