from PIL import Image
import numpy
import sys

class ImageProcessing:
    def __init__(self, first_im, second_im):
        self.first_im = first_im
        self.second_im = second_im

        self.pixels_1 = first_im.load()
        self.pixels_2 = second_im.load()

        self.total_diff = 0
        self.pixel_count = 0

    def format_number(self, number):
        number = str(numpy.format_float_positional(number, trim="-"))
        if len(number) < 10:
            for i in range(10-len(number)):
                number+="0"
            return number

        elif len(number) > 10:
            return number[:10]

    def calculate_difference(self):
        for x in range(self.first_im.size[0]): #iterating through all x co-ordinates
            for y in range(self.first_im.size[1]): #iterating through all y co-ordinates
                one_red = self.pixels_1[x,y][0]
                one_green = self.pixels_1[x,y][1]
                one_blue = self.pixels_1[x,y][2]

                two_red = self.pixels_2[x,y][0]
                two_green = self.pixels_2[x,y][1]
                two_blue = self.pixels_2[x,y][2]

                factor = abs(((two_red-one_red)+(two_green-one_green)+(two_blue-one_blue))/3) #difference in colour of 2 pixels
                self.total_diff += factor/255 #reduced to a value between 0 and 1
                self.pixel_count += 1

        value = self.total_diff/self.pixel_count
        return self.format_number(value)