
import numpy as np 
import os
import argparse
from shutil import copyfile

argparser = argparse.ArgumentParser(
    description='Image Segmentation Labeling too')

argparser.add_argument(
    '-i',
    '--images', default="./image/",
    help='image folder')

argparser.add_argument(
    '-l',
    '--labels', default="./image_gt_bin/",
    help='image label folder')

args = argparser.parse_args()


image_folder = args.images
label_folder = args.labels
image_name_list = sorted(list(os.listdir(image_folder)))
image_name_list = [path for path in image_name_list if path.endswith(".jpg") or path.endswith(".png") ]


dlen = len(image_name_list)
for i in range(len(image_name_list)):
    if i in range(dlen // 3):
        sim_folder = "./sim1"
    elif i in range(dlen // 3 + 1, 2 * dlen // 3 + 1):
        sim_folder = "./sim2"
    else:
        sim_folder = "./sim3"

    img_path = os.path.join(image_folder, image_name_list[i])
    label_path = os.path.join(label_folder, image_name_list[i])

    copyfile(img_path, os.path.join(sim_folder, 'image/', image_name_list[i]))
    copyfile(label_path, os.path.join(sim_folder, 'image_gt/', image_name_list[i]))

    
