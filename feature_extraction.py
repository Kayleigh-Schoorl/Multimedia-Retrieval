import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

curr_directory = os.getcwd()
db_path = os.path.join(curr_directory, "images", "bw")

for folder in os.listdir(db_path):
    if folder.startswith("."):
        continue

    for filename in os.listdir(os.path.join(db_path, folder)):

        if "Vase" not in filename:
            continue

        print(filename + "\n")

        # Read image
        image_original = cv2.imread(os.path.join(db_path, folder, filename),0)
        image = cv2.bitwise_not(image_original)

        # Get area 
        area = cv2.countNonZero(image)
        print("Area: " + str(area))

        # Get perimeter (only outer perimeter)
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        perimeter = int(cv2.arcLength(contours[0],True))
        print("Perimeter: " + str(perimeter))

        # Compute compactness
        area_2 = cv2.contourArea(contours[0])
        compactness = (perimeter ** 2) / (4 * math.pi * area_2)
        print("Compactness: " + str(compactness))

        # Compute circularity
        circularity = 1 / compactness
        print("Circularity: " + str(circularity))

        # Get axis-aligned bounding box
        x,y,w,h = cv2.boundingRect(contours[0])
        print("\nAxis-aligned bounding box:")
        print("Top-left coordinate: (" + str(x) + ", " + str(y) + ")")
        print("Width: " + str(w))
        print("Height: " + str(h) + "\n")

        # Compute rectangularity (using object oriented bounding box)
        rect = cv2.minAreaRect(contours[0])
        rectangularity = area_2 / (rect[1][0] * rect[1][1])
        print("Rectangularity: " + str(rectangularity))

        # Get diameter
        _,radius = cv2.minEnclosingCircle(contours[0])
        diameter = radius*2
        print("Diameter: " + str(diameter))

        # Compute eccentricity
        _,(MA,ma),angle = cv2.fitEllipse(contours[0])
        eccentricity = MA / ma
        print("Eccentricity: " + str(eccentricity))

        print("\n\n")
