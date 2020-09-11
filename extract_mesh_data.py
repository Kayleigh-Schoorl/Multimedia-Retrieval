import xlsxwriter
import numpy as np
import trimesh
import os, stat
from pathlib import Path


def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)


curr_directory = os.getcwd()
db_path = os.path.join(curr_directory, "LabeledDB_new")

data = [["Class", "Faces", "Vertices", "Type of faces", "Bounding box"]]

for mesh_class in os.listdir(db_path):

    #exclude hidden files
    if mesh_class.startswith("."):
        continue

    mesh_class_path = os.path.join(db_path, mesh_class)
    for filename in os.listdir(mesh_class_path):
        extension = os.path.splitext(filename)[1]
        if extension == ".off" or extension == ".ply":
            mesh_path = os.path.join(mesh_class_path, filename)
            mesh = trimesh.load(mesh_path)

            faces = len(mesh.faces)
            vertices = len(mesh.vertices)

            face_types = []
            for face in mesh.faces:
                no = len(face)
                if no not in face_types:
                    face_types.append(no)

            bounds = mesh.bounds
            
            data.append([mesh_class, faces, vertices, face_types, bounds])



# write to excel sheet
workbook = xlsxwriter.Workbook('mesh_database.xlsx')
worksheet = workbook.add_worksheet("Data")

row = 0
for mesh_data in data:
    worksheet.write(row, 0, mesh_data[0])
    worksheet.write(row, 1, mesh_data[1])
    worksheet.write(row, 2, mesh_data[2])
    worksheet.write(row, 3, str(mesh_data[3]))
    worksheet.write(row, 4, str(mesh_data[4]))
    row += 1

workbook.close()
