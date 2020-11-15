import numpy as np
import trimesh
import os, stat
from pathlib import Path
import meshlabxml as mlx
import math 
import cv2


# Code for writing a MeshLab script for scaling by 3DLIRIOUS
# https://github.com/3DLIRIOUS/MeshLabXML
def make_list(var, num_terms=1):
    """ Make a variable a list if it is not already
    If variable is not a list it will make it a list of the correct length with
    all terms identical.
    """
    if not isinstance(var, list):
        if isinstance(var, tuple):
            var = list(var)
        else:
            var = [var]
    #if len(var) == 1:
            for _ in range(1, num_terms):
                var.append(var[0])
    return var


def write_filter(script, filter_xml):
    """ Write filter to FilterScript object or filename
    Args:
        script (FilterScript object or filename str): the FilterScript object
            or script filename to write the filter to.
        filter_xml (str): the xml filter string
    """
    if isinstance(script, mlx.FilterScript):
        script.filters.append(filter_xml)
    elif isinstance(script, str):
        script_file = open(script, 'a')
        script_file.write(filter_xml)
        script_file.close()
    else:
        print(filter_xml)
    return None


def scale_fixed(script, value=1.0, uniform=True, center_pt='origin',
           custom_center_pt=None, unit=False, freeze=True, all_layers=False):
    """
    Args:
        script: the FilterScript object or script filename to write
            the filter to.
        value (float): Scaling along the X axis.
        uniform (bool): If selected an uniform scaling (the same for all the',
        ' three axis) is applied (the X axis value is used).
        center_pt (str): Choose a method.
        custom_center_pt (point): This scaling center is used only if the',
        ' _custom point_ option is chosen.
        unit (bool): If selected, the object is scaled to a box whose',
        ' sides are at most 1 unit length.
        freeze (bool): The transformation is explicitly applied and the',
        ' vertex coords are actually changed.
        all_layers (bool): The transformation is explicitly applied to all the',
        ' mesh and raster layers in the project.
    """
    """# Convert value to list if it isn't already
    if not isinstance(value, list):
        value = list(value)
    # If a single value was supplied use it for all 3 axes
    if len(value) == 1:
        value = [value[0], value[0], value[0]]"""
    value = make_list(value, 3)
    # Convert center point name into number
    if center_pt.lower() == 'origin':
        center_pt_num = 0
    elif center_pt.lower() == 'barycenter':
        center_pt_num = 1
    else:  # custom axis
        center_pt_num = 2
        if custom_center_pt is None:
            print('WARNING: a custom center point was selected, however',
                  '"custom_center_pt" was not provided. Using default',
                  '(origin).')
            custom_center_pt = [0.0, 0.0, 0.0]
    filter_xml = ''.join([
        '  <filter name="Transform: Scale, Normalize">\n',
        '    <Param name="axisX" ',
        'value="%s" ' % value[0],
        'description="X Axis" ',
        'type="RichFloat" ',
        '/>\n',
        '    <Param name="axisY" ',
        'value="%s" ' % value[1],
        'description="Y Axis" ',
        'type="RichFloat" ',
        '/>\n',
        '    <Param name="axisZ" ',
        'value="%s" ' % value[2],
        'description="Z Axis" ',
        'type="RichFloat" ',
        '/>\n',
        '    <Param name="uniformFlag" ',
        'value="%s" ' % str(uniform).lower(),
        'description="Uniform Scaling" ',
        'type="RichBool" ',
        '/>\n',
        '    <Param name="scaleCenter" ',
        'value="%d" ' % center_pt_num,
        'description="Center of scaling:" ',
        'enum_val0="origin" ',
        'enum_val1="barycenter" ',
        'enum_val2="custom point" ',
        'enum_cardinality="3" ',
        'type="RichEnum" ',
        '/>\n',
        '    <Param name="customCenter" ',
        'x="%s" ' % custom_center_pt[0],
        'y="%s" ' % custom_center_pt[1],
        'z="%s" ' % custom_center_pt[2],
        'description="Custom center" ',
        'type="RichPoint3f" ',
        '/>\n',
        '    <Param name="unitFlag" ',
        'value="%s" ' % str(unit).lower(),
        'description="Scale to Unit bbox" ',
        'type="RichBool" ',
        '/>\n',
        '    <Param name="Freeze" ',
        'value="%s" ' % str(freeze).lower(),
        'description="Freeze Matrix." ',
        'type="RichBool" ',
        '/>\n',
        '    <Param name="ToAll" ',
        'value="%s" ' % str(all_layers).lower(),
        'description="Apply to all layers." ',
        'type="RichBool" ',
        '/>\n',
        '  </filter>\n'])
    write_filter(script, filter_xml)
    return None


