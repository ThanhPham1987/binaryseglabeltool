
import numpy as np 
import os
import argparse
import cv2

argparser = argparse.ArgumentParser(
    description='Convert to Kitti format')

argparser.add_argument(
    '-o',
    '--output', default="./image_gt_kitti/",
    help='output folder')

argparser.add_argument(
    '-l',
    '--labels', default="./image_gt_bin/",
    help='image label folder')

args = argparser.parse_args()


label_folder = args.labels
output_folder = args.output
image_name_list = sorted(list(os.listdir(label_folder)))
image_name_list = [path for path in image_name_list if path.endswith(".jpg") or path.endswith(".png") ]


for i in range(len(image_name_list)):
    label_path = os.path.join(label_folder, image_name_list[i])
    output_path = os.path.join(output_folder, image_name_list[i])
    img = cv2.imread(label_path)

    # Remove small holes
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    height, width, channels = img.shape
    for x in range(0,height):
        for y in range(0,width):
            if img[x,y,0] == 0 and img[x,y,1] == 0 and img[x,y,2] == 0:
                img[x,y,0] = 0
                img[x,y,1] = 0
                img[x,y,2] = 255
            else:
                img[x,y,0] = 255
                img[x,y,1] = 0
                img[x,y,2] = 255

    print("{} / {}".format(i, len(image_name_list)))

    # Write output
    cv2.imwrite(output_path, img)

    
