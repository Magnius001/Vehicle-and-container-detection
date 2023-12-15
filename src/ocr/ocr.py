import numpy as np
import pytesseract
from pytesseract import Output
import cv2

folderDir = None

# Preprocessing functions
# Grayscale
def get_grayscale(image):
    output = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if not save_image(output, "grayscaled.jpg"):
        print("Unable to save grayscaled image")
    return output

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    output = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    if not save_image(output, "thresholded.jpg"):
        print("Unable to save thresholded image")
    return output

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    output = cv2.dilate(image, kernel, iterations = 1)
    if not save_image(output, "dilated.jpg"):
        print("Unable to save dilated image")
    return output

#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    output = cv2.erode(image, kernel, iterations = 1)
    if not save_image(output, "eroded.jpg"):
        print("Unable to save eroded image")
    return output

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    output = cv2.Canny(image, 100, 200)
    if not save_image(output, "cannied.jpg"):
        print("Unable to save cannied image")
    return output

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    output = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    if not save_image(output, "deskewed.jpg"):
        print("Unable to save deskewed image")
    return output

# #template matching
# def match_template(image, template):
#     return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 

# Save image
def save_image(image, filename):
    return cv2.imwrite(filename, image)

def pytesseract_setup(oem, psm, pytesseract_path):
    pytesseract.pytesseract.tesseract_cmd = pytesseract_path
    return '--oem 3 --psm 12'


def ocr(image, oem, psm, pytesseract_path):
    temp_image = image.copy()
    # Preprocess
    temp_image = get_grayscale(temp_image)

    temp_image = thresholding(temp_image)

    # OCR
    custom_config = r'--oem 3 --psm 12'
    pytesseract.pytesseract.tesseract_cmd = pytesseract_path
    df = pytesseract.image_to_data(temp_image, config=custom_config, output_type=Output.DICT)
    



