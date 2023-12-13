import torch
import cv2
from PIL import Image

def model_setup(modePath, weightPath):
    model = torch.hub.load(modePath, 'custom', path=weightPath)
    model.conf = 0.8
    return model

# Process on an mp4 file from input, then process using the input model
def videoProcessing(videoPath, model):
    # Reading video file
    print("Opening video stream...\n")
    capture = cv2.VideoCapture(videoPath)
    # Start reading video frames
    while True:
        flag, frame = capture.read()
        # Stop if frame is not ready
        if not flag:
            print("Unable to receive next frame, exiting...")
            break
        # Apply ml model on frame
        results = model(frame)
        # Convert to dataframe
        df = results.pandas().xyxy[0]
        # Iterate through bounding boxes
        for ind in df.index:
            # Extracting bounding box coords from dataframe 
            x1, y1 = int(df['xmin'][ind]), int(df['ymin'][ind])
            x2, y2 = (int(df['xmax'][ind]),int(df['ymax'][ind]))
            cv2.rectangle(frame, (x1, y1), (x2, y2), color=(255,0,0), thickness=2)
            cv2.putText(frame, df['confidence'][ind], (x1, y1-5), color=(255,0,0), thickness=2)
            # Display
            cv2.imshow("Image", downscale_img(frame, 0.7))
            # cv2.imshow("Cropped", frame[x1:x2, y1:y2])
        # Pressed esc to close player
        exitKey = cv2.waitKey(10)
        if exitKey == 27:
            break
    cv2.destroyAllWindows()
    capture.release()

# Downscale image by the given scaleFactor
def downscale_img(image, scaleFactor):
    width = int(image.shape[1] * scaleFactor)
    height = int(image.shape[0] * scaleFactor)
    resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    return resized

def main():
    print("Starting...\n")
    model = model_setup('ultralytics/yolov5', 'weights/best2.pt')
    videoProcessing('test_video/x2mate.com-SmartGate.mp4', model)

if __name__ == "__main__":
    main()