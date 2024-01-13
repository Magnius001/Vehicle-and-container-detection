# Setup environment
import numpy
import cv2
import pandas

pandas.options.mode.chained_assignment = None  # default='warn'


# Resize
def _resize_image(image, scale_factor) -> numpy.ndarray:
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

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
        # Put boundary boxes to image and add it to tuple
        if True:
            code_detected_flag = True
            # Mock code
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