"""
@file filter2D.py
@brief Sample code that shows how to implement your own linear filters by using filter2D function
"""
from math import ceil
import sys
import cv2
import numpy as np
import random


def draw_text(
    img,
    *,
    text,
    uv_top_left,
    color=(255, 255, 255),
    fontScale=1,
    thickness=1,
    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    outline_color=(255, 0, 0),
    line_spacing=1.5,
):
    """
    Draws multiline with an outline.
    """
    assert isinstance(text, str)

    uv_top_left = np.array(uv_top_left, dtype=float)
    assert uv_top_left.shape == (2,)

    for line in text.splitlines():
        (w, h), _ = cv2.getTextSize(
            text=line,
            fontFace=fontFace,
            fontScale=fontScale,
            thickness=thickness,
        )
        uv_bottom_left_i = uv_top_left + [0, h]
        org = tuple(uv_bottom_left_i.astype(int))

        if outline_color is not None:
            cv2.putText(
                img,
                text=line,
                org=org,
                fontFace=fontFace,
                fontScale=fontScale,
                color=outline_color,
                thickness=thickness * 3,
                lineType=cv2.LINE_AA,
            )
        cv2.putText(
            img,
            text=line,
            org=org,
            fontFace=fontFace,
            fontScale=fontScale,
            color=color,
            thickness=thickness,
            lineType=cv2.LINE_AA,
        )

        uv_top_left += [0, h * line_spacing]


def show_webcam(mirror=False):
    cap = cv2.VideoCapture('/home/micha/Downloads/Japanoschlampen.mp4')

    if (cap.isOpened() == False):
        print("Error opening video stream or file")
        # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
            # Display the resulting frame

        to_ascii(frame)
        cv2.imshow('Frame', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def rand_string():
    density = ''
    i = 0
    while i < 11:
        i += 1
        random_char_ord = random.randrange(40, 10000)
        try:
            rand_char = chr(random_char_ord)
            density += rand_char
        except UnicodeEncodeError:
            i -= 1
    return density


def generate_empty_image():

    return np.zeros(shape=(1024, 2048, 3), dtype=np.int8)


def main(argv):

    # if argv[0] == 'webcam':
    # elif argv[0] == #path to file to transform video or pic
    random = False
    if len(argv[0]) > 0:
        if argv[0] == 'rand':
            random = True
            density = rand_string()
        elif argv[0] == 'norm':
            density = 'Ñ@#W$9876543210?!abc;:+=-,._ '[::-1]
        elif argv[0] == 'b2s':
            density = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'.  '
        elif argv[0] == 's2b':
            density = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'.  '[::-1]

    video = 1
    if len(argv[1]) > 0:
        if argv[1] == 'droid':
            video = 0
        if argv[1] == 'webcam':
            video = 1

    cam = cv2.VideoCapture(video)
    ret_val, image = cam.read()

    width = image.shape[0]
    height = image.shape[1]
    print(height, width)

    adjusted_h = height // 4
    adjusted_w = width // 8

    # the steps in which a pixel is evaluated as a char
    # for each 'jump' in the intensity of a given pixel the char is diffrent
    jump = ceil(255 / len(density))

    j = 0
    while True:

        if random:
            j += 1
            if j % 100 == 0:
                density = rand_string()

        ret_val, img = cam.read()

        # adjust size
        new_image = cv2.resize(img, (adjusted_h, adjusted_w))

        # single Channel
        gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

        my_interpretation = ''
        for x in range(0, adjusted_w):
            for y in range(0, adjusted_h):
                num = gray[x, y].astype(int)
                ascii_representation = density[num // jump]
                my_interpretation += ascii_representation
            my_interpretation += '\n'

    print(my_interpretation)

def to_ascii(appearance=1, source='webcam'):

    if appearance == 0:
        density = rand_string()
    elif appearance == 1:
        density = '$987654321?abc+-_ '[::-1] # 'Ñ@#W$9876543210?!abc;:+=-,._ '[::-1]
    elif appearance == 2:
        density = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'.  '
    elif appearance == 3:
        density = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'.  '[::-1]

    
    if source == 'droidcam':
        video = 0
    elif source == 'webcam':
        video = 1

    cam = cv2.VideoCapture(video)
    ret_val, image = cam.read()

    width = image.shape[0]
    height = image.shape[1]
    print(height, width)

    adjusted_h = height // 4
    adjusted_w = width // 8

    # the steps in which a pixel is evaluated as a char
    # for each 'jump' in the intensity of a given pixel the char is diffrent
    jump = ceil(255 / len(density))

    j = 0
    while True:

        if appearance == 0:
            j += 1
            if j % 100 == 0:
                density = rand_string()

        ret_val, img = cam.read()

        # adjust size
        new_image = cv2.resize(img, (adjusted_h, adjusted_w))

        # single Channel
        gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

        my_interpretation = ''
        for x in range(0, adjusted_w):
            for y in range(0, adjusted_h):
                num = gray[x, y].astype(int)
                ascii_representation = density[num // jump]
                my_interpretation += ascii_representation
            my_interpretation += '\n'

        print(my_interpretation)



if __name__ == "__main__":
    # show_webcam()
    to_ascii(appearance=1, source='webcam')
    #appearance 
    # 0 = rand
    # 1 = norm
    # 2 = advanced
    # 3 = advanced backwards