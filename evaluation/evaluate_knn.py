import os
import json
import math
import random
from pynndescent import NNDescent
import numpy as np
import numba
import pickle
import matplotlib.pyplot as plt

def evaluate_knn(k):
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

            if correct_class == found_shape_class:
                correct_count += 1
                class_count[correct_class][1] += 1
            test_count += 1

    all_recall = []
    for class_acc in class_count:
        class_recall = class_count.get(class_acc)[1] / (class_count.get(class_acc)[2])**2
        all_recall.append(class_recall)
    

    print("k = " + str(k))
    precision = correct_count / test_count
    print("Overall precision: " + str(precision))
    recall = sum(all_recall) / len(class_count)
    print("Overall recall: " + str(recall))
    F1 = 2 * (recall * precision / (precision + recall))
    print("Overall F1 score: " + str(F1))
    print("\n")
    return (precision, recall, F1)

if __name__ == "__main__":
    os.chdir("..")

    precision = []
    recall = []
    F1 = []
    
    for i in range(1,51):
        precision_k, recall_k, F1_k = evaluate_knn(i)
        precision.append(precision_k)
        recall.append(recall_k)
        F1.append(F1_k)

    plt.plot(range(1,51), precision, color='blue', label='precision')
    plt.plot(range(1,51), recall, color='red', label='recall')
    plt.plot(range(1,51), F1, color='purple', label='F1-score')
    plt.xlabel('k')
    plt.ylabel('value')
    plt.legend()
    plt.show()
