import customtkinter
import time
import numpy
import cv2
import tkinter
from PIL import Image, ImageTk
from gradient_frame import GradientFrame

# Get screen resolution
import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Setup customtkinter theme
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Main app
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Portlogics")
        self.geometry(f"{screensize[0]}x{screensize[1]}")
        self.config(padx=10, pady=10)

        # Configure grid layout 2x3
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        self.rowconfigure(1, weight=1)


        # Create top banner
        self.top_frame = customtkinter.CTkFrame(self, height=40, fg_color='#2c2f33', corner_radius=4)
        self.top_frame.grid(row=0, column=0, columnspan=2, rowspan=1, pady=5, padx=5, sticky="new")

        # Create left status frame
        self.left_frame = customtkinter.CTkFrame(self, width=450, fg_color='#2c2f33')
        self.left_frame.grid(row=1, column=0, columnspan=1, rowspan=1, pady=5, padx=5, sticky="nsew")
        # self.left_frame.rowconfigure(1, weight=1)
        self.left_frame.rowconfigure(2, weight=1)
        self.left_frame.columnconfigure(0, weight=1)

        # Adding to left status frame
        self.top_left_frame = customtkinter.CTkFrame(self.left_frame, fg_color='#2c2f33')
        self.top_left_frame.grid(row=0, column=0, columnspan=1, rowspan=1, pady=5, padx=5, sticky="new")
        self.top_left_frame.rowconfigure((0,1), weight=1)
        self.top_left_frame.columnconfigure(0, weight=1)
        self.top_left_frame.columnconfigure(1, weight=2)

        self.status_label = customtkinter.CTkLabel(self.top_left_frame, text='STATUS', width=70, height=10, bg_color= '#7289da', corner_radius=20, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.status_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.status_display = customtkinter.CTkLabel(self.top_left_frame, text='TRUCK DETECTED', width=230, height=10, bg_color='#58e91d', corner_radius=20, font=customtkinter.CTkFont(size=20, weight="bold"), text_color='black')
        self.status_display.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.plate_label = customtkinter.CTkLabel(self.top_left_frame, text='PLATE', width=70, height=10, bg_color= '#7289da', corner_radius=20, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.plate_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.plate_display = customtkinter.CTkLabel(self.top_left_frame, text='15C05466', width=230, height=10, bg_color='#ffffff', corner_radius=20, font=customtkinter.CTkFont(size=20, weight="bold"), text_color='black')
        self.plate_display.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Container details display
        self.con_details_display = customtkinter.CTkLabel(self.left_frame, text='Container 1: TRHU558756\nContainer 2: WHSU058540\nDate:  27/12/2023\nTime: 14:55:45\n', anchor='nw', justify='left', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.con_details_display.grid(row=1, column=0, padx=10, sticky="nsew")

        self.bot_left_frame = customtkinter.CTkFrame(self.left_frame, width=300, fg_color='#2c2f33', border_color='#7289da', border_width=2, corner_radius=0)
        self.bot_left_frame.grid(row=2, column=0, columnspan=1, pady=5, padx=5, sticky="nsew")
        self.bot_left_frame.rowconfigure((0,1), weight=1)
        self.bot_left_frame.columnconfigure((0,1), weight=1)

        # Add logo
        logo_img = customtkinter.CTkImage(dark_image=Image.open(r"D:\Download\z5011201651262_2ff0d0dc64e458ab3aef9519d54df2e2-transformed-removebg-preview.png"), size=(int(float(screensize[0])/5.49),int(float(screensize[1])/7.45)))
        self.logo = customtkinter.CTkLabel(self.left_frame, image=logo_img, text='')
        self.logo.grid(row=3, column=0, columnspan=1, pady=5, padx=5, sticky="sew")

        # Creating right frame
        self.right_frame = customtkinter.CTkFrame(self, fg_color='#2c2f33')
        self.right_frame.grid(row=1, column=1, columnspan=1, rowspan=1, pady=5, padx=5, sticky="nsew")
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.columnconfigure(1, weight=1)
        self.right_frame.rowconfigure(0, weight=1)
        self.right_frame.rowconfigure(1, weight=1)

        # Dimensions for each camera
        self.camera_width = int(float(screensize[0])/2.6)
        # camera_width = 740
        self.camera_height = int(float(screensize[1])/2.3)
        # camera_height = 480

        # Adding front camera display
        self.cameras = []
        self.front_camera = []
        self.back_camera = []
        self.con1_camera = []
        self.con2_camera = []
        self.cameras.append(self.front_camera)
        self.cameras.append(self.back_camera)
        self.cameras.append(self.con1_camera)
        self.cameras.append(self.con2_camera)
        self.camera_types = ['FRONT', 'BACK', 'CONTAINER 1', 'CONTAINER 2']
        row = 0
        col = 0
        counter = 0
        for camera in self.cameras:
            camera.append(customtkinter.CTkFrame(self.right_frame))
            camera.append(customtkinter.CTkLabel(camera[0]))
            camera.append(customtkinter.CTkLabel(camera[1]))
            self._setup_camera_display(camera, row, col,self.camera_types[counter])

            if counter % 2 == 0:
                col += 1
            else:
                col = 0
                row += 1
            counter += 1
            
                
        
    def _setup_camera_display(self, _display:list, row:int, col:int, camera_type: str):
        _display[0].configure(width=450, fg_color='#2c2f33', border_color='#7289da', border_width=2, corner_radius=0)
        _display[0].grid(row=row, column=col, pady=5, padx=5)
        _display[0].rowconfigure(0, weight=1)
        _display[0].rowconfigure(1, weight=3)
        _display[0].rowconfigure(2, weight=3)
        _display[0].columnconfigure(0, weight=1)

        _display[1].configure(width=self.camera_width, height=self.camera_height, text='', bg_color= 'transparent', anchor='s')
        _display[1].grid(row=0, column=0, padx=5, pady=5, sticky="n")

        _display[2].configure(width=110, text=camera_type, text_color='#ffffff', bg_color= '#7289da', corner_radius=0, font=customtkinter.CTkFont(size=15, weight="bold"))
        _display[2].place(relx=1, rely=1, x=0, y=1,anchor="se")
    
    def update_camera_display(self, images: list):
        for camera, im in zip(self.cameras, images):
            im = im.copy()
            blue,green,red = cv2.split(im)
            im = cv2.merge((red,green,blue))
            im = Image.fromarray(im)
            imtk = customtkinter.CTkImage(dark_image=im, size=(self.camera_width, self.camera_height-5))
            camera[1].configure(image = imtk)
            camera[1].image = imtk


new_app = App()

images = []
# for i in range(4):
#     images.append(cv2.imread(r"E:\Internship\Common_resources\official_train_img\images\images\1.png"))
images.append(cv2.imread(r"E:\Internship\Common_resources\Screenshots\cam_20070_c.png"))
images.append(cv2.imread(r"E:\Internship\Common_resources\Screenshots\cam_20075_c.png"))
images.append(cv2.imread(r"E:\Internship\Common_resources\Screenshots\cam_20078_c.png"))
images.append(cv2.imread(r"E:\Internship\Common_resources\Screenshots\cam_20079_c.png"))

new_app.update_camera_display(images=images)
new_app.mainloop()