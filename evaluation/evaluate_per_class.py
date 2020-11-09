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

    k = 8
    index = pickle.load( open( os.path.join(curr_directory, "ann_model.p"), "rb" ) )
    neighbors = index.query(np.array(dataset), k=k+1, )[0]

    for i in range(len(neighbors)):
        name = dataset_names[i]
        correct_class = name.split("_")[0]
        if correct_class not in class_count:
            class_count[correct_class] = [k,0,1]
        else:
            class_count[correct_class][0] += k
            class_count[correct_class][2] += 1
            
        count = 0
        for found_shape in neighbors[i]:
            if count >= k:
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

    all_recall = []
    all_accuracy = []
    for class_acc in class_count:
        no_in_class = class_count.get(class_acc)[2]
        accuracy = (class_count.get(class_acc)[1] + ((len(data)-1)*no_in_class - (no_in_class-1)**2 - (k*(no_in_class-1) - class_count[correct_class][1]))) / ((len(data)-1)*no_in_class)
        print("Accuracy for class " + class_acc + ": " + str(accuracy))
        all_accuracy.append(accuracy)
        precision = class_count.get(class_acc)[1] / class_count.get(class_acc)[0]
        print("Precision for class " + class_acc + ": " + str(precision))
        recall = class_count.get(class_acc)[1] / (class_count.get(class_acc)[2])**2
        print("Recall for class " + class_acc + ": " + str(recall))
        all_recall.append(recall)
        print("F1 score for class " + class_acc + ": " + str(2 * (recall * precision / (recall + precision))) + "\n")
    

    overall_accuracy = sum(all_accuracy) / len(class_count)
    print("Overall accuracy: " + str(overall_accuracy))
    overall_precision = correct_count / test_count
    print("Overall precision: " + str(overall_precision))
    overall_recall = sum(all_recall) / len(class_count)
    print("Overall recall: " + str(overall_recall))
    print("Overall F1 score: " + str(2 * (overall_recall * overall_precision / (overall_precision + overall_recall))))


if __name__ == "__main__":
    os.chdir("..")
    evaluate_knn()
