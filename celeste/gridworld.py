from mss import mss
from PIL import Image#, ImageDraw
# import threading
import numpy as np
# import cv2

bounding_box = {'top': 50, 'left': 0, 'width': 600, 'height': 450}

HTBX_COLOR = (0, 255, 0)
DNG_ZONE_COLOR = (178, 0, 0)
BG_HTBX_COLOR = (255, 135, 85)
BG_COLOR = (0, 0, 0)

cur_pos = new_pos = (-1, -1)


def get_hitbox_upper_corner(img) -> tuple:
    # start_x = 0 if cur_pos[0] == -1 else cur_pos[0] - 100
    # end_x = bounding_box['width'] if cur_pos[0] == -1 else cur_pos[0] + 100
    # start_y = 0 if cur_pos[1] == -1 else cur_pos[1] - 100
    # end_y = bounding_box['height'] if cur_pos[1] == -1 else cur_pos[1] + 100
    for x in range(bounding_box['width']):
        for y in range(bounding_box['height']):
            if img.pixel(x, y) == HTBX_COLOR:
                return (x, y)
    return (-1, -1)


def compose_bg_matrix(img):
    bg = [[0] * bounding_box['height']] * bounding_box['width']
    for x in range(bounding_box['width']):
        for y in range(bounding_box['height']):
            if img.pixel(x, y) == BG_HTBX_COLOR:
                bg[x][y] = 100
            elif img.pixel(x, y) == BG_HTBX_COLOR:
                bg[x][y] = 200
    return bg


def get_all_colors(img):
    res = set()
    for i in img.pixels:
        for j in i:
            res.add(j)
    # for i in range(10):
    #     print(img.pixels[0][i])
    # print(set(img.pixels[0]))
    # print(res)
    print(len(res))


sct = mss()
img = sct.grab(bounding_box)
# get_all_colors(img)
# print(img.pixels)
# print(compose_bg_matrix(sct.grab(bounding_box)))

# image_matrix = np.array(compose_bg_matrix(img))
image = Image.fromarray(img, 'RGB')
# image .save('image-grad.jpg')
# image = Image.fromarray(image_matrix, 'L')
image.save('bg.jpg')

# while True:
    # cv2.imshow('screen', np.array(sct_img))
    # new_pos = get_hitbox_upper_corner(sct.grab(bounding_box))
    # if cur_pos != new_pos:
    #     print(new_pos)
    #     cur_pos = new_pos
