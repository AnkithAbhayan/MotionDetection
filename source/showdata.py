import matplotlib.pyplot as plt
import sys
import json
from math import ceil

class GraphData:
    def __init__(self, filepath):
        self.filepath = filepath

    def configuredata(self):
        with open(f"log\\{self.filepath}.json", "r") as JsonFile:
            self.data = json.load(JsonFile) 
        del self.data["timestamps"][-1]
        
        self.differences = self.data["differences"]
        self.timestamps = self.data["timestamps"]
        self.fps = self.data["fps"]
        self.frame_count = self.data["frame_count"]

        self.ymax = round((max(self.differences)*1.5),2)
        self.xmax = ceil(self.timestamps[-1])+1

    def relayresults(self):
        def calc_time(seconds):
            minutes = 0 
            hours = 0
            if seconds >= 60:
               minutes = str(floor(seconds/60))
               seconds = str(seconds/60)
            if minutes >= 60:
                hours = str(floor(minutes/60))
                minutes = str(minutes%60)
            
            if len(str(seconds)) == 1:
                seconds = "0"+str(seconds)
            if len(str(minutes)) == 1:
                minutes = "0"+str(minutes)
            if len(str(hours)) == 1:
                hours = "0"+str(hours)

            return f"{hours}:{minutes}:{str(seconds)[:6]}"

        def format_fps_count(count, total):
            if len(str(count)) < len(str(total)):
                return f"{'0'*(len(str(total))-len(str(count)))}{count}/{total}"
            return f"{count}/{total}"

        time_per_frame = 1/self.fps
        seconds_done_rn = 0
        print(f"TIME- {self.timestamps[0]} FRAME NO- 001/{self.frame_count} DIFFERENCE- NIL")
        for i in range(len(self.differences)):
            time = calc_time(self.timestamps[i])
            frame_no = format_fps_count(i+2, self.frame_count)
            difference = self.differences[i]
            print(f"TIME- {time} FRAME NO- {frame_no} DIFFERENCE- {difference}")

    def showgraph(self):
        plt.plot(self.timestamps, self.differences)
        plt.axis([0,self.xmax,0,self.ymax])
        plt.ylabel('difference (1 to 0)')
        plt.xlabel('timestamp (seconds)')
        plt.show()