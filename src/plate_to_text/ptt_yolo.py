# Setup environment
import collections
import sys
import numpy
import torch
import cv2
import pandas

# Mute false positive warnings
pandas.options.mode.chained_assignment = None  # default='warn'

from plate_to_text.ptt import ocr_ 

# def setup_model(modelName, weightPath):
#     model = torch.hub.load('ultralytics/{}'.format(modelName), 'custom', path = weightPath, verbose=False)
#     # Custom config here
#     model.conf = 0.35
#     # ...
#     return model

# Resize
def _resize_image(image, scale_factor):
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

# Return a single frame with boundary boxes
def _extract_result(results, frame):
    # Extract to dataframe
    df = results.pandas().xyxy[0]
    df = pandas.DataFrame(df)
    mean_of_y = int((df.max()['ymin'] + df.min()['ymin'])/2)
    print(f'Mean of ymin: {mean_of_y}\n')
    # Added boundary boxes to frame
    for ind in df.index:
        # Extracting coords
        x1, y1 = int(df['xmin'][ind]), int(df['ymin'][ind])
        x2, y2 = int(df['xmax'][ind]),int(df['ymax'][ind])
        # Draw boundary boxes
        cv2.rectangle(frame, (x1, y1), (x2, y2), color=(255,0,0), thickness=2)
        # Convert class name to character
        df['name'][ind] = _class_to_character(int(df['name'][ind]))
        # Put text in boundary boxes
        cv2.putText(frame, df['name'][ind], (x1, y1+20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 0), 2)
        # Separate top from bottom row
        df['ymin'][ind] = int(df['ymin'][ind])
        if df['ymin'][ind] > mean_of_y:
            df['ymin'][ind] = 1
        else:
            df['ymin'][ind] = 0
    df = df.sort_values(['ymin', 'xmin'], ascending = [True, True])
    df = df.reset_index()
    print(df)
    if _verify_result(df):
        print(_result_to_string(df))
        return frame
    return frame

# Convert from class name to character on plate
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
def _verify_result(df) -> bool:
    df.reset_index()
    if (len(df) == 8 or len(df) == 9) and str(df['name'][2]).isalpha() and str(df['name'][0]).isdigit():
        return True
    else:
        return False

def _result_to_string(df: pandas.DataFrame) -> str:
    df.reset_index()
    output = ""
    for ind in df.index:
        output += df['name'][ind]
    return output

def ocr_yolo_version(image, model = None) -> numpy.ndarray:
    # Setup
    # Using default model if needed
    if model is None:
        return None
    # Inference
    frame = image.copy()
    frame = _resize_image(frame, 5)
    results = model(frame)
    return _extract_result(results, frame)
