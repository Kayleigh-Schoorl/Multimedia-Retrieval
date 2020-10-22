import os
import json
import math
import random
from pynndescent import NNDescent
import numpy as np
import numba

os.chdir("..")
curr_directory=os.getcwd()

with open(os.path.join(curr_directory, 'normalized_features.json'), 'r') as f:
    dataset = json.load(f)

dataset_classes = {}
for shape in dataset:
    class_name = shape.split("_")[0]
    if class_name not in dataset_classes:
        dataset_classes[class_name] = {shape: dataset.get(shape)}
    else:
        dataset_classes.get(class_name)[shape] = dataset.get(shape)

training_set = []
training_set_names = []

test_set = []
test_set_names = []

for shape_class in dataset_classes:
    class_shapes = dataset_classes.get(shape_class)
    keys = list(class_shapes.keys())
    random.shuffle(keys)
    split_value = int(len(keys) / 4)
    query_shapes = keys[:split_value]
    database_shapes = keys[split_value:]

    for shape_name in query_shapes:
        shape_features = []
        shape = class_shapes.get(shape_name)
        for image in shape:
            image_data = shape.get(image)
            for feature in image_data:
                shape_features.append(image_data.get(feature))
        test_set.append(shape_features)
        test_set_names.append(shape_name)

    for shape_name in database_shapes:
        shape_features = []
        shape = class_shapes.get(shape_name)
        for image in shape:
            image_data = shape.get(image)
            for feature in image_data:
                shape_features.append(image_data.get(feature))
        training_set.append(shape_features)
        training_set_names.append(shape_name)


@numba.jit(nopython=True)
def distance_computation(v1, v2):
    no_features = 14
    v1_images = [v1[i:i + no_features] for i in range(0, len(v1), no_features)]
    v2_images = [v2[i:i + no_features] for i in range(0, len(v2), no_features)]

    total_distance = 0
    for query_image in v1_images:
        min_distance = 1000000 
        for image in v2_images:
            distance = 0
            for i in range(no_features):
                distance += (query_image[i] - image[i])**2
            distance = np.sqrt(distance)
            if distance < min_distance:
                min_distance = distance
        total_distance += min_distance

    for image in v2_images:
        min_distance = 1000000 
        for query_image in v1_images:
            distance = 0
            for i in range(no_features):
                distance += (query_image[i] - image[i])**2
            distance = np.sqrt(distance)
            if distance < min_distance:
                min_distance = distance
        total_distance += min_distance

    return total_distance


index = NNDescent(np.array(training_set), metric=distance_computation)

test_count = 0
correct_count = 0
class_count = {}

neighbors = index.query(np.array(test_set), k=5)[0]

for i in range(len(neighbors)):
    name = test_set_names[i]
    correct_class = test_set_names[i].split("_")[0]
    if correct_class not in class_count:
        class_count[correct_class] = [5,0]
    else:
        class_count[correct_class][0] += 5

    for found_shape in neighbors[i]:
        found_shape_name = training_set_names[found_shape]
        found_shape_class = found_shape_name.split("_")[0]
        print("Original shape is " + name + ", found shape is " + found_shape_name)
        if correct_class == found_shape_class:
            correct_count += 1
            class_count[correct_class][1] += 1
        test_count += 1

for class_acc in class_count:
    print("Accuracy for class " + class_acc + ": " + str(class_count.get(class_acc)[1] / class_count.get(class_acc)[0] * 100) + "%")
print("Overall accuracy: " + str(correct_count / test_count * 100) + "%")