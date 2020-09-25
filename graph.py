import xlsxwriter
import numpy as np
import trimesh
import os, stat
from pathlib import Path


def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)


curr_directory = os.getcwd()
print(curr_directory)
db_path = os.path.join(curr_directory, "normalized")
#db_path = os.path.join(r"C:\Users\trekk\Documents\GitHub\Multimedia-Retrieval", "LabeledDB_new_small")
print(db_path)
data = []

for filename in os.listdir(db_path):

    #exclude hidden files
    if filename.startswith("."):
        continue

    extension = os.path.splitext(filename)[1]
    if extension == ".off" or extension == ".ply":
        mesh_path = os.path.join(db_path, filename)
        mesh = trimesh.load(mesh_path)

        faces = len(mesh.faces)
        vertices = len(mesh.vertices)

        face_types = []
        for face in mesh.faces:
            no = len(face)
            if no not in face_types:
                face_types.append(no)

        bounds = mesh.bounds
        
        data.append(['mesh_class', faces, vertices, face_types, bounds])



import matplotlib.pyplot as plt
import pandas as pd

no_faces = []



row = 0
for mesh_data in data:
    print(mesh_data[1])
    no_faces.append(mesh_data[1])

bins = [0, 10000, 20000, 30000, 40000, 50000, 60000]
plt.hist(no_faces, bins=13, linewidth=1, edgecolor='black',)
#plt.xticks(bins)
#plt.xticks = bins
plt.xlabel("Faces")
plt.ylabel("3D shapes")
plt.show()

