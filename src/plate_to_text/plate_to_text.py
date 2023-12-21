# Setup environment
import collections
import sys
import numpy
import torch
import cv2
import pandas

# Resize
def _resize_image(image, scale_factor) -> numpy.ndarray:
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

# # Return a single frame with boundary boxes
# def place_boundary_boxes(results, frame) -> numpy.ndarray:
#     # Extract to dataframe
#     df = results.pandas().xyxy[0]
#     df = pandas.DataFrame(df)
#     mean_of_y = int((df.max()['ymin'] + df.min()['ymin'])/2)
#     print(f'Mean of ymin: {mean_of_y}\n')
#     # Added boundary boxes to frame
#     for ind in df.index:
#         # Extracting coords
#         x1, y1 = int(df['xmin'][ind]), int(df['ymin'][ind])
#         x2, y2 = int(df['xmax'][ind]),int(df['ymax'][ind])
#         # Draw boundary boxes
#         cv2.rectangle(frame, (x1, y1), (x2, y2), color=(255,0,0), thickness=2)
#         # Convert class name to character
#         df['name'][ind] = _class_to_character(int(df['name'][ind]))
#         # Put text in boundary boxes
#         cv2.putText(frame, df['name'][ind], (x1, y1+20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 0), 2)
#         # Separate top from bottom row
#         df['ymin'][ind] = int(df['ymin'][ind])
#         if df['ymin'][ind] > mean_of_y:
#             df['ymin'][ind] = 1
#         else:
#             df['ymin'][ind] = 0
#     df = df.sort_values(['ymin', 'xmin'], ascending = [True, True])
#     df = df.reset_index()
#     print(df)
#     if _verify_result(df):
#         print(_result_to_string(df))
#         return frame
#     return frame

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

# # Return arrays of cropped images of a single frame
# def _get_cropped_images(results, frame) -> list:
#     # Extract to dataframe
#     df = results.pandas().xyxy[0]
#     # Added cropped image to output deque as nd.arrays
#     output = []
#     # print(df)
#     # Real scenarios should only output one image
#     for ind in df.index:
#         frame
#         leftMin, topMin = int(df['xmin'][ind]), int(df['ymin'][ind])
#         leftMax, topMax = int(df['xmax'][ind]),int(df['ymax'][ind])
#         class_name = str(df['name'][ind])
#         # Crop image and append to output array, add extra conditions if needed then put it through ocr
#         if "plate" in class_name:
#             cropped_image = frame[topMin:topMax, leftMin:leftMax]
#             # processed_image = ocr_(cropped_image, 1, 1, r'D:/Programs/Tesseract-OCR/tesseract.exe')
#             processed_image = _apply_ocr(cropped_image)
#             if processed_image is None:
#                 continue
#             new_tuple = (processed_image, class_name)
#             output.append(new_tuple)
#     return output

# def _region_detect(image, plate_region_model, plate_ocr_model) -> tuple:
    # Inference
    frame = image.copy()
    results = plate_region_model(frame)
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
        if "plate" in class_name:
            cropped_image = frame[topMin:topMax, leftMin:leftMax]
            plate_text = _apply_ocr(cropped_image, plate_ocr_model)
            if plate_text is None:
                continue
            # Placing boundary box and text to original image
            image = cv2.rectangle(image, (leftMin, topMin), (leftMax, topMax), color=(255,0,0), thickness=2)
            image = cv2.putText(image, plate_text, (leftMin, topMin-5), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 0), 2)
            # Adding to list
            all_plate_texts.append(plate_text)
    # Returning the process images
    return (image, all_plate_texts)

# Return a list of image with a string represent the text
def detect(image: numpy.ndarray, plate_region_model = None, plate_ocr_model = None) -> tuple:
    if plate_ocr_model is None or plate_region_model is None or image is None:
        return None
    frame = image.copy()
    results = plate_region_model(frame)
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
        if "plate" in class_name:
            cropped_image = frame[topMin:topMax, leftMin:leftMax]
            plate_text = _apply_ocr(cropped_image, plate_ocr_model)
            if plate_text is None:
                continue
            # Placing boundary box and text to original image
            cv2.rectangle(image, (leftMin, topMin), (leftMax, topMax), color=(255,0,0), thickness=2)
            cv2.putText(image, plate_text, (leftMin, topMin-5), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 0), 2)
            # Adding to list
            all_plate_texts.append(plate_text)
    # Returning the process images
    return (image, all_plate_texts)