import numpy as np
import trimesh
import os, stat
from pathlib import Path
import meshlabxml as mlx


def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

os.chdir("..")
os.chdir("..")

curr_directory = os.getcwd()
db_path = os.path.join(curr_directory, "LabeledDB_new")

if not os.path.exists(os.path.join(curr_directory, "meshes", "converted")):
    os.makedirs(os.path.join(curr_directory, "meshes", "converted"))
if not os.path.exists(os.path.join(curr_directory, "meshes", "simplified")):
    os.makedirs(os.path.join(curr_directory, "meshes", "simplified"))

for mesh_class in os.listdir(db_path):

    #exclude hidden files
    if mesh_class.startswith("."):
        continue

    mesh_class_path = os.path.join(db_path, mesh_class)
    for filename in os.listdir(mesh_class_path):
        extension = os.path.splitext(filename)[1]
        if extension == ".off" or extension == ".ply":
            mesh_path = os.path.join(mesh_class_path, filename)
            mesh = trimesh.load(mesh_path)
            name = os.path.splitext(filename)[0]
            name_labeled = mesh_class + '_' + name
            mesh.export(os.path.join('meshes', 'converted', name_labeled + '.ply'))

            faces = len(mesh.faces)
            converted_mesh_path = os.path.join(curr_directory, "meshes", "converted", name_labeled + ".ply")
            script = mlx.FilterScript(file_in=converted_mesh_path, file_out=os.path.join("meshes","simplified", name_labeled + ".ply"),
                                      ml_version='2016.12')

            if faces > 20000:

                mlx.remesh.simplify(script, texture=False, faces=20000,
                    target_perc=0.0, quality_thr=1.0, preserve_boundary=True,
                    boundary_weight=1.0, preserve_normal=True,
                    optimal_placement=True, planar_quadric=True,
                    selected=False, extra_tex_coord_weight=1.0)

            if faces < 20000:
                while (faces < 20000):
                    mlx.subdivide.loop(script)
                    faces *= 4

                mlx.remesh.simplify(script, texture=False, faces=20000,
                                    target_perc=0.0, quality_thr=1.0, preserve_boundary=True,
                                    boundary_weight=1.0, preserve_normal=True,
                                    optimal_placement=True, planar_quadric=True,
                                    selected=False, extra_tex_coord_weight=1.0)

            script.run_script()


