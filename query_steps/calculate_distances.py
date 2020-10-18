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
    distance=0
    distances=[]
    image_index=[]
    counter=0
    cnt=0

    for shape in data.items():
        for image in shape[1]:
            for query_image in query_data.items():
                for feature in features:
                    distance+=math.sqrt(abs((shape[1][str(image)][feature])**2 - (query_image[1][feature])**2))
                cnt+=1
        distance=distance/cnt
        distances.append(distance)
        image_index.append(counter)
        distance = 0
        cnt=0
        counter+=1

    distances, image_index = (list(t) for t in zip(*sorted(zip(distances, image_index))))
    #minpos = distances.index(min(distances))
    print(image_index)
    print(distances)
    print("closest 3 matching shapes are:  "+ list(data.keys())[image_index[0]] +"   "+ list(data.keys())[image_index[1]]+"   "+ list(data.keys())[image_index[2]])