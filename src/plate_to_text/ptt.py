import numpy as np
import pytesseract
from pytesseract import Output
import cv2
import skimage

folderDir = None

# Preprocessing functions
def get_grayscale(image):
    output = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return output
 
# Median filter
def apply_median_filter(image):
    output = cv2.medianBlur(image, 5)
    return output

# Resize
def resize_image(image, scale_factor):
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

# Dilation
def apply_dilation(image):
    kernel = np.ones((1,1),np.uint8)
    output = cv2.dilate(image, kernel, iterations = 1)
    return output

# Convolution

# Convert to 0 -> 1 scale
def rescale_intensity(image):
    output = skimage.exposure.rescale_intensity(image, (0, 255), (0, 1))
    return output

# Thresholding
def thresholding(image):
    output = image.astype(np.uint8)
    # output = cv2.GaussianBlur(image, (3, 3), 0)
    output = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # output = cv2.adaptiveThreshold(output, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)
    return output

# Substration

# Fill
def fill_holes(image):
    seed = np.copy(image)
    seed[1:-1, 1:-1] = image.max()
    mask = image
    output = skimage.morphology.reconstruction(seed, mask, method='erosion')
    return output

# Morphology and Erosion
def apply_morphological(thresholed_image):
    kernel = np.ones((7,7), np.uint8)
    # invert = cv2.bitwise_not(thresholed_image)
    output = cv2.morphologyEx(thresholed_image, cv2.MORPH_BLACKHAT, kernel)
    return output

# Erosion
def erode(image):
    kernel = np.ones((3,3),np.uint8)
    output = cv2.erode(image, kernel, iterations = 1)
    return output


#skew correction - not used
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
    return output

#border removal
def remove_border(image):
    mask = np.zeros(image.shape, dtype=np.uint8)

    cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    cv2.fillPoly(mask, cnts, [255,255,255])
    mask = 255 - mask
    result = cv2.bitwise_or(image, mask)
    return result

# Save image
def save_image(image, filename):
    # return cv2.imwrite(filename, image)
    # cv2.imshow(filename, image)
    # cv2.waitKey(10)
    return True



def pytesseract_setup(oem, psm, pytesseract_path):
    pytesseract.pytesseract.tesseract_cmd = pytesseract_path
    return '--oem 3 --psm 12'

def draw_bounding_boxes(image, df):
    n_boxes = len(df['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (df['left'][i], df['top'][i], df['width'][i], df['height'][i])
        if df['conf'][i]>-1:
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            image = cv2.putText(image, df['text'][i], (x, y-5), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
    return image

def ocr_(image, oem, psm, pytesseract_path):
    # Preprocess
    temp_img = image.copy()
    temp_img = resize_image(temp_img, 3)
    temp_img = get_grayscale(temp_img)
    # Median filter
    temp_img = apply_median_filter(temp_img)
    # # Binarization
    temp_img = thresholding(temp_img)
    # Remove border
    temp_img = remove_border(temp_img)
    # Dilation
    temp_img = apply_dilation(temp_img)
    # Convolution

    # Convert to 0 -> 1 scale
    # temp_img = rescale_intensity(temp_img)
    # # Substration

    # # Fill
    # temp_img = fill_holes(temp_img)

    # # Morphology and Erosion
    # temp_img = apply_morphological(temp_img)
    temp_img = erode(temp_img)
    # temp_img = cv2.bitwise_not(temp_img)
    # OCR
    custom_config = r'--oem 3 --psm 12'
    pytesseract.pytesseract.tesseract_cmd = pytesseract_path
    output = pytesseract.image_to_string(temp_img, config=custom_config)
    print(output.replace('\n', ''), '\n')
    # df = pytesseract.image_to_data(temp_img, config=custom_config, output_type=Output.DICT)
    # image = draw_bounding_boxes(image, df)
    # print(df.keys())
    return temp_img

    



