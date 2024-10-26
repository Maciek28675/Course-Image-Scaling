import cv2
import numpy as np

filename = 'dog1.png'
img = cv2.imread(filename)
height, width, _ = img.shape

# Image downscaling

smaller_img = np.zeros((height//2, width//2, 3), np.uint8)

for row in range(0, height - 1, 2):
    for column in range(0, width - 1, 2):
        current_mean_b = img[row][column][0] / 4 + img[row][column + 1][0] / 4 + img[row + 1][column][0] / 4 + img[row + 1][column + 1][0] / 4
        current_mean_g = img[row][column][1] / 4 + img[row][column + 1][1] / 4 + img[row + 1][column][1] / 4 + img[row + 1][column + 1][1] / 4
        current_mean_r = img[row][column][2] / 4 + img[row][column + 1][2] / 4 + img[row + 1][column][2] / 4 + img[row + 1][column + 1][2] / 4

        smaller_img[row//2][column//2][0] = current_mean_b
        smaller_img[row//2][column//2][1] = current_mean_g
        smaller_img[row//2][column//2][2] = current_mean_r

# Image Upscaling

bigger_img = np.zeros((height, width, 3), np.uint8)

# Copy pixels to the bigger image
for row in range(height//2 - 1):
    for column in range(width//2 - 1):
        bigger_img[row*2][column*2] = smaller_img[row][column]

# Interpolate using nearest neigbor method

cv2.imwrite('bigger_image1.png', bigger_img)

# Approximate row by row
for row in range(0, height - 1, 2):
    for column in range(1, width - 1, 2):
        for color in range(3):
            bigger_img[row][column][color] = bigger_img[row][column - 1][color] / 2 + bigger_img[row][column + 1][color] / 2

# Approximate column by column

for column in range(0, width - 1):
    for row in range(1, height - 1, 2):
        for color in range(3):
            bigger_img[row][column][color] = bigger_img[row - 1][column][color] / 2 + bigger_img[row + 1][column][color] / 2

sum_b = sum_g = sum_r = 0

for row in range(height):
    for column in range(width):
        sum_b += float(bigger_img[row][column][0])
        sum_g += float(bigger_img[row][column][1])
        sum_r += float(bigger_img[row][column][2])

mean1 = (sum_b + sum_g + sum_r)/(500*500*3)

for row in range(height):
    for column in range(width):
        sum_b += float(img[row][column][0])
        sum_g += float(img[row][column][1])
        sum_r += float(img[row][column][2])

mean2 = (sum_b + sum_g + sum_r)/(500*500*3)

print(mean2-mean1)

difference = bigger_img - img

cv2.imshow('Image', img)
cv2.imshow('Smaller image', smaller_img)
cv2.imshow('Bigger image', bigger_img)
cv2.imshow('Image difference', difference)
cv2.waitKey(0)

cv2.imwrite('bigger_image.png', bigger_img)
cv2.imwrite('smaller_image.png', smaller_img)
cv2.imwrite('difference.png', difference)
