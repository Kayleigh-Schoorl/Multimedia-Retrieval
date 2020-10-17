import json
import os
import statistics 

curr_directory = os.getcwd()
with open(os.path.join(curr_directory, 'features.json'), 'r') as f:
    data = json.load(f)

feature_data = []
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

for feature in features:
    feature_data.append([])

for mesh in data.items():
    for i in range(len(features)):
        feature_data[i].append(mesh[1].get(features[i]))

average = []
stdev = []
for feature in feature_data:
    average.append(statistics.mean(feature))
    stdev.append(statistics.stdev(feature))

normalized_data = {}
for image in data.items():
    for i in range(len(features)):
        normalized_value = (image[1].get(features[i]) - average[i]) / stdev[i]
        image[1][features[i]] = normalized_value
    mesh = image[0].split("_")
    mesh_name = mesh[0] + "_" + mesh[1]
    if mesh_name not in normalized_data:
        normalized_data[mesh_name] = {}
    normalized_data[mesh_name][mesh[2]] = image[1]

with open(os.path.join(curr_directory, 'normalized_features.json'), 'w') as f:
    json.dump(normalized_data, f, sort_keys=True)

