import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

imageName = 'a1.png'

image = cv.imread(imageName)

######k-means

Z = image.reshape((-1, 3))
Z = np.float32(Z)

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 2
ret, label, center = cv.kmeans(Z, K, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape(image.shape)


plt.imshow(res2)
plt.show()