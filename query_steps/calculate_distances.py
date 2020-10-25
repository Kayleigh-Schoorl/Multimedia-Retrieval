import os
import json
import math
from pynndescent import NNDescent
import numba
import numpy as np
import pickle

def distance(query_data):

    curr_directory = os.getcwd()
    with open(os.path.join(curr_directory, 'normalized_features.json'), 'r') as f:
        data = json.load(f)

    dataset_names = []
    for shape_name in data:
        dataset_names.append(shape_name)

    query_features = []
    for image in query_data:
        image_features = query_data.get(image)
        for feature in image_features:
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