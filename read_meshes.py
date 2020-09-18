import numpy as np
import trimesh
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-M", "--mesh", help="input mesh")
parser.add_argument("-S", "--smooth", help="show smooth mesh", action="store_true")

args = parser.parse_args()

if args.mesh:
    print("Opening mesh...")
    mesh = trimesh.load(args.mesh)
    mesh.show(smooth=args.smooth)
else:
    print("Please input a mesh.")
    print("Usage: -M path/to/mesh")
