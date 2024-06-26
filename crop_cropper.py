# enter code here
import machupX as mx  # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import json 
import itertools
import os
import csv
import time 
from PIL import Image

class jpeg_cropper:
    """"This class allows for the creation of tables for any aircraft that can be read into machup"""
    def __init__(self, input_file):
        self.input_file = input_file
        self.load_json()

    def load_json(self):
        """
        This function pulls in all the input values from the json.

        It reads the input values from a JSON file and assigns them to the corresponding class attributes.

        Args:
            None

        Returns:
            None
        """
        with open(self.input_file, 'r') as json_handle:
            input_vals = json.load(json_handle)
            self.original_directories = input_vals["original_directories"]
            self.new_directories = input_vals["new_directories"]
            self.example_jpg = input_vals["example_jpg"]    
            self.crop_percent = input_vals["crop_percentage"]

def crop_longer_side(input_jpg, output_jpg, crop_percent):
    """
    Crops the top and bottom of the longer side of an image by specified percentages.

    Args:
        input_jpg (str): The path to the input jpeg file.
        output_jpg (str): The path to the output jpeg file.
        crop_percent_top (float): The percentage of the entire longer side to crop from the top.
        crop_percent_bottom (float): The percentage of the entire longer side to crop from the bottom.
    """
    with Image.open(input_jpg) as img:
        width, height = img.size

        if height > width:
            # For taller images, calculate top and bottom crop based on height
            top = int(height * crop_percent / 100)
            bottom = height - int(height * crop_percent / 100)
            box = (0, top, width, bottom)
        else:
            # For wider images, calculate left and right crop based on width
            left = int(width * crop_percent / 100)  # Assuming crop_percent_top is used for left
            right = width - int(width * crop_percent / 100)  # Assuming crop_percent_bottom is used for right
            box = (left, 0, right, height)

        cropped_image = img.crop(box)
        cropped_image.save(output_jpg)

def loop_through_directories_and_crop_longer_sides(original_directories, new_directories, crop_percent):
    """
    Loops through all the directories in the original_directories list, crops the images in each directory, and saves the cropped images in the corresponding directories in the new_directories list.

    Args:
        original_directories (list): List of paths to the original directories containing the images to crop.
        new_directories (list): List of paths to the new directories where the cropped images will be saved.
        crop_percent (float): The percentage of the entire longer side to crop from the top and bottom.

    Returns:
        None
    """
    for original_dir, new_dir in zip(original_directories, new_directories):
        for file in os.listdir(original_dir):
            if file.endswith(".jpg") or file.endswith(".jpeg"):
                input_jpg = os.path.join(original_dir, file)
                output_jpg = os.path.join(new_dir, file)
                crop_longer_side(input_jpg, output_jpg, crop_percent)
# Example usage
# crop_longer_side('path/to/input.jpg', 'path/to/output.jpg', 10)  # Crop 10% from the longer side

if __name__=="__main__":
    # machup_input_file = ".\..\..\..\Aircraft\Baseline_Full\Aerodynamics\MachupX\Input_files\F16_input.json"

    # initialize the jpeg_cropper object
    jpeg_cropper = jpeg_cropper("crop_cropper.json")
    # do an example crop splitter thing. 

    time_1 = time.perf_counter()
    
    # crop_longer_side(jpeg_cropper.example_jpg, "output.jpg", jpeg_cropper.crop_percent)
    loop_through_directories_and_crop_longer_sides(jpeg_cropper.original_directories, jpeg_cropper.new_directories, jpeg_cropper.crop_percent)

    time_2 = time.perf_counter()

    # Print the time taken to crop the image
    print(f"Time taken to crop image: {time_2 - time_1} seconds")
    
