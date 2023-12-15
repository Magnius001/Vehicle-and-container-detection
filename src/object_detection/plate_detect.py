# Setup environment
import collections
import re
import torch
import cv2 
import numpy as np
import pytesseract
from pytesseract import Output

def setup_model(modelName, weightPath):
    model = torch.hub.load('ultralytics/{}'.format(modelName), 'custom', path = weightPath)
    # Custom config here
    
    # ...
    return model

# Return arrays of cropped images
def extract_result(results, frame):
    # Extract to dataframe
    df = results.pandas().xyxy[0]
    # Added cropped image to output deque as nd.arrays
    output = collections.deque()
    print(df)
    # Real scenarios should only output one image
    for ind in df.index:
        frame
        leftMin, topMin = int(df['xmin'][ind]), int(df['ymin'][ind])
        leftMax, topMax = int(df['xmax'][ind]),int(df['ymax'][ind])
        # Crop image and append to output array, add extra conditions if needed
        if True:
            output.append(frame[topMin:topMax, leftMin:leftMax])
    return output


def detect(image, modelName, weightPath):
    # Setup
    model = setup_model(modelName, weightPath)
    # Inference
    frame = image.copy()
    results = model(frame)
    results.print()
    # Extracting
    croppedImages = extract_result(results, frame)
    return croppedImages