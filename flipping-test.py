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
mesh.show(smooth=args.smooth)


coords = []

f_x = 0
f_y = 0
f_z = 0

for vertex in mesh.vertices:
    f_x += np.sign(vertex[0])
    f_y += np.sign(vertex[1])
    f_z += np.sign(vertex[2])

print(f_x)
print(f_y)
print(f_z)

F = np.array([[-np.sign(f_x), 0, 0],
                [0, -np.sign(f_y), 0],
                [0, 0, -np.sign(f_z)]])

print(F)

transformed = F.dot(np.transpose(mesh.vertices))
mesh.vertices = np.transpose(transformed)
mesh.show()
