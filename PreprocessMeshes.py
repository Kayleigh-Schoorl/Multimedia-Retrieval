import numpy as np
import trimesh
import os, stat
from pathlib import Path
import meshlabxml as mlx

meshlabserver_path = '/Applications/meshlab.app/Contents/MacOS'
os.environ['PATH'] = meshlabserver_path + os.pathsep + os.environ['PATH']

def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)


curr_directory = os.getcwd()
db_path = os.path.join(curr_directory, "LabeledDB_new")

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
            mesh.export(os.path.join('converted',name + '.ply'))

            faces = len(mesh.faces)
            if faces > 20000:
                converted_mesh_path = os.path.join(curr_directory, "converted", name + ".ply")
                # script = mlx.FilterScript(file_in=converted_mesh_path, file_out=os.path.join("simplified", name + ".ply"), ml_version='2016.12')

                # mlx.remesh.simplify(script, texture=False, faces=20000,
                #     target_perc=0.0, quality_thr=1.0, preserve_boundary=True,
                #     boundary_weight=1.0, preserve_normal=True,
                #     optimal_placement=True, planar_quadric=True,
                #     selected=False, extra_tex_coord_weight=1.0)
                
                # script.run_script()

            elif faces < 20000:
                new_vertices, new_faces = trimesh.remesh.subdivide(mesh.vertices, mesh.faces)

                print("mesh "+str(filename))
                print(len(mesh.faces))
                print(len(new_faces))


