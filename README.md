# REAL-TIME VEHICLE AND CONTAINER DETECTION SYSTEM
## Status: Ending
This project take video streams and perform truck detection, plate and container's codes OCR by using Yolov5 models.

In its current state, the project only serves as a proof-of-concept only, so the efficiency and error rate for object detections are questionable.

Plan for improvements:
- Improve all Yolo model, or converting it to the newest Yolo version.
- Improve GUI performance, the current GUI is running at <20 fps. This is due to the fact that the GUI is multithreading on a single thread.
- Improve overall code structure to allow better data transfer from object detection part to GUI.
- Improve stability and robustness as the current program will not responding due to infinite while loop when the video stream stopped or interrupted.
## How to run
### Installing Pip
Pip is the package installer for Python and it will be used exclusively for installing the required packages for this project. If you have Pip already (which is likely as Pip is come packaged with Python installed from python.org), skip over this section. If you don't, please follow the steps from [pip installing guide](https://pip.pypa.io/en/stable/installation/).

This project used pip version 22.3.1.
### Installing libraries
All required modules have been listed in the requirements.txt folder in root directory.
To install them with pip:
```
pip install -r requirements.txt
```
In case that does not work, here is how to install the libraries manually.
#### Pytorch
For PyTorch, you need to visit the [Pytorch website](https://pytorch.org/get-started/locally/) and choose the suitable version.
#### OpenCV, Pandas and CustomTkinter
They can be install by running the following code:
```
pip install opencv-python
pip install pandas
pip install customtkinter
```
### Weight files
The weight files are required to run the different yolov5 models. Due to their size, they cannot be included with this repositary.
### Running the application
To run the application, we only need to execute the main.py script in the src folder. The command is as follow:
```
python -u src\main.py
```
## Important notices
### Input video streams
The current version of the application pull from 3 camera streams of Hai Phong Port. Therefore, suitable Fortinet Client setup is required. For further information regarding this matter, please contact Mr. Phong (Head of R&D).

However, a alternate version can be run by changing the 4 urls in the main.py file to either other video urls or path to local video file. The 4 urls mentioned above are as follow:
```
stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.111:554/media/video2&172.16.17.111:80/LAPI/V1.0/Channels/1")
stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.112:554/media/video2&172.16.17.112:80/LAPI/V1.0/Channels/1")
stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.117:554/media/video2&172.16.17.117:80/LAPI/V1.0/Channels/1")
stream_urls.append(r"rtsp://admin:A@12345678@172.16.17.117:554/media/video2&172.16.17.117:80/LAPI/V1.0/Channels/1")
```

### Frame rates
Frame rates can be control with the UPDATE_INTERVAL constant in controller.py. Lower update interval will result in better frame rates but require more computing and vice versa.

### Trainings
#### Yolov5 Framework
For simplicity purposes, I decided to use the Yolov5 framework for training. The details on how to use the framework can be found in the [Yolov5 Git Repository](https://github.com/ultralytics/yolov5).

#### Used datasets
The weight files for the current project is trained from premaded Roboflow datasets. The links to them are in the root directory. The links are mainly for referencing, visualizing the classes. All of the datasets should be included in the onedrive folder.

#### Training with custom datasets
After cloning the yolov5 framework, extract the datasets into the yolov5 directory. Then, run the following code:
```
python train.py --img 640 --batch 24 --epochs 10 --data <Folder name of the dataset>/data.yaml --weights yolov5l.pt
```
You can replace the pretrained weight file to 5s/5m/5x depending on the use case. If Python has trouble finding the dataset images, I recommend to edit the data.yml file to contain absolute path.

## Further discussions
Discussion on different aspects of the project.
### Design objectives
The original purposes of this application was to determine the container's codes only. However, throughout the design process, extra features were added, including the GUI, front and back plate detection.
### Modularity of the application
In theory, the program can be modified to accept more camera streams by just adding more labels to the gui frame.
### Using threads to receive video streams instead of processes
Considering the current project only run on 4 video streams, using the multithreading over multiprocessing offer sufficient performance while lowering performance overhead and maintanance cost. Should the program be expand to multiple lanes with more camera streams, creating one process for each set of 4 streams is recommended.
### Using Yolov5
Out of the bunch, v5 is the simplest one to use while also offering good enough performanance. From a brief research, Yolov8 seems to be the best model for real-time system, which is what this long-term project aiming for. Converting to yolov8 should not be too complex as it only involve changing how the model is setup and call, the inference result can still be view and process as a pandas dataframe.

