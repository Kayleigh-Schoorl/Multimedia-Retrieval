import numpy as np
import trimesh
import os, stat
from pathlib import Path
import meshlabxml as mlx

meshlabserver_path = 'C:\\Program Files\\VCG\\MeshLab'
os.environ['PATH'] = meshlabserver_path + os.pathsep + os.environ['PATH']

def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)


curr_directory = os.getcwd()
db_path = os.path.join(curr_directory, "simplified")

for filename in os.listdir(db_path):

    #exclude hidden files
    if filename.startswith("."):
        continue


    extension = os.path.splitext(filename)[1]
    if extension == ".off" or extension == ".ply":
        mesh_path = os.path.join(db_path, filename)
        name = os.path.splitext(filename)[0]
        normalized_path=os.path.join(curr_directory, "normalized")

        #aabb = mlx.files.measure_aabb(os.path.join(normalized_path, name + ".ply"))
        #just to check that the files are centered

        aabb = mlx.files.measure_aabb(mesh_path)
        simplified_mesh_path = os.path.join(curr_directory, "simplified", name + ".ply")

        script = mlx.FilterScript(file_in=simplified_mesh_path,
                                  file_out=os.path.join("normalized", name + ".ply"),
                                  ml_version='2016.12')


        #scale

        # mlx.transform.scale(script,np.divide(1,aabb['size']))
        # script.run_script()


        #center
        script = mlx.FilterScript(file_in=os.path.join("normalized", name + ".ply"),
                                  file_out=os.path.join("normalized", name + ".ply"),
                                  ml_version='2016.12')

        mlx.transform.translate(script , np.negative(aabb['center']))
        script.run_script()
