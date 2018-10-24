import cv2 as cv
import numpy as np
from cielab import rgbToCielab
from backgroundRemover import removeBackground
import ntpath

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def segment_image(imageName, pixel_size, x, y, width, height):

    image = cv.imread(imageName)
    image = image[y: y + height, x: x + width]

    image, leaf_pixel_count = removeBackground(image)
    semb = imageName.split('.')[0] + "_" + '.png'
    test = cv.cvtColor(image, cv.COLOR_RGB2Lab);
    cv.imwrite(semb, test)
    # image = cv.medianBlur(image, 5)

    image = rgbToCielab(image) * 255
    cielabImagePathName = imageName.split('.')[0] + "_cielab" + '.png'
    cv.imwrite(cielabImagePathName, image)

    image = cv.imread(cielabImagePathName)
    # os.remove(cielabImagePathName)

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
    diseasePixelsCount = 0

    for i in range(height):
        for j in range(width):
            if np.array_equal(res2[i, j], diseaseCenter):
                diseasePixels[i, j] = [0, 0, 0]
                diseasePixelsCount += 1

    image_result_path = imageName.split('.')[0] + 'result' + '.png'

    cv.imwrite(image_result_path, diseasePixels)

    percentage_of_leaf_infected = (diseasePixelsCount / (leaf_pixel_count * 1.0)) * 100

    # print diseasePixelsCount * float(pixel_size)

    return image_result_path, percentage_of_leaf_infected, diseasePixelsCount * float(pixel_size)
