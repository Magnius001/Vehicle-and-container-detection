# Setup environment
import collections
import sys
import torch

sys.path.append(r"src\plate_to_text")
from plate_to_text.ptt import ocr_ 

def setup_model(modelName, weightPath):
    model = torch.hub.load('ultralytics/{}'.format(modelName), 'custom', path = weightPath)
    # Custom config here
    
    # ...
    return model

# Return arrays of cropped images of a single frame
def _extract_result(results, frame) -> list:
    # Extract to dataframe
    df = results.pandas().xyxy[0]
    # Added cropped image to output deque as nd.arrays
    output = []
    # print(df)
    # Real scenarios should only output one image
    for ind in df.index:
        frame
        leftMin, topMin = int(df['xmin'][ind]), int(df['ymin'][ind])
        leftMax, topMax = int(df['xmax'][ind]),int(df['ymax'][ind])
        class_name = str(df['name'][ind])
        # Crop image and append to output array, add extra conditions if needed
        if "plate" in class_name:
            cropped_image = frame[topMin:topMax, leftMin:leftMax]
            processed_image = ocr_(cropped_image, 1, 1, r'D:/Programs/Tesseract-OCR/tesseract.exe')
            new_tuple = (processed_image, class_name)
            output.append(new_tuple)
    return output


def detect(image, model = None) -> list:
    # Setup
    # Using default model if needed
    if model is None:
        model = setup_model("yolov5", "weights/best_plate.pt")
    # Inference
    frame = image.copy()
    results = model(frame)
    # results.print()
    # Extracting
    return _extract_result(results, frame)