import os
import json
import math
import random

def evaluate():
    curr_directory=os.getcwd()

    with open(os.path.join(curr_directory, 'normalized_features.json'), 'r') as f:
        dataset = json.load(f)

    # dataset_classes = {}
    # for shape in dataset:
    #     class_name = shape.split("_")[0]
    #     if class_name not in dataset_classes:
    #         dataset_classes[class_name] = {shape: dataset.get(shape)}
    #     else:
    #         dataset_classes.get(class_name)[shape] = dataset.get(shape)

    # query_set = {}
    # database_set = {}
    # for shape_class in dataset_classes:
    #     class_shapes = dataset_classes.get(shape_class)
    #     keys = list(class_shapes.keys())      # Python 3; use keys = d.keys() in Python 2
    #     random.shuffle(keys)
    #     split_value = int(len(keys) / 4)
    #     query_shapes = keys[:split_value]
    #     database_shapes = keys[split_value:]
    #     for shape in query_shapes:
    #         query_set[shape] = class_shapes.get(shape)
    #     for shape in database_shapes:
    #         database_set[shape] = class_shapes.get(shape)


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

    weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


    test_count = 0
    correct_count = 0
    class_count = {}

    for query_shape in dataset:
        distances=[]
        image_index=[]
        counter=0

        r = dict(dataset)
        del r[query_shape]

        for shape in r.items():
            total_distance = 0

            for query_image in dataset.get(query_shape).items():
                min_distance = math.inf 
                for image in shape[1]:
                    distance = 0
                    for i in range(len(features)):
                        distance += float(weights[i]) * (shape[1][str(image)][features[i]] - query_image[1][features[i]])**2
                    distance = math.sqrt(distance)
                    if distance < min_distance:
                        min_distance = distance
                total_distance += min_distance

            for image in shape[1]:
                min_distance = math.inf 
                for query_image in dataset.get(query_shape).items():
                    distance = 0
                    for i in range(len(features)):
                        distance += float(weights[i])**2 * (shape[1][str(image)][features[i]] - query_image[1][features[i]])**2
                    distance = math.sqrt(distance)
                    if distance < min_distance:
                        min_distance = distance
                total_distance += min_distance

            distances.append(total_distance)
            image_index.append(counter)
            counter+=1
            
        distances, image_index = (list(t) for t in zip(*sorted(zip(distances, image_index))))

        query_shape_class = query_shape.split("_")[0]
        if query_shape_class not in class_count:
            class_count[query_shape_class] = [5,0]
        else:
            class_count[query_shape_class][0] += 5
        for i in range(5):
            found_shape = list(r.keys())[image_index[i]]
            found_shape_class = found_shape.split("_")[0]
            print("Original shape is is " + query_shape + ", found shape is " + found_shape + " with a distance of " + str(distances[i]))
            if query_shape_class == found_shape_class:
                correct_count += 1
                class_count[query_shape_class][1] += 1
            test_count += 1

    for class_acc in class_count:
        print("Accuracy for class " + class_acc + ": " + str(class_count.get(class_acc)[1] / class_count.get(class_acc)[0] * 100) + "%")
    print("Overall accuracy: " + str(correct_count / test_count * 100) + "%")


if __name__ == "__main__":
    os.chdir("..")
    evaluate()