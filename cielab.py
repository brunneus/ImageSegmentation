import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def rgbToCielab(rgb_image):

    r = rgb_image[:, :, 2]
    g = rgb_image[:, :, 1]
    b = rgb_image[:, :, 0]

    r = np.double(r) / 255
    g = np.double(g) / 255
    b = np.double(b) / 255

    T = 0.008856

    M, N = r.shape
    S = M * N
    RGB = np.array([r.reshape(1, S).flatten(), g.reshape(1, S).flatten(), b.reshape(1, S).flatten()])

    MAT = np.array([
        [0.412453, 0.357580, 0.180423],
        [0.212671, 0.715160, 0.072169],
        [0.019334, 0.119193, 0.950227]])

    XYZ = np.dot(MAT, RGB)

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

    L = np.reshape(YT * (116.0 * Y3 - 16.0) + np.logical_not(YT) * (903.30 * Y), [M, N])
    a = np.reshape(500 * (fX - fY), [M, N])
    b = np.reshape(200 * (fY - fZ), [M, N])

    return np.stack((L, a, b), 2)

def rgbToCielabPixelByPixel(rgb_image):

    r = rgb_image[:, :, 2]
    g = rgb_image[:, :, 1]
    b = rgb_image[:, :, 0]

    r = np.double(r) / 255
    g = np.double(g) / 255
    b = np.double(b) / 255

    T = 0.008856

    M, N = r.shape
    S = M * N
    RGB = np.array([r.reshape(1, S).flatten(), g.reshape(1, S).flatten(), b.reshape(1, S).flatten()])

    MAT = np.array([
        [0.412453, 0.357580, 0.180423],
        [0.212671, 0.715160, 0.072169],
        [0.019334, 0.119193, 0.950227]])

    XYZ = np.dot(MAT, RGB)

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

    L = np.reshape(YT * (116.0 * Y3 - 16.0) + np.logical_not(YT) * (903.30 * Y), [M, N])
    a = np.reshape(500 * (fX - fY), [M, N])
    b = np.reshape(200 * (fY - fZ), [M, N])

    return np.stack((L, a, b), 2)