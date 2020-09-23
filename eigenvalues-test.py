import numpy as np
import trimesh
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-M", "--mesh", help="input mesh")
parser.add_argument("-S", "--smooth", help="show smooth mesh", action="store_true")

args = parser.parse_args()


if not args.mesh:
    print("Please input a mesh.")
    print("Usage: -M path/to/mesh")
    quit()

print("Opening mesh...")
mesh = trimesh.load(args.mesh)
#mesh.show(smooth=args.smooth)


coords = []

for vertex in mesh.vertices:
    coords.append(vertex)

A = np.transpose(np.array(coords))


print(A.shape)

#A = np.zeros((3, n_points))
#A[0] = x_coords
#A[1] = y_coords
#A[2] = z_coords

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


# Code for computing angle between two n-dimensional vectors:
# https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python/13849249#13849249
def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))





indices = np.argsort(eigenvalues)
# x_old = eigenvectors[indices[0]]
# y_old = eigenvectors[indices[1]]
# z_old = eigenvectors[indices[2]]


x_old,y_old,z_old = np.linalg.inv((eigenvectors[indices[0]],eigenvectors[indices[1]],eigenvectors[indices[2]]))

x_new = np.array((1,0,0))
y_new = np.array((0,1,0))
z_new = np.array((0,0,1))


M11, M12, M13 = np.dot(x_old, x_new), np.dot(x_old, y_new), np.dot(x_old, z_new)
M21, M22, M23 = np.dot(y_old, x_new), np.dot(y_old, y_new), np.dot(y_old, z_new)
M31, M32, M33 = np.dot(z_old, x_new), np.dot(z_old, y_new), np.dot(z_old, z_new)

# set up rotation matrix
R = np.array([[M11, M12, M13],
                [M21, M22, M23],
                [M31, M32, M33]])

transformed = np.linalg.inv(np.transpose(R)).dot(np.transpose(mesh.vertices))

mesh.show()
mesh.vertices = np.transpose(transformed)
mesh.show()