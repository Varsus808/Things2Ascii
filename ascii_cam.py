from math import ceil
import cv2
import numpy as np
import random

import platform
import os
import sys
import time
import argparse
import pathlib
import warnings

def rand_string():
    density = ''
    i = 0
    while i < 11:
        i += 1
        random_char_ord = random.randrange(40, 1000)
        try:
            rand_char = chr(random_char_ord)
            density += rand_char
        except UnicodeEncodeError:
            i -= 1
    return density


def generate_empty_image():
    return np.zeros(shape=(1024, 2048, 3), dtype=np.int8)

def interpret(adjusted_h ,adjusted_w, density, gray, color=""):

    # the steps in which a pixel is evaluated as a char
    # for each 'jump' in the intensity of a given pixel the char is different

    jump = ceil(255 / len(density))

    my_interpretation = '' #Ascii Output

    for x in range(0, adjusted_w):
        for y in range(0, adjusted_h):
            num = gray[x, y].astype(int)
            ascii_representation = density[num // jump]
            my_interpretation += color+ascii_representation
        my_interpretation += color +'\n'
    return my_interpretation
    

def file_to_ascii(density, path_to_file, resolution=1, store=False, color=""):

    try:
        cap = cv2.VideoCapture(path_to_file)
    except:
        warnings.warn("Error opening the File. Please check whether the Path is correct")

    
    pause = input("Press \"Ctrl\" + \"C\" to exit to exit a Video. Press any key to continue")

    if (cap.isOpened() == False):
        print("Error opening video stream or file")
        # Read until video is completed

    my_interpretation=None
    while(cap.isOpened()):
        
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
            # Display the resulting frame


        width = frame.shape[0]
        height = frame.shape[1]

        adjusted_h = height // (4 + (resolution-1))
        adjusted_w = width // (8 + (resolution*2-2))
                    

        # adjust size
        new_image = cv2.resize(frame, (adjusted_h, adjusted_w))
        # single Channel
        gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)


        if my_interpretation!=None:
            cv2.imshow('Frame',frame)


        my_interpretation=interpret(adjusted_h, adjusted_w, density ,gray, color)

        if platform.system() == 'Windows': 
            os.system("cls")
        else:
            os.system("clear")

        print(my_interpretation)
        time.sleep(0.01) #this is sadly needed to reduce flickering


        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def feed_to_ascii(density, source=-1, resolution=1, color=""):
    
   
    cam = cv2.VideoCapture(source)
    ret_val, img = cam.read()

    width = img.shape[0]
    height = img.shape[1]

    adjusted_h = height // (1 + (resolution))
    adjusted_w = width // (1 + (resolution*2))

    print(density)

    while True:

        ret_val, img = cam.read()
        

        # adjust size
        new_image = cv2.resize(img, (adjusted_h, adjusted_w))
        # single Channel
        gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

        my_interpretation=interpret(adjusted_h, adjusted_w, density, gray, color)

        if platform.system() == 'Windows': 
            os.system("cls")
        else:
            os.system("clear")
        
        print(my_interpretation)
        time.sleep(0.01) #this is sadly needed to reduce flickering




def main():

    
    col_dict={
    'black':'\033[0;30m',
    'red':'\033[0;31m',
    'green':'\033[0;32m',
    'orange':'\033[0;33m',
    'blue':'\033[0;34m',
    'purple':'\033[0;35m',
    'cyan':'\033[0;36m',
    'light_gray':'\033[0;37m',
    'dark_grey':'\033[1;30m',
    'light_red':'\033[1;31m',
    'light_green':'\033[1;32m',
    'yellow':'\033[1;33m',
    'light_blue':'\033[1;34m',
    'light_purple':'\033[1;35m',
    'light_cyan':'\033[1;36m',
    'white':'\033[1;37m',
    }

    parser = argparse.ArgumentParser(description="Ascii Cam, example usage: ")
    group = parser.add_mutually_exclusive_group()
    ascii_str_group = parser.add_mutually_exclusive_group()
    
    group.add_argument("-c","--cam", action="store_true", dest="cam",
                        help="VideoCapture Device -1"
    )
    group.add_argument("-f","--file", action="store", dest="file_path",
                        type=str,
                        help="Path to a Picture or Video"
    )

    parser.add_argument("-r", "--resolution", default="4", action="store", dest="res",
                        type=int, required=False,
                        help="Output resolution, starting at 0 (BIG) default %(default)s (inverse linear). Can be higher depending on your input"
    )

    parser.add_argument("-o", "--output", action="store", dest="store",
                        type=str, required=False,
                        help="Name of Out File, currently supported for Picture Mode"
    )
    
    parser.add_argument("-col", "--colour", "--color", choices=[key for key in col_dict], action="store", dest="color",
                        type=str, required=False,
                        help="Color of Ascii chars, for bash console"
    )
    parser.add_argument("-a", "--appearance", action="store", dest="appearance",
                        type=str, required=False,
                        help="String of Ascii Characters to use in conversion"
    )

    ascii_str_group.add_argument("-R", "--random", action="store", dest="random",
                    type=str, required=False,
                    help="Cycle through diffrent Ascii representation. Output may seem broken at times, because random chars aren't of equal width"
    )
    
    ascii_str_group.add_argument("-s", "--source", default=-1, action="store", dest="source",
                    type=int, required=False,
                    help="Provide index of Video Capture Device (e.g. default %(default)s for webcam)"
    )
    

    
    args = parser.parse_args()


    if args.color != None:
        color=col_dict[str(args.color)]
    else:
        color=""

    if args.random != None:
        density = rand_string()
    
    if args.appearance != None:
        density = args.appearance
    else:
        density = 'Ñ@#W$9876543210?!abc;:+=-,._ '[::-1]
    


    if args.cam:
        feed_to_ascii(density=density, source=args.source, resolution=args.res, color=color)
    elif args.file_path:
        file_to_ascii(density=density, path_to_file=args.file_path, resolution=args.res, store=args.store, color=color)
    
    ##TODO
    # resolution less convoluted
    # SOUND for video
    ## Optional:
    ## Store Video as Ascii?

if __name__ == "__main__":
    main()
    