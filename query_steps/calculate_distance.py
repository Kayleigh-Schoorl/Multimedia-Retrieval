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


    for shape in data.items():
        for image in shape[1]:
            for query_image in query_data.items():
                for feature in features:
                    distance+=math.sqrt(abs((shape[1][str(image)][feature])**2 - (query_image[1][feature])**2))

                distances.append(distance)
                image_index.append(counter)
                distance = 0
        counter+=1

    minpos = distances.index(min(distances))
    print(distances)
    print("closest match is shape number  "+str(image_index[minpos])+"  with a distance of  "+str(distances[minpos]))