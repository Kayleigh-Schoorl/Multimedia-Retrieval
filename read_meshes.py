# read_meshes.py
# Small program for viewing meshes in a trimesh or pyvista window.

import numpy as np
import trimesh
import argparse
import pyvista as pv
import os

parser = argparse.ArgumentParser()
parser.add_argument("-M", "--mesh", help="input mesh")
parser.add_argument("-S", "--smooth", help="show smooth mesh", action="store_true")
parser.add_argument("-T", "--trimesh", help="use trimesh viewer", action="store_true")
parser.add_argument("-E", "--edges", help="show edges", action="store_true")

args = parser.parse_args()

if args.mesh:
    splitted = os.path.splitext(args.mesh)
    extension = splitted[len(splitted)-1]

    if extension == ".ply" or extension == ".off":

        if args.trimesh:
            mesh = trimesh.load(args.mesh)
            mesh.show(smooth=args.smooth, flags={"wireframe":args.edges})

        else:
            mesh = pv.read(args.mesh)
            mesh.plot(show_edges=args.edges, color="pink", window_size=[2048, 1536], background="white", smooth_shading=args.smooth)

    else:
        print("Please input a .off or .ply file.")

else:
    print("Please input a mesh.")
    print("Usage: -M path/to/mesh")
