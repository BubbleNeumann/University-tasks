from mss import mss
# import numpy as np
# import cv2

bounding_box = {'top': 50, 'left': 0, 'width': 600, 'height': 450}

HTBX_COLOR = (0, 255, 0)
BG_COLOR = (0, 0, 0)

cur_pos = new_pos = (-1, -1)


def get_hitbox_upper_corner(img) -> tuple:
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if img.pixel(x, y) == HTBX_COLOR:
                return (x, y)
    return (-1, -1)


sct = mss()
while True:
    # cv2.imshow('screen', np.array(sct_img))
    new_pos = get_hitbox_upper_corner(sct.grab(bounding_box))
    if cur_pos != new_pos:
        print(new_pos)
        cur_pos = new_pos
