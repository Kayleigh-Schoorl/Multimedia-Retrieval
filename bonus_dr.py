import tsne
import json
import os
import numpy as np
import matplotlib.pyplot as plt

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

classes=[]
colors=[]
numbered_labels=[]

for i in data.items():
    for j in range(1,13):
        for k in features:
            feature.append(i[1][str(j)][str(k)])

    numbered_labels.append(i[0])
    labels.append(i[0].split("_")[0])
    shape.append(feature)
    print(feature)
    feature=[]

for i in range(len(labels)):
    if labels[i] not in classes:
        classes.append(labels[i])

for i in range(len(labels)):
    for k in range(len(classes)):
        if labels[i] == classes[k]:
            colors.append(k)

shape=np.array(shape)

X=tsne.tsne(shape,initial_dims=168)

print(shape.shape)
print(X.shape)

fig,ax = plt.subplots()
sc = plt.scatter(X[:, 0], X[:, 1], 20,colors)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = numbered_labels[ind['ind'][0]]
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor([1,0,1])
    annot.get_bbox_patch().set_alpha(0.4)

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()