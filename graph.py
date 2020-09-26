import xlsxwriter
import numpy as np
import trimesh
import os, stat
from pathlib import Path


def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)


curr_directory = os.getcwd()
db_path = os.path.join(curr_directory, "meshes", "scaled")
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
        center = mesh.centroid
        scale = mesh.scale

        face_types = []
        for face in mesh.faces:
            no = len(face)
            if no not in face_types:
                face_types.append(no)

        bounds = mesh.bounds
        print(scale)
        data.append(['mesh_class', faces, vertices, face_types, bounds, center, scale])



import matplotlib.pyplot as plt


no_faces = []
no_scale = []


row = 0
for mesh_data in data:
    no_faces.append(mesh_data[1])
    no_scale.append(mesh_data[6])

# bins = np.array([0, 10000, 20000, 30000, 40000, 50000, 60000])
# plt.hist(no_faces, bins=13, linewidth=1, edgecolor='black')
# plt.ticklabel_format(useOffset=False)
# plt.xlim(bins.min(), bins.max())
# plt.xlabel("Faces")
# plt.ylabel("3D shapes")
# plt.show()


bins = np.array([ 1, 1.2, 1.4,1.6,1.8, 2 , 2.2 , 2.4, 2.6, 2.8, 3])
plt.hist(no_scale, bins=13, linewidth=1, edgecolor='black')
plt.ticklabel_format(useOffset=False)
plt.xlim(bins.min(), bins.max())
plt.xlabel("Scale")
plt.ylabel("3D shapes")
plt.show()
