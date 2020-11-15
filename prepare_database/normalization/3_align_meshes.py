import numpy as np
import trimesh
import os

os.chdir("..")
os.chdir("..")

curr_directory = os.getcwd()
db_path = os.path.join(curr_directory, "meshes", "normalized")

if not os.path.exists(os.path.join(curr_directory, "meshes", "aligned")):
    os.makedirs(os.path.join(curr_directory, "meshes", "aligned"))

for filename in os.listdir(db_path):

    extension = os.path.splitext(filename)[1]
    if extension == ".off" or extension == ".ply":
        mesh_path = os.path.join(db_path, filename)
        mesh = trimesh.load(mesh_path)

        for i in range(4):

            coords = []

            for vertex in mesh.vertices:
                coords.append(vertex)

            A = np.transpose(np.array(coords))


            # compute the covariance matrix for A 
            # see the documentation at 
            # https://docs.scipy.org/doc/numpy/reference/generated/numpy.cov.html
            # this function expects that each row of A represents a variable, 
            # and each column a single observation of all those variables
            A_cov = np.cov(A)  # 3x3 matrix

            # computes the eigenvalues and eigenvectors for the 
            # covariance matrix. See documentation at  
            # https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.eig.html 
            eigenvalues, eigenvectors = np.linalg.eig(A_cov)

            print("==> eigenvalues for (x, y, z)")
            print(eigenvalues)
            print("\n==> eigenvectors")
            print(eigenvectors)


            indices = np.argsort(eigenvalues)
            R = np.linalg.inv(np.array([eigenvectors[indices[2]],eigenvectors[indices[1]],eigenvectors[indices[0]]]))

            transformed = R.dot(np.transpose(mesh.vertices))
            mesh.vertices = np.transpose(transformed)

        name = os.path.splitext(filename)[0]
        export_path=os.path.join(curr_directory, "meshes", "aligned", filename)

        mesh.export(file_obj=export_path)