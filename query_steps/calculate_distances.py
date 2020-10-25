import os
import json
import math
from pynndescent import NNDescent
import numba
import numpy as np
import pickle

def distance(query_data):

    curr_directory = os.getcwd()
    dataset_names = pickle.load( open( os.path.join(curr_directory, "dataset_names.p"), "rb" ) )

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

    features.sort()

    query_features = []
    for image in query_data:
        image_features = query_data.get(image)
        for feature in features:
            query_features.append(image_features.get(feature))

    index = pickle.load( open( os.path.join(curr_directory, "ann_model.p"), "rb" ) )
    neighbors = index.query(np.array([query_features]), k=5)[0][0]

    count = 1
    neighbor_names = []
    for neighbor in neighbors:
        found_shape_name = dataset_names[neighbor]
        neighbor_names.append(found_shape_name)
        print("Found shape number " + str(count) + " is: " + found_shape_name)
        count += 1

    return neighbor_names