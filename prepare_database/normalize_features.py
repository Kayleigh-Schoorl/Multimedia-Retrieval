import json
import os
import statistics 

os.chdir("..")
curr_directory = os.getcwd()
with open(os.path.join(curr_directory, 'config', 'features.json'), 'r') as f:
    data = json.load(f)

feature_data = {}
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

for mesh in data.items():
    for feature in features:
        if feature not in feature_data:
            feature_data[feature] = [mesh[1].get(feature)]
        else:
            feature_data[feature].append(mesh[1].get(feature))

average = {}
stdev = {}
for feature in features:
    average[feature] = statistics.mean(feature_data.get(feature))
    stdev[feature] = statistics.stdev(feature_data.get(feature))

with open(os.path.join(curr_directory, 'config', 'averages.json'), 'w') as f:
    json.dump(average, f, sort_keys=True)
with open(os.path.join(curr_directory, 'config', 'stdevs.json'), 'w') as f:
    json.dump(stdev, f, sort_keys=True)

normalized_data = {}
for image in data.items():
    for feature in features:
        normalized_value = (image[1].get(feature) - average.get(feature)) / stdev.get(feature)
        image[1][feature] = normalized_value
    mesh = image[0].split("_")
    mesh_name = mesh[0] + "_" + mesh[1]
    if mesh_name not in normalized_data:
        normalized_data[mesh_name] = {}
    normalized_data[mesh_name][mesh[2]] = image[1]

with open(os.path.join(curr_directory, 'config', 'normalized_features.json'), 'w') as f:
    json.dump(normalized_data, f, sort_keys=True)

