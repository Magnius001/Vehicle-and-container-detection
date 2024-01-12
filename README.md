# REAL TIME VEHICLE AND CONTAINER DETECTION SYSTEM
## Status: Developing
This project take video streams and perform truck detection, plate and container's codes OCR by using Yolov5 models.

In its current state, the project only serves as a proof-of-concept only, so the efficiency and error rate for object detections are questionable.

Plan for improvements:
- Improve all Yolo model, or converting it to the newest Yolo version
- Improve GUI performance, the current GUI is running at 1 fps
- Improve overall code structure to allow better data transfer from object detection part to GUI
- Improve stability and robustness as the current program will not responding due to infinite while loop when the video stream stopped or interrupted
## How to run
### Installing libraries
All required modules have been listed in the requirements.txt folder in root directory.
To install them with pip:
```
pip install -r requirements.txt
```
### Weight files
The weight files are required to run the different yolov5 models. Due to their size, they cannot be included with this repositary.
### Running the application
To run the application, we only need to execute the main.py script in the src folder. The command is as follow:
```
python -u src\main.py
```
### Important notices
The current version of the application pull from 3 camera streams of Hai Phong Port. Therefore, suitable Fortinet Client setup is required. For further information regarding this matter, please contact Mr. Phong (Head of R&D).

However, a alternate version can be run by changing the 4 urls in the main.py file to either other video urls or path to local video file. The 4 urls mentioned above are as follow:
```
stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.111:554/media/video2&172.16.17.111:80/LAPI/V1.0/Channels/1")
stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.112:554/media/video2&172.16.17.112:80/LAPI/V1.0/Channels/1")
stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.117:554/media/video2&172.16.17.117:80/LAPI/V1.0/Channels/1")
stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.117:554/media/video2&172.16.17.117:80/LAPI/V1.0/Channels/1")
```

## Further discussions
This section is just my rant and talk about the application itself. Feel free to skip should you not want to read it.
### Design objectives
The original purposes of this application was to determine the container's codes only. However, throughout the design process, extra features were added, including the GUI, front and back plate detection.
### Modularity of the application
In theory, the program can be modified to accept more camera streams by just adding more labels to the gui frame.
### Using threads to receive video streams instead of processes
Considering the current project only run on 4 video streams, using the threads offer sufficient performance while lower performance overhead and maintanance cost. Should the program be expand to multiple lanes with more camera streams, adding one process for each set of 4 streams is recommended.
### Frame rates
Frame rates can be control with the UPDATE_INTERVAL constant in controller.py. Lower update interval will result in better frame rates but require more computing and vice versa.
