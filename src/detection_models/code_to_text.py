# Setup environment
import collections
import sys
import numpy
import torch
import cv2
import pandas

pandas.options.mode.chained_assignment = None  # default='warn'


# Resize
def _resize_image(image, scale_factor) -> numpy.ndarray:
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

# Convert from class name to alphanumeric characters
def _class_to_character(class_name) -> str:
    id = int(class_name)
    offset = 0
    if id >= 0 and id <= 8:
        offset = 49
    elif id >= 9 and id <= 16:
        offset = 56
    elif id >= 17 and id <= 20:
        offset = 58
    elif id == 21:
        offset = 59
    elif id >= 22 and id <= 25:
        offset = 61
    elif id >= 26 and id <= 28:
        offset = 62
    elif id == 29:
        offset = 19
    return chr(id + offset)

# Check if the result is in the correct format of a license plate
def _verify_result(df: pandas.DataFrame) -> bool:
    df.reset_index()
    if (len(df) == 8 or len(df) == 9) and str(df['name'][2]).isalpha() and str(df['name'][0]).isdigit():
        return True
    else:
        return False

# Get a string of alpha numeric characters from dataframe
def _result_to_string(df: pandas.DataFrame) -> str:
    df.reset_index()
    output = ""
    for ind in df.index:
        output += df['name'][ind]
    return output

# Recognize text from cropped images
def _apply_ocr(cropped_image: numpy.ndarray, model) -> str:
    # Setup
    # Using default model if needed
    if model is None:
        return None
    # Inference
    frame = cropped_image.copy()
    frame = _resize_image(frame, 5)
    results = model(frame)
    # Extracting results
    df = results.pandas().xyxy[0]
    # Empty
    if len(df) < 1:
        return None
    df = pandas.DataFrame(df)
    # Caculate mean of ymin values to determines rows
    mean_of_y = int((df.max()['ymin'] + df.min()['ymin'])/2)
    print(f'Mean of ymin: {mean_of_y}\n')
    # Iterate through dataframe to get the alphanumerics
    for ind in df.index:
        # Extracting coords
        x1, y1 = int(df['xmin'][ind]), int(df['ymin'][ind])
        x2, y2 = int(df['xmax'][ind]),int(df['ymax'][ind])
        # Draw boundary boxes
        # cv2.rectangle(frame, (x1, y1), (x2, y2), color=(255,0,0), thickness=2)
        # Convert class name to character
        df['name'][ind] = _class_to_character(int(df['name'][ind]))
        # Put text in boundary boxes
        # cv2.putText(frame, df['name'][ind], (x1, y1+20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 0), 2)
        # Separate top from bottom row
        df['ymin'][ind] = int(df['ymin'][ind])
        if df['ymin'][ind] > mean_of_y:
            df['ymin'][ind] = 1
        else:
            df['ymin'][ind] = 0
    # Sort based on the highest row and closet to left side
    df = df.sort_values(['ymin', 'xmin'], ascending = [True, True])
    df = df.reset_index()
    # print(df)
    # Check if output format is correct, if yes, return string, else return none
    if _verify_result(df):
        return _result_to_string(df)
    return None

# Return a list of image with a string represent the text if able to detect
def detect(image: numpy.ndarray, code_region_model = None) -> tuple:
    if code_region_model is None or image is None:
        return None
    code_detected_flag = False
    frame = image.copy()
    results = code_region_model(frame)
    # Extracting
    df = results.pandas().xyxy[0]
    # List storing the all the plate texts
    all_plate_texts = []
    # Start iterating through the dataframe
    for ind in df.index:
        leftMin, topMin = int(df['xmin'][ind]), int(df['ymin'][ind])
        leftMax, topMax = int(df['xmax'][ind]),int(df['ymax'][ind])
        class_name = str(df['name'][ind])
        # Crop image and append to output array, add extra conditions if needed then put it through ocr
        if True:
            code_detected_flag = True
            # print("Code region detected\n")
            plate_text = "ABCD123456"
            # Placing boundary box and text to original image
            cv2.rectangle(image, (leftMin, topMin), (leftMax, topMax), color=(255,0,0), thickness=2)
            cv2.putText(image, plate_text, (leftMin, topMin-5), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 0), 2)
            # Adding to list
            all_plate_texts.append(plate_text)
    # Returning the process images
    if not code_detected_flag:
        return None
    return (image, all_plate_texts)