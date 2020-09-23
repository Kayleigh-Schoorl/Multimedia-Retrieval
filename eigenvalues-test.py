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



indices = np.argsort(eigenvalues)
# x_old = eigenvectors[indices[0]]
# y_old = eigenvectors[indices[1]]
# z_old = eigenvectors[indices[2]]

R = np.linalg.inv(np.transpose(np.array([eigenvectors[indices[0]],eigenvectors[indices[1]],eigenvectors[indices[2]]])))


transformed = np.transpose(R).dot(np.transpose(mesh.vertices))

mesh.show()
mesh.vertices = np.transpose(transformed)
mesh.show()