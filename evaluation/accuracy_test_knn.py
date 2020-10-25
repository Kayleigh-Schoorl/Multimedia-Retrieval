import os
import json
import math
import random
from pynndescent import NNDescent
import numpy as np
import numba
import pickle

def evaluate_knn():
    curr_directory=os.getcwd()

    with open(os.path.join(curr_directory, 'normalized_features.json'), 'r') as f:
        data = json.load(f)

    dataset_classes = {}
    dataset_names = []
    for shape in data:
        class_name = shape.split("_")[0]
        if class_name not in dataset_classes:
            dataset_classes[class_name] = {shape: data.get(shape)}
        else:
            dataset_classes.get(class_name)[shape] = data.get(shape)
        dataset_names.append(shape)


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

    test_count = 0
    correct_count = 0
    class_count = {}

    index = pickle.load( open( os.path.join(curr_directory, "ann_model.p"), "rb" ) )
    neighbors = index.query(np.array(dataset), k=6, )[0]

    for i in range(len(neighbors)):
        name = dataset_names[i]
        correct_class = name.split("_")[0]
        if correct_class not in class_count:
            class_count[correct_class] = [5,0]
        else:
            class_count[correct_class][0] += 5
            
        count = 0
        for found_shape in neighbors[i]:
            if count >= 5:
                continue

            found_shape_name = dataset_names[found_shape]
            if found_shape_name == name:
                continue

            count += 1
            found_shape_class = found_shape_name.split("_")[0]
            print("Original shape is " + name + ", found shape is " + found_shape_name)

            if correct_class == found_shape_class:
                correct_count += 1
                class_count[correct_class][1] += 1
            test_count += 1

    for class_acc in class_count:
        print("Accuracy for class " + class_acc + ": " + str(class_count.get(class_acc)[1] / class_count.get(class_acc)[0] * 100) + "%")
    print("Overall accuracy: " + str(correct_count / test_count * 100) + "%")


if __name__ == "__main__":
    os.chdir("..")
    evaluate_knn()
