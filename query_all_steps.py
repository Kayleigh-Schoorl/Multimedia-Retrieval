import trimesh
import os
import argparse

from query_steps import normalization
from query_steps import render_2D_images
from query_steps import extract_features

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
normalized_mesh = normalization.normalize(mesh, args.mesh)
render_2D_images.generate(normalized_mesh)
data = extract_features.extract(mesh)
print(data)