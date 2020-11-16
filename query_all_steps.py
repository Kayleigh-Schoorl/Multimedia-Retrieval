import trimesh
import os
import argparse
import pyvista as pv

from query_steps import normalization
# query_all_steps.py
# This code allows providing a mesh as input and will return the closest shape in our shape database.

from query_steps import render_2D_images
from query_steps import extract_features
from query_steps import calculate_distances

parser = argparse.ArgumentParser()
parser.add_argument("-M", "--mesh", help="input mesh")
parser.add_argument("-E", "--exact", help="use exact distance method", action="store_true")

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

print("Finding 8 closest shapes in the database...")
found_shapes, distances = calculate_distances.distance(data, exact=args.exact)

curr_directory = os.getcwd()
db_path = os.path.join(curr_directory, "LabeledDB_new")

p = pv.Plotter(shape=(3, 3))
p.background_color="white"

original_mesh = pv.read(args.mesh)
p.subplot(0, 0)
p.add_text("Original shape", color="black")
p.add_mesh(original_mesh, color="grey")

subplots = [(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
count = 1

for i in range(len(found_shapes)):
    shape = found_shapes[i]
    mesh_class1 = found_shapes[i].split("_")[0]
    mesh_name1 = found_shapes[i].split("_")[1] + ".off"
    mesh = pv.read(os.path.join(db_path, mesh_class1, mesh_name1))
    p.subplot(subplots[i][0],subplots[i][1])
    p.add_text("Found shape #" + str(count), color="black")
    p.add_text("Distance: " + str(round(distances[i],3)), color="black", position="bottom", font_size=10)
    p.add_mesh(mesh, color="pink")
    count += 1

p.show()