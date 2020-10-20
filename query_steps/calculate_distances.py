import os
import json
import math

def distance(query_data):

    curr_directory=os.getcwd()

    with open(os.path.join(curr_directory, 'normalized_features.json'), 'r') as f:
        data = json.load(f)

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
    distances=[]
    image_index=[]
    counter=0

    for shape in data.items():
        total_distance = 0
        for query_image in query_data.items():
            min_distance = math.inf 
            for image in shape[1]:
                distance = 0
                for feature in features:
                    distance += (shape[1][str(image)][features[i]] - query_image[1][features[i]])**2
                distance = math.sqrt(distance)
                if distance < min_distance:
                    min_distance = distance
            total_distance += min_distance

        for image in shape[1]:
            min_distance = math.inf 
            for query_image in query_data.items():
                distance = 0
                for i in range(len(features)):
                    distance += (shape[1][str(image)][features[i]] - query_image[1][features[i]])**2
                distance = math.sqrt(distance)
                if distance < min_distance:
                    min_distance = distance
            total_distance += min_distance

        distances.append(total_distance)
        image_index.append(counter)
        counter+=1

    distances, image_index = (list(t) for t in zip(*sorted(zip(distances, image_index))))
    print("The closest 3 matching shapes are: " + list(data.keys())[image_index[0]] + " "+ list(data.keys())[image_index[1]] + " " + list(data.keys())[image_index[2]])