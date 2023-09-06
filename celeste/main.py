import mss.tools
import cv2 as cv
import numpy as np
from PIL import Image


HTBX_COLOR = (0, 255, 0)
DNG_ZONE_COLOR = (178, 0, 0)
BG_HTBX_COLOR = (255, 135, 85)
BG_COLOR = (0, 0, 0)

CHAR_DIMS = (24, 27)
CHAR_DIMS_CROUCH = (24, 12)

cur_pos = new_pos = (-1, -1)

bounding_box = {'top': 40, 'left': 0, 'width': 955, 'height': 535}
template = cv.imread('char.png', cv.IMREAD_COLOR)
sct = mss.mss()
sct_img = sct.grab(bounding_box)  # screen capture
pixels = np.array(sct_img)
pixels = cv.cvtColor(pixels, cv.COLOR_RGB2BGR)


def get_char_pos():
    res = cv.matchTemplate(pixels, template, 2)
    return cv.minMaxLoc(res)[3]  # return maxloc

def compose_bg_matrix(img):
    bg = []
    for y in range(bounding_box['height']):
        col_bg = []
        for x in range(bounding_box['width']):
            if img.pixel(x, y) == BG_HTBX_COLOR:
                col_bg.append(100)
            elif img.pixel(x, y) == DNG_ZONE_COLOR:
                col_bg.append(200)
            else:
                col_bg.append(0)
        bg.append(col_bg)
    return bg

def main():
    image_matrix = np.array(compose_bg_matrix(sct_img))
    # image = Image.fromarray(image_matrix, 'L')
    # image.save('bg.png')
    # output = "sct-{top}x{left}_{width}x{height}.png".format(**bounding_box)
    # mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)


if __name__ == "__main__":
    main()
