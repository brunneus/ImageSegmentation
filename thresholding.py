import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from cielab import rgbToCielab
from backgroundRemover import removeBackground, remove_by_k_means
from utils import show_image
import os

imageName = 'a1.jpg'
image = cv.imread(imageName)
image = removeBackground(image)
# image = cv.medianBlur(image, 5)

image = rgbToCielab(image) * 255
cielabImagePathName = imageName.split('.')[0] + "_cielab" + '.png'
cv.imwrite(cielabImagePathName, image)

image = cv.imread(cielabImagePathName)
os.remove(cielabImagePathName)

Z = image.reshape((-1, 3))
Z = np.float32(Z)

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 3
ret, label, center = cv.kmeans(Z, K, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape(image.shape)

height, width, _ = image.shape

diseaseCenter = center[0]

if np.sum([255, 255, 255] - center[1]) < np.sum([255, 255, 255] - diseaseCenter):
    diseaseCenter = center[1]

if np.sum([255, 255, 255] - center[2]) < np.sum([255, 255, 255] - diseaseCenter):
    diseaseCenter = center[2]

diseasePixels = np.zeros((height, width, 3), np.uint8) + 255

for i in range(height):
    for j in range(width):
        if np.array_equal(res2[i, j], diseaseCenter):
            diseasePixels[i, j] = [0, 0, 0]

cv.imwrite(imageName.split('.')[0] + 'result' + '.png', diseasePixels)
# show_image(diseasePixels)

