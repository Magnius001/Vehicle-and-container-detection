import cv2
from object_detection.plate_detect import detect

image = cv2.imread("E:\Internship\Common_programs\Sample collector 2\images\INA4_231215105249_FRONT.png")
for element in detect(image, "yolov5", "E:/Internship/ML_test/yolov5/runs/train/exp20/weights/best.pt"):
    cv2.imshow('img', element)
    cv2.waitKey(0)
