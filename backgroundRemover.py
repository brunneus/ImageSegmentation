import cv2 as cv
import numpy as np

def removeBackground(image):
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    height, width = gray_image.shape

    ret2, th2 = cv.threshold(gray_image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    leaf_pixels = np.zeros((height, width, 3), np.uint8) + 255

    leaf_pixels_count = 0

    for i in range(height):
        for j in range(width):
            if th2[i, j] != 255:
                leaf_pixels[i, j] = image[i, j]
                leaf_pixels_count += 1

    return leaf_pixels, leaf_pixels_count


def remove_by_k_means(image):
    Z = image.reshape((-1, 3))
    Z = np.float32(Z)

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 2
    ret, label, center = cv.kmeans(Z, K, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape(image.shape)

    plt.imshow(image)
    plt.show()

    return res2
