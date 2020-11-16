import os
import json
import math
import random
from pynndescent import NNDescent
import numpy as np
import numba
import pickle


@numba.jit(nopython=True)
def distance_computation(v1, v2):

    features = ["area",
            "perimeter",
            "compactness",
            "circularity",
            "centroid_x",
            "centroid_y",
            "bounding_box_x",
            "bounding_box_y",
            "bounding_box_w",
            "bounding_box_h",
            "rectangularity",
            "diameter",
            "eccentricity",
            "skeleton_length"]

    weights = [0.2,0.01,0.01,0.01,0.01,0.01,0.01,1,0.8,0.01,0.05,0.5,0.4,1]

    no_features = 14
    v1_images = [v1[i:i + no_features] for i in range(0, len(v1), no_features)]
    v2_images = [v2[i:i + no_features] for i in range(0, len(v2), no_features)]

    total_distance = 0
    for query_image in v1_images:
        min_distance = math.inf 
        for image in v2_images:
            distance = 0
            for i in range(no_features):
                distance += float(weights[i]) * (query_image[i] - image[i])**2
            distance = np.sqrt(distance)
            if distance < min_distance:
                min_distance = distance
        total_distance += min_distance

    for image in v2_images:
        min_distance = math.inf 
        for query_image in v1_images:
            distance = 0
            for i in range(no_features):
                distance += (query_image[i] - image[i])**2
            distance = np.sqrt(distance)
            if distance < min_distance:
                min_distance = distance
        total_distance += min_distance

    return total_distance

curr_directory=os.getcwd()
with open(os.path.join(curr_directory, 'config', 'normalized_features.json'), 'r') as f:
    data = json.load(f)

dataset = []
dataset_names = []
for shape_name in data:
    shape_features = []
    shape = data.get(shape_name)
    for image in shape:
        image_data = shape.get(image)
        for feature in image_data:
            shape_features.append(image_data.get(feature))
    dataset.append(shape_features)
    dataset_names.append(shape_name)

index = NNDescent(np.array(dataset), metric=distance_computation)
index.prepare()
pickle.dump( index, open( os.path.join(curr_directory, 'config', 'ann_model.p'), "wb" ) )

pickle.dump( dataset_names, open( os.path.join(curr_directory, 'config', 'dataset_names.p'), "wb" ) )