def normalize(mesh, mesh_path):

    # Subdivide and/or simplify mesh
    faces = len(mesh.faces)
    curr_directory = os.getcwd()

    temp_mesh_path = os.path.join(curr_directory, "tempfile.ply")
    remesh_script = mlx.FilterScript(file_in=mesh_path, file_out=temp_mesh_path, ml_version='2016.12')

    if faces > 20000:

        mlx.remesh.simplify(remesh_script, texture=False, faces=20000,
            target_perc=0.0, quality_thr=1.0, preserve_boundary=True,
            boundary_weight=1.0, preserve_normal=True,
            optimal_placement=True, planar_quadric=True,
            selected=False, extra_tex_coord_weight=1.0)

    if faces < 20000:
        while (faces < 20000):
            mlx.subdivide.loop(remesh_script)
            faces *= 4

        mlx.remesh.simplify(remesh_script, texture=False, faces=20000,
                            target_perc=0.0, quality_thr=1.0, preserve_boundary=True,
                            boundary_weight=1.0, preserve_normal=True,
                            optimal_placement=True, planar_quadric=True,
                            selected=False, extra_tex_coord_weight=1.0)

    remesh_script.run_script()


    # Scaling
    scaling_script = mlx.FilterScript(file_in=temp_mesh_path,
                                file_out=temp_mesh_path,
                                ml_version='2016.12')


    scale_fixed(script=scaling_script,unit=True,center_pt='')
    scaling_script.run_script()


    # Centering 
    centering_script = mlx.FilterScript(file_in=temp_mesh_path,
                                file_out=temp_mesh_path,
                                ml_version='2016.12')

    aabb = mlx.files.measure_aabb(temp_mesh_path)
    center_before = aabb['center']
    mlx.transform.translate(centering_script, np.negative(aabb['center']))
    centering_script.run_script()


    # Alignment 
    mesh = trimesh.load(temp_mesh_path)
    aligning_coords = []

    for vertex in mesh.vertices:
        aligning_coords.append(vertex)

    A = np.transpose(np.array(aligning_coords))
    A_cov = np.cov(A) 
    eigenvalues, eigenvectors = np.linalg.eig(A_cov)

    indices = np.argsort(eigenvalues)
    R = np.linalg.inv(np.array([eigenvectors[indices[2]],eigenvectors[indices[1]],eigenvectors[indices[0]]]))

    transformed = R.dot(np.transpose(mesh.vertices))
    mesh.vertices = np.transpose(transformed)


    # Flipping 
    f_x = 0
    f_y = 0
    f_z = 0

    for vertex in mesh.vertices:
        f_x += np.sign(vertex[0])
        f_y += np.sign(vertex[1])
        f_z += np.sign(vertex[2])

    sign_x = -np.sign(f_x) if np.sign(f_x) else 1
    sign_y = -np.sign(f_y) if np.sign(f_y) else 1
    sign_z = -np.sign(f_z) if np.sign(f_z) else 1

    F = np.array([[sign_x, 0, 0],
                    [0, sign_y, 0],
                    [0, 0, sign_z]])

    transformed = F.dot(np.transpose(mesh.vertices))
    mesh.vertices = np.transpose(transformed)

    if os.path.exists(os.path.join(curr_directory, "tempfile.ply")):
        os.remove(os.path.join(curr_directory, "tempfile.ply"))
    if os.path.exists(os.path.join(curr_directory, "TEMP3D_aabb.xyz")):
        os.remove(os.path.join(curr_directory, "TEMP3D_aabb.xyz"))
    return mesh