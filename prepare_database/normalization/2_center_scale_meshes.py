import numpy as np
import trimesh
import os, stat
from pathlib import Path
import meshlabxml as mlx
import matplotlib.pyplot as plt

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


def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)


os.chdir("..")
os.chdir("..")

curr_directory = os.getcwd()
db_path = os.path.join(curr_directory, "meshes", "simplified")

if not os.path.exists(os.path.join(curr_directory, "meshes", "scaled")):
    os.makedirs(os.path.join(curr_directory, "meshes", "scaled"))
if not os.path.exists(os.path.join(curr_directory, "meshes", "normalized")):
    os.makedirs(os.path.join(curr_directory, "meshes", "normalized"))

distance_before=[]
distance_after=[]

for filename in os.listdir(db_path):

    extension = os.path.splitext(filename)[1]
    if extension == ".off" or extension == ".ply":
        name = os.path.splitext(filename)[0]

        # #scale
        scaling_script = mlx.FilterScript(file_in=os.path.join("meshes", "simplified", name + ".ply"),
                                  file_out=os.path.join("meshes", "scaled", name + ".ply"),
                                  ml_version='2016.12')


        scale_fixed(script=scaling_script,unit=True,center_pt='')
        scaling_script.run_script()

        #center
        centering_script = mlx.FilterScript(file_in=os.path.join("meshes", "scaled", name + ".ply"),
                                  file_out=os.path.join("meshes", "normalized", name + ".ply"),
                                  ml_version='2016.12')

        aabb = mlx.files.measure_aabb(os.path.join("meshes", "scaled", name + ".ply"))
        center_before = aabb['center']
        print("cent_bef =  "+str(center_before))
        mlx.transform.translate(centering_script, np.negative(aabb['center']))
        centering_script.run_script()

        aabb = mlx.files.measure_aabb(os.path.join("meshes", "normalized", name + ".ply"))
        center_after = aabb['center']
        print("cent_aft =  "+str(center_after))


        distance_before.append(abs(np.sqrt(center_before[0]**2+center_before[1]**2+center_before[2]**2)))
        distance_after.append(abs(np.sqrt(center_after[0]**2+center_after[1]**2+center_after[2]**2)))


