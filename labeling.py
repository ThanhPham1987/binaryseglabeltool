import cv2
import numpy as np 
import os
import argparse

argparser = argparse.ArgumentParser(
    description='Image Segmentation Labeling too')

argparser.add_argument(
    '-i',
    '--images', default="./image/",
    help='image folder')

argparser.add_argument(
    '-l',
    '--labels', default="./image_gt/",
    help='image label folder')

args = argparser.parse_args()


# Global variables
drawing = False # true if mouse is pressed
mode = "pen" # "pen" or "eraser"
pensize = 10

# Image and Label
img_path = None
img = None
label_path = None
label = None
last_label = None

line_begin = (-1, -1)
line_end = (-1, -1)

# mouse callback function
def interactive_drawing(event, x, y, flags, param):
    global ix, iy, drawing, mode, label, last_label, img, line_begin, line_end
    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        ix,iy=x,y

        # If in "line" mode, save the first point
        if mode == "line":
            line_begin = (x,y)
            line_end = (x,y)

    elif event==cv2.EVENT_MOUSEMOVE:

        if drawing == True:
            
            if mode == "pen":
                cv2.line(label, (ix,iy), (x,y), (255, 255, 255), pensize)
                ix=x
                iy=y

            elif mode == "eraser":
                cv2.line(label, (ix,iy), (x,y), (0, 0, 0), pensize)
                ix=x
                iy=y

            # If in "line" mode, save the first point
            elif mode == "line":
                line_end = (x,y)   

    elif event==cv2.EVENT_LBUTTONUP:

        drawing=False

        if mode == "magic":
            last_label = label # backup

            connectivity = 4 # or 8?
            newMaskVal = 255
            flags = connectivity + (newMaskVal << 8) + cv2.FLOODFILL_FIXED_RANGE

            # tmp = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            tmp = cv2.GaussianBlur(img,(3,3),cv2.BORDER_DEFAULT)
            # Mask used to flood filling.
            # Notice the size needs to be 2 pixels than the image.
            h, w = tmp.shape[:2]
            mask = np.zeros((h + 2, w + 2), np.uint8)

            # Floodfill from point (0, 0)
            cv2.floodFill(tmp, mask, (x, y), 255, loDiff=(20, 20, 20), upDiff=(20, 20, 20), flags=flags)

            label = label | mask[1:-1, 1:-1]

        elif mode == "line":
            cv2.line(label, line_begin, line_end, (255, 255, 255), pensize)

    return x,y



def combine_img_label(img, label):
    global drawing, mode, image_name_list, img_index
    redImg = np.zeros(img.shape, img.dtype)
    redImg[:,:] = (0, 0, 255)
    redMask = cv2.bitwise_and(redImg, redImg, mask=label)
    
    output_img = cv2.addWeighted(redMask, 1, img, 1, 0)
    output_img = cv2.putText(output_img, 'Drawing: ' + str(drawing) + ' - Mode: ' + mode , (10, 20) , cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 255, 0), 1, cv2.LINE_AA) 
    output_img = cv2.putText(output_img, 'Pen size: ' + str(pensize), (10, 40) , cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 255, 0), 1, cv2.LINE_AA) 
    cv2.line(output_img, (120, 35), (140, 35), (0, 0, 255), pensize)
    output_img = cv2.putText(output_img, 'Image: {} / {}'.format(img_index+1, len(image_name_list)), (10, 60) , cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 255, 0), 1, cv2.LINE_AA) 
    cv2.line(output_img, (120, 35), (140, 35), (0, 0, 255), pensize)

    # If in line mode, draw temporary line
    if mode == "line" and drawing:
        cv2.line(output_img, line_begin, line_end, (0, 0, 255), pensize)

    return output_img

def refine_mask(input_mask):
    # Copy the thresholded image.
    im_floodfill = input_mask.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = input_mask.shape[:2]

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, None, (0, 0), 255)
    cv2.floodFill(im_floodfill, None, (319, 0), 255)
    cv2.floodFill(im_floodfill, None, (319, 239), 255)
    cv2.floodFill(im_floodfill, None, (0, 239), 255)

    im_floodfill = cv2.resize(im_floodfill, (320, 240))

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    return input_mask | im_floodfill_inv

def reload_images():
    global img, img_path, label, label_path, image_folder, label_folder, image_name_list, img_index, last_label
    img_path = os.path.join(image_folder, image_name_list[img_index])
    label_path = os.path.join(label_folder, image_name_list[img_index])
    img = cv2.imread(img_path)
    label = cv2.imread(label_path, 0)
    label = refine_mask(label)
    last_label = label

def save_label():
    global label, label_path, label_folder, image_name_list, img_index
    label_path = os.path.join(label_folder, image_name_list[img_index])
    cv2.imwrite(label_path, label)

# Initialize
print("Image Segmentation Labeling tool")
print("Instruction: ")
print("Pen: w; Eraser: e; Save: s; +pensize: z; -pensize: x; Reload: r")
print("Next image: f")
print("Previous image: d")

image_folder = args.images
label_folder = args.labels
image_name_list = sorted(list(os.listdir(image_folder)))
image_name_list = [path for path in image_name_list if path.endswith(".jpg") or path.endswith(".png") ]
img_index = 0
if len(image_name_list) == 0:
    print("Error reading image folder:" +  image_folder)
    exit(1)
else:
    reload_images()


window_name = "Segmentation Label Editor"
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name,interactive_drawing)

while(1):
    cv2.imshow(window_name, combine_img_label(img, label))

    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('s'): # Save image
        save_label()
    elif k == ord('w'): # Pen mode
        mode = "pen"
    elif k == ord('e'): # Eraser mode
        mode = "eraser"
    elif k == ord('m'): # Magic mode
        mode = "magic"
    elif k == ord('t'): # Line mode
        mode = "line"
    elif k == ord('n'): # Undo magic
        label = last_label
    elif k == ord('z'): # Increase pen size
        pensize += 1
    elif k == ord('x'): # Decrease pen size
        pensize -= 1
        if pensize < 1:
            pensize = 1
    elif k == ord('r'): # Reload image and label
        reload_images()
    elif k == ord('f'): # Next image
        save_label() # Save label first
        img_index += 1
        if img_index >= len(image_name_list):
            img_index = 0
        reload_images()
    elif k == ord('d'): # Previous image
        save_label() # Save label first
        img_index -= 1
        if img_index < 0:
            img_index = 0
        reload_images()


cv2.destroyAllWindows()
