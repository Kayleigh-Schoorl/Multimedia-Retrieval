import trimesh
import os
import argparse
import pyvista as pv

from query_steps import normalization
from query_steps import render_2D_images
from query_steps import extract_features
from query_steps import calculate_distances

parser = argparse.ArgumentParser()
parser.add_argument("-M", "--mesh", help="input mesh")

args = parser.parse_args()

if not args.mesh:
    print("Please input a mesh.")
    print("Usage: -M path/to/mesh")
    exit()

splitted = os.path.splitext(args.mesh)
extension = splitted[len(splitted)-1]

if extension != ".ply" and extension != ".off":
    print("Please input a .off or .ply file.")
    exit()

mesh = trimesh.load(args.mesh)

print("Normalizing input mesh...")
normalized_mesh = normalization.normalize(mesh, args.mesh)

print("Rendering 2D images for feature extraction...")
render_2D_images.generate(normalized_mesh)

print("Performing feature extraction...")
data = extract_features.extract(mesh)

print("Finding 5 closest shapes in the database...")
found_shapes = calculate_distances.distance(data)

curr_directory = os.getcwd()
db_path = os.path.join(curr_directory, "LabeledDB_new")

original_mesh = pv.read(args.mesh)

mesh_class1 = found_shapes[0].split("_")[0]
mesh_name1 = found_shapes[0].split("_")[1] + ".off"
mesh1 = pv.read(os.path.join(db_path, mesh_class1, mesh_name1))

mesh_class2 = found_shapes[1].split("_")[0]
mesh_name2 = found_shapes[1].split("_")[1] + ".off"
mesh2 = pv.read(os.path.join(db_path, mesh_class2, mesh_name2))

mesh_class3 = found_shapes[2].split("_")[0]
mesh_name3 = found_shapes[2].split("_")[1] + ".off"
mesh3 = pv.read(os.path.join(db_path, mesh_class3, mesh_name3))

mesh_class4 = found_shapes[3].split("_")[0]
mesh_name4 = found_shapes[3].split("_")[1] + ".off"
mesh4 = pv.read(os.path.join(db_path, mesh_class4, mesh_name4))

mesh_class5 = found_shapes[4].split("_")[0]
mesh_name5 = found_shapes[4].split("_")[1] + ".off"
mesh5 = pv.read(os.path.join(db_path, mesh_class5, mesh_name5))

p = pv.Plotter(shape=(2, 3))
p.subplot(0, 0)
p.add_text('Original shape')
p.add_mesh(original_mesh, color="red")
p.subplot(0, 1)
p.add_text('Found shape 1')
p.add_mesh(mesh1, color="orange")
p.subplot(0, 2)
p.add_text('Found shape 2')
p.add_mesh(mesh2, color="yellow")
p.subplot(1, 0)
p.add_text('Found shape 3')
p.add_mesh(mesh3, color="green")
p.subplot(1, 1)
p.add_text('Found shape 4')
p.add_mesh(mesh4, color="blue")
p.subplot(1, 2)
p.add_text('Found shape 5')
p.add_mesh(mesh5, color="purple")
p.show()