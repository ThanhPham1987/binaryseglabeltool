#! /usr/bin/env python

import cv2
import numpy as np
import argparse
import os

# define command line arguments
argparser = argparse.ArgumentParser(
    description='Image extractor from video')

argparser.add_argument(
    '-v',
    '--video', default="video.mp4",
    help='path to video file')

argparser.add_argument(
    '-i',
    '--image_folder', default="./image",
    help='path to output rgb image folder')

argparser.add_argument(
    '-height',
    '--height', default="240",
    help='image height')

argparser.add_argument(
    '-width',
    '--width', default="320",
    help='image width')

argparser.add_argument(
    '-s',
    '--steps', default="10",
    help='number of steps between frames')


def _main_(args):
    """
    :param args: command line argument
    """

    # image count
    count = 0

    image_width = int(args.width)
    image_height = int(args.height)

    if not os.path.exists(args.image_folder):
        os.makedirs(args.image_folder)

    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv2.VideoCapture(args.video)
    
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
        return

    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        for i in range(int(args.steps)):
            ret, frame = cap.read()
        
        if not ret:
            break

        image = cv2.resize(frame, (image_width, image_height))

        cv2.imwrite(os.path.join(args.image_folder, "image_" + str(count).zfill(5) + ".png"), image)

        print(count)
        count += 1
        

if __name__ == '__main__':
    # parse the arguments
    args = argparser.parse_args()
    _main_(args)

