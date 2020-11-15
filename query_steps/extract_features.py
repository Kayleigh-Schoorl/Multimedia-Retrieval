import cv2
import numpy as np
import os
import math
import json

def extract(mesh):
    curr_directory = os.getcwd()
    data = {}
    for filename in os.listdir(os.path.join(curr_directory, "renders")):
        if filename.startswith("."):
            continue

        extension = os.path.splitext(filename)[1]
        mesh_name = os.path.splitext(filename)[0]

        if extension != ".png":
            continue

        image = cv2.imread(os.path.join(curr_directory, "renders", filename))
        (thresh, image) = cv2.threshold(image, 254, 255, cv2.THRESH_BINARY)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.bitwise_not(image)

        features = {}

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

        # Normalization
        with open(os.path.join(curr_directory, 'config', 'averages.json'), 'r') as f:
            averages = json.load(f)
        with open(os.path.join(curr_directory, 'config', 'stdevs.json'), 'r') as f:
            stdevs = json.load(f)

        normalized_features = {}

        for feature in features:
            normalized_features[feature] = (features.get(feature) - averages.get(feature)) / stdevs.get(feature)
        
        number = mesh_name.split("_")[1]
        data[number] = normalized_features

    if os.path.exists(os.path.join(curr_directory, "renders")):
        for filename in os.listdir(os.path.join(curr_directory, "renders")):
            os.remove(os.path.join(curr_directory, "renders", filename))
        os.rmdir(os.path.join(curr_directory, "renders"))
    return data