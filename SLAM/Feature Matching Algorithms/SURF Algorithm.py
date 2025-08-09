import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

def SIFT():
    img_path = os.path.join(os.getcwd(), "tesla.png")
    imgGray = cv.imread(img_path, cv.IMREAD_GRAYSCALE)

    if imgGray is None:
        print("❌ Image not found. Make sure 'tesla.png' exists in the current directory.")
        return

    sift = cv.SIFT_create()
    keypoints = sift.detect(imgGray, None)

    img_with_keypoints = cv.drawKeypoints(
        imgGray, keypoints, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )

    plt.figure()
    plt.imshow(img_with_keypoints, cmap='gray')
    plt.title("SIFT Keypoints")
    plt.axis('off')
    plt.show()

SIFT()
