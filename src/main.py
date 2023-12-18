import sys
import cv2
import datetime

sys.path.append('src\object_detection')
from object_detection.plate_detect import *

sys.path.append('src\input_handler')
from input_handler.get_images import load_images_from

sys.path.append('src\output_handler')
from output_handler.save_image import *

CURRENT_WORKING_DIRECTORY = pathlib.Path.cwd()

def main():
    # Getting all images from folder
    all_images_file_name = load_images_from(r"E:\Internship\Common_resources\TV6-1.v1i.yolov5pytorch\train\images")
    model = setup_model("yolov5", "weights/best_plate.pt")
    i = 0
    # print(os.path.join(CURRENT_WORKING_DIRECTORY, "hello"))
    # Processing all image in folder
    for image_file_name in all_images_file_name:
        # Processing for one image
        classified_images = detect(cv2.imread(image_file_name), model)
        if len(classified_images) < 1:
            continue
        # Saving results
        folder_name = '{date: %d-%m-%Y_%H-%M-%S}'.format(date = datetime.datetime.now())
        # path = os.path.join(CURRENT_WORKING_DIRECTORY, '{date: %d-%m-%Y}'.format(date = datetime.datetime.now()), folder_name)
        path = os.path.join(CURRENT_WORKING_DIRECTORY, 'saved_images', '{date: %d-%m-%Y}'.format(date = datetime.datetime.now()))
        save_classified_images(classified_images, path)
        # Counting
        i+=1
        # Break after 400 loops
        if (i > 50):
            break
    print("\n {} of {} images have detected objects".format(i, len(all_images_file_name)))

if __name__ == "__main__":
    main()