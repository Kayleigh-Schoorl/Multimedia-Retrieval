import numpy as np
import trimesh
import os


os.chdir("..")
curr_directory = os.getcwd()
db_path = os.path.join(curr_directory, "meshes", "simplified")

for filename in os.listdir(db_path):

    extension = os.path.splitext(filename)[1]
    if extension == ".off" or extension == ".ply":
        mesh_path = os.path.join(db_path, filename)
        mesh = trimesh.load(mesh_path)

        coords = []

        f_x = 0
        f_y = 0
        f_z = 0

        for vertex in mesh.vertices:
            f_x += np.sign(vertex[0])
            f_y += np.sign(vertex[1])
            f_z += np.sign(vertex[2])

        F = np.array([[-np.sign(f_x), 0, 0],
                        [0, -np.sign(f_y), 0],
                        [0, 0, -np.sign(f_z)]])

        transformed = F.dot(np.transpose(mesh.vertices))
        mesh.vertices = np.transpose(transformed)

        name = os.path.splitext(filename)[0]
        export_path=os.path.join(curr_directory, "meshes", "flipped", filename)

        mesh.export(file_obj=export_path)