import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from utils import show_image

def rgb_to_lab(rgb):
    # Conversion Matrix
    T = 0.008856

    rgb[0] = rgb[0] / 255
    rgb[1] = rgb[1] / 255
    rgb[2] = rgb[2] / 255

    MAT = np.array([
        [0.412453, 0.357580, 0.180423],
        [0.212671, 0.715160, 0.072169],
        [0.019334, 0.119193, 0.950227]])

    XYZ = np.dot(MAT, rgb)

    X = XYZ[0] / 0.950456
    Y = XYZ[1]
    Z = XYZ[2] / 1.088754

    XT = X > T
    YT = Y > T
    ZT = Z > T

    Y3 = Y ** (1 / 3.0)

    fX = XT * (X ** (1 / 3.0)) + np.logical_not(XT) * (7.787 * X + (16 / 116.0))
    fY = YT * Y3 + (np.logical_not(YT)) * (7.787 * Y + 16 / 116.0)
    fZ = ZT * (Z ** (1 / 3.0)) + np.logical_not(ZT) * (7.787 * Z + (16 / 116.0))

    L = YT * (116.0 * Y3 - 16.0) + np.logical_not(YT) * (903.30 * Y)
    a = 500 * (fX - fY)
    b = 200 * (fY - fZ)

    return np.array([L, a, b])


rgbImage = cv.imread('a1.png')
h, w, d = rgbImage.shape

labPixels = np.zeros((h, w, 3), np.uint8)

for i in range(h):
     for j in range(w):
         labPixels[i, j] = rgb_to_lab(rgbImage[i, j])

show_image(labPixels)
