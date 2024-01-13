import os
import sys
from controller import controller

# # Defining all types of yolo models
# PLATE_REGION = 0
# PLATE_OCR = 1

def main():
    # for thread in support_threads:
    #     thread.start()
    stream_names = ['FRONT', 'BACK', 'CON1', 'CON2']
    stream_urls = []
    # stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.111:554/media/video2&172.16.17.111:80/LAPI/V1.0/Channels/1")
    # stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.112:554/media/video2&172.16.17.112:80/LAPI/V1.0/Channels/1")
    # stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.117:554/media/video2&172.16.17.117:80/LAPI/V1.0/Channels/1")
    # stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.117:554/media/video2&172.16.17.117:80/LAPI/V1.0/Channels/1")
    stream_urls.append(r"E:\Internship\ML_simplePython_2\ML_simplePython\test_video\x2mate.com-SmartGate.mp4")
    stream_urls.append(r"E:\Internship\ML_simplePython_2\ML_simplePython\test_video\x2mate.com-SmartGate.mp4")
    stream_urls.append(r"E:\Internship\ML_simplePython_2\ML_simplePython\test_video\x2mate.com-SmartGate.mp4")
    stream_urls.append(r"E:\Internship\ML_simplePython_2\ML_simplePython\test_video\x2mate.com-SmartGate.mp4")
    new_app = controller.Controller(stream_names, stream_urls)
    print("Exiting...\n")
    os._exit(1)

if __name__ == "__main__":
    main()