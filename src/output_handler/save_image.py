import os
import pathlib
import time
import cv2

def save_classified_images(classified_images: list, folder_path:str) -> bool:
    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
    # print(type(classified_images))
    for element in classified_images:
        file_path = os.path.join(folder_path, f"{element[1]}_{round(time.time() * 1000)}.jpg")
        flag = cv2.imwrite(file_path, element[0])
        print(flag, '\n')
        return flag
