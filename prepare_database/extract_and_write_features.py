import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import time
import json

os.chdir("..")
curr_directory = os.getcwd()
db_path = os.path.join(curr_directory, "images", "bw")

data = {}

for folder in os.listdir(db_path):
    if folder.startswith("."):
        continue

    for filename in os.listdir(os.path.join(db_path, folder)):

        # if "_1_" not in filename:
        #     continue

        features = {}

        # Read image
        image_original = cv2.imread(os.path.join(db_path, folder, filename),0)
        image = cv2.bitwise_not(image_original)

        # Get area 
        area = cv2.countNonZero(image)
        features["area"] = area

        # Get perimeter (total for all contours)
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        perimeter = 0
        for contour in contours:
            perimeter += int(cv2.arcLength(contour,True))
        features["perimeter"] = perimeter

        # Compute compactness
        compactness = (perimeter ** 2) / (4 * math.pi * area)
        features["compactness"] = compactness

        # Compute circularity
        circularity = 1 / compactness
        features["circularity"] = circularity

        # Compute centroid
        major_contour = contours[0]
        for contour in contours:
            if int(cv2.arcLength(contour,True)) > int(cv2.arcLength(major_contour,True)):
                major_contour = contour
        M = cv2.moments(major_contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        features["centroid_x"] = cX
        features["centroid_y"] = cY

        # Get axis-aligned bounding box
        x,y,w,h = cv2.boundingRect(major_contour)
        features["bounding_box_x"] = x        
        features["bounding_box_y"] = y
        features["bounding_box_w"] = w
        features["bounding_box_h"] = h

        # Compute rectangularity (using object oriented bounding box)
        rect = cv2.minAreaRect(major_contour)
        rectangularity = area / (rect[1][0] * rect[1][1])
        features["rectangularity"] = rectangularity

        # Get diameter
        _,radius = cv2.minEnclosingCircle(major_contour)
        diameter = radius*2
        features["diameter"] = diameter

        # Compute eccentricity
        if len(major_contour) < 5:
            features["eccentricity"] = 0
        else:
            _,(MA,ma),angle = cv2.fitEllipse(major_contour)
            eccentricity = MA / ma
            features["eccentricity"] = eccentricity

        # Get length of skeleton
        # Install library opencv-contrib-python to use this!
        skeleton = cv2.ximgproc.thinning(image, thinningType=1)
        skeleton_length = cv2.countNonZero(skeleton)
        features["skeleton_length"] = skeleton_length

        split_filename = filename.split("_")
        name = split_filename[0] + "_" + split_filename[1] + "_" + split_filename[2]
        print(name)
        data[name] = features

with open(os.path.join(curr_directory, 'config', 'features.json'), 'w') as f:
    json.dump(data, f, sort_keys=True)

