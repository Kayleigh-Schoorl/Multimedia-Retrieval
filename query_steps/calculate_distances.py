import os
import json
import math
from pynndescent import NNDescent
import numba
import numpy as np
import pickle

def distance_exact(query_data):

    curr_directory=os.getcwd()
    with open(os.path.join(curr_directory, 'config', 'normalized_features.json'), 'r') as f:
        dataset = json.load(f)

    distances=[]
    image_index=[]
    counter=0

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

    for shape in dataset:
        total_distance = 0

        for query_image in query_data.values():
            min_distance = math.inf 
            for image in dataset.get(shape).values():
                distance = 0
                for i in range(len(features)):
                    distance += float(weights[i]) * (image.get(features[i]) - query_image.get(features[i]))**2
                distance = math.sqrt(distance)
                if distance < min_distance:
                    min_distance = distance
            total_distance += min_distance

        for image in dataset.get(shape).values():
            min_distance = math.inf 
            for query_image in query_data.values():
                distance = 0
                for i in range(len(features)):
                    distance += float(weights[i]) * (image.get(features[i]) - query_image.get(features[i]))**2
                distance = math.sqrt(distance)
                if distance < min_distance:
                    min_distance = distance
            total_distance += min_distance

        distances.append(total_distance)
        image_index.append(counter)
        counter += 1
        
    distances, image_index = (list(t) for t in zip(*sorted(zip(distances, image_index))))

    neighbor_names = []
    count = 1
    for i in range(8):
        found_shape = list(dataset.keys())[image_index[i]]
        neighbor_names.append(found_shape)
        print("Found shape number " + str(count) + " is: " + found_shape)
        count += 1
    return neighbor_names, distances[:8]
    
def distance_ann(query_data):

    curr_directory = os.getcwd()
    dataset_names = pickle.load( open( os.path.join(curr_directory, 'config', "dataset_names.p"), "rb" ) )

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

    index = pickle.load( open( os.path.join(curr_directory, 'config', "ann_model.p"), "rb" ) )
    results = index.query(np.array([query_features]), k=8)

    neighbors = results[0][0]
    distances = results[1][0]

    count = 1
    neighbor_names = []
    for neighbor in neighbors:
        found_shape_name = dataset_names[neighbor]
        neighbor_names.append(found_shape_name)
        print("Found shape number " + str(count) + " is: " + found_shape_name)
        count += 1

    return neighbor_names, distances

def distance(query_data, exact=False):
    if exact == False:
        return distance_ann(query_data)
    else:
        return distance_exact(query_data)