import mss.tools
import numpy as np
import cv2 as cv

# environment globals
bounding_box = {'top': 135, 'left': 345, 'width': 400, 'height': 400}

# capture screen
sct = mss.mss()
im = np.array(sct.grab(bounding_box))

# convert to grayscale
# gray_img = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
# print(gray_img.shape)

# scale image
# :

cv.imshow('pico fuckkk', im)
cv.waitKey(0)


# find the character on the screen
# template = cv.cvtColor(cv.imread('char_template.png'), cv.COLOR_BGR2GRAY)
template = cv.imread('char_template.png')

# cv.imshow('pico char', template)
# cv.waitKey(0)
res = cv.matchTemplate(im, template, 2)

_minVal, _maxVal, _minLoc, _maxLoc = cv.minMaxLoc(res, None)

# -1.5 11863070.0 (246, 301) (324, 95)
print(_minVal, _maxVal, _minLoc, _maxLoc)
