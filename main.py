import cv2
from PIL import Image
import sys
from source.image_processing import ImageProcessing
from source.video_processing import VideoProcessing
from source.showdata import GraphData

class Core:
    def __init__(self):
        self.arguments = sys.argv
        self.filepath = []
        self.type = 0

    def load_arguments(self):
        if len(self.arguments) == 1:
            print("No arguments found, enter 2- [type] and [path(s)].")
            sys.exit()

        self.type = self.arguments[1]
        if self.arguments[1] == "vid":
            if len(self.arguments) != 3:
                print("Wrong number of arguments for 'path(s)'. Enter 1 in this case.")
                sys.exit()
            self.filepath = [self.arguments[2]]

        elif self.arguments[1] == "img":
            if len(self.arguments) > 4 or len(self.arguments) < 4:
                print("Wrong number of arguments for 'path(s). Enter 2 in this case.'")
                sys.exit()
            self.filepath = self.arguments[2:4]
        elif self.arguments[1] == "showdata":
            if len(self.arguments) != 3:
                print("Wrong number of arguments for 'path(s)'. Enter 1 in this case.")
                sys.exit()
            self.filepath = self.arguments[2]
        else:
            print("Unknown argument for 'type'. Enter either 'vid', 'img' or 'showdata'.")
            sys.exit()  

    def invoke_img_processor(self):
        first_im = Image.open(self.filepath[0])
        second_im = Image.open(self.filepath[1])
        imgprocx = ImageProcessing(first_im, second_im)
        print(f"DIFFERENCE- {imgprocx.calculate_difference()}")

    def invoke_vid_processor(self):
        vidprocx = VideoProcessing(self.filepath[0])
        vidprocx.process_video()
        vidprocx.save_results()

    def invoke_data(self):
        dataclient = GraphData(self.filepath)
        dataclient.configuredata()
        dataclient.relayresults()
        dataclient.showgraph()
        
myclient = Core()
myclient.load_arguments()


data = {
    "img":myclient.invoke_img_processor,
    "vid":myclient.invoke_vid_processor,
    "showdata":myclient.invoke_data
}
data[myclient.type]()
