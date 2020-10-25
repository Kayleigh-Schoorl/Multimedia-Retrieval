import tsne
import json
import os
import numpy as np
import pylab

curr_directory=os.getcwd()

with open(os.path.join(curr_directory, 'normalized_features.json'), 'r') as f:
    data = json.load(f)

feature=[]
image=[]
shape=[]
labels=[]

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

for i in data.items():
    for j in range(1,13):
        for k in features:
            feature.append(i[1][str(j)][str(k)])

    labels.append(i[0])
    shape.append(feature)
    feature=[]



shape=np.array(shape)

print(np.shape(shape))
print(labels)

X=tsne.tsne(shape)
pylab.scatter(X[:,0], labels)
pylab.show()