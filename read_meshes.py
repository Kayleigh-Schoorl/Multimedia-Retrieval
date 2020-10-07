import numpy as np
import trimesh
import argparse
import meshpy
import pyvista as pv
import os

parser = argparse.ArgumentParser()
parser.add_argument("-M", "--mesh", help="input mesh")
parser.add_argument("-S", "--smooth", help="show smooth mesh", action="store_true")

args = parser.parse_args()

if args.mesh:
    splitted = os.path.splitext(args.mesh)
    extension = splitted[len(splitted)-1]

    if extension == ".ply" or extension == ".off":
        mesh = pv.read(args.mesh)
        mesh.plot(show_edges=True, color="pink", window_size=[2048, 1536], background="white")

    else:
        print("Please input a .off or .ply file.")

else:
    print("Please input a mesh.")
    print("Usage: -M path/to/mesh")
