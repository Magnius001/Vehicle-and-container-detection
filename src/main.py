import sys
import cv2
import datetime
import pathlib
import os
# sys.path.append('src\input_handler')
from input_handler.get_images import load_images_from
# sys.path.append('src\output_handler')
from output_handler import save_image
from plate_to_text import plate_to_text
from utils_ import my_utils

# Defining all types of yolo models
PLATE_REGION = 0
PLATE_OCR = 1

CURRENT_WORKING_DIRECTORY = pathlib.Path.cwd()

def process_on_folder(folder_path : str, models : dict, iteration_limts : int):
    all_images_file_name = load_images_from(folder_path)

    counter = 0
    for image_file_name in all_images_file_name:
        # Processing for one image
        result = plate_to_text.detect(cv2.imread(image_file_name), models[PLATE_REGION], models[PLATE_OCR])
        # No plate detected, continue to next image
        if result is None:
            continue
        # Saving results
        folder_name = '{date: %d-%m-%Y_%H-%M-%S}'.format(date = datetime.datetime.now())
        path = os.path.join(CURRENT_WORKING_DIRECTORY, 'saved_images', '{date: %d-%m-%Y}'.format(date = datetime.datetime.now()))
        save_image.save_one_image(result[0], path)
        # Counting
        counter+=1
        # Break after 10 loops
        if (counter > iteration_limts):
            break
    print("\n {} of {} images have detected objects".format(counter, len(all_images_file_name)))

def process_on_video(video_path : str, models : dict):
    video_stream = cv2.VideoCapture(video_path)
    while video_stream.isOpened():
        flag, frame = video_stream.read()
        if not flag:
            break
        result = plate_to_text.detect(frame, models[PLATE_REGION], models[PLATE_OCR])
        # No plate detected, continue to next image
        # if result is None:
        #     continue
        # Displaying frame
        cv2.imshow('Frame', result[0]) 
        # Press Q on keyboard to exit 
        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
    video_stream.release()

def main():
    # Getting all images from folder
    # all_images_file_name = load_images_from(r"E:\Internship\Common_resources\TV6-1.v1i.yolov5pytorch\train\images")
    # all_images_file_name = load_images_from(r"E:\Internship\Common_resources\easyscale-front-top-cw.v12i.yolov5pytorch\test\images")
    all_images_file_name = load_images_from(r"D:\Download\Sample collector\images")

    # Setup models
    models = {}
    models[PLATE_REGION] = my_utils.setup_yolo_model("yolov5", r"weights\best_plate_5l.pt")
    models[PLATE_OCR] = my_utils.setup_yolo_model("yolov5", r"weights\best_character_10e.pt")
    # process_on_folder(r"D:\Download\Sample collector\images", models, 100)
    process_on_video(r"C:\Users\Asus\Videos\Captures\Photos 2023-12-21 14-52-11.mp4", models)

if __name__ == "__main__":
    main()