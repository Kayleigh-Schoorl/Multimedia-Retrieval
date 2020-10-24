import os
import json
import math
from pynndescent import NNDescent
import numba
import numpy as np

@numba.jit(nopython=True)
def distance_computation(v1, v2):
    no_features = 14
    v1_images = [v1[i:i + no_features] for i in range(0, len(v1), no_features)]
    v2_images = [v2[i:i + no_features] for i in range(0, len(v2), no_features)]

    total_distance = 0
    for query_image in v1_images:
        min_distance = math.inf 
        for image in v2_images:
            distance = 0
            for i in range(no_features):
                distance += (query_image[i] - image[i])**2
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


def distance(query_data):

    curr_directory=os.getcwd()

    with open(os.path.join(curr_directory, 'normalized_features.json'), 'r') as f:
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

    query_features = []
    for image in query_data:
        image_features = query_data.get(image)
        for feature in image_features:
            query_features.append(image_features.get(feature))

    neighbors = index.query(np.array([query_features]), k=5)[0][0]
    count = 1
    neighbor_names = []
    for neighbor in neighbors:
        found_shape_name = dataset_names[neighbor]
        neighbor_names.append(found_shape_name)
        print("Found shape number " + str(count) + " is: " + found_shape_name)
        count += 1

    return neighbor_names