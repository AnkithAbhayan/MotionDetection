from source.image_processing import ImageProcessing
from PIL import Image
from math import floor
import json
import cv2
import os

class VideoProcessing:
    def __init__(self, filepath):
        self.buffer = []
        self.differences = []
        self.timestamps = []
        self.filepath = filepath
        self.cap = cv2.VideoCapture(filepath)

        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.duration = self.frame_count/self.fps


    def add_new_frame(self, frame):
        self.buffer.append(frame)

    def process_current_and_previous_frame(self):
        if len(self.buffer) == 2:
            client = ImageProcessing(self.buffer[0], self.buffer[1])
            difference = client.calculate_difference()
            
            self.differences.append(difference)
            del self.buffer[0]

    def process_video(self):
        if self.cap.isOpened() == False:
            print("error opening video file")
            sys.exit()

        count = 0 
        time_per_frame = 1/self.fps
        seconds_done_rn = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret == True:
                im = Image.fromarray(frame)
                self.add_new_frame(im)
                count += 1
                print(f"processing frame {count}/{self.frame_count}")
                self.process_current_and_previous_frame()
                seconds_done_rn += time_per_frame
                self.timestamps.append(seconds_done_rn)
                if cv2.waitKey(25) and 0xFF == ord('q'):
                    break
            else:
                break

        cv2.destroyAllWindows()
    def save_results(self):
        if not os.path.exists("log"):
            os.mkdir("log")
        
        self.differences = [float(item) for item in self.differences]
        data = {
            "timestamps":self.timestamps,
            "differences":self.differences,
            "fps":self.fps,
            "frame_count":self.frame_count
        }
        with open(f"log/{os.path.basename(self.filepath)}.json", "w") as JsonFile:
            json.dump(data, JsonFile)

