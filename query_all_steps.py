import numpy as np
import trimesh
import os, stat
from pathlib import Path
import meshlabxml as mlx
import argparse
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

# Subdivide and/or simplify mesh
faces = len(mesh.faces)
curr_directory = os.getcwd()

temp_mesh_path = os.path.join(curr_directory, "tempfile.ply")
remesh_script = mlx.FilterScript(file_in=args.mesh, file_out=temp_mesh_path, ml_version='2016.12')

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

# scaling
scaling_script = mlx.FilterScript(file_in=temp_mesh_path,
                            file_out=temp_mesh_path,
                            ml_version='2016.12')


scale_fixed(script=scaling_script,unit=True,center_pt='')
scaling_script.run_script()

# center
centering_script = mlx.FilterScript(file_in=temp_mesh_path,
                            file_out=temp_mesh_path,
                            ml_version='2016.12')

aabb = mlx.files.measure_aabb(temp_mesh_path)
center_before = aabb['center']
mlx.transform.translate(centering_script, np.negative(aabb['center']))
centering_script.run_script()


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



# generate 2D images

curr_directory = os.getcwd()
ANGLE72 = math.radians(72)
ANGLE36 = math.radians(36)
ANGLE72m = math.radians(-72)
ANGLE36m = math.radians(-36)

Rx = np.array([[math.cos(ANGLE72), 0, math.sin(ANGLE72)],
               [0, 1, 0],
               [-math.sin(ANGLE72), 0, math.cos(ANGLE72)]])

R72j = np.array([[1, 0, 0],
               [0, math.cos(ANGLE72), -math.sin(ANGLE72)],
               [0, math.sin(ANGLE72), math.cos(ANGLE72)]])

R72s = np.array([[1, 0, 0],
               [0, math.cos(ANGLE72m), -math.sin(ANGLE72m)],
               [0, math.sin(ANGLE72m), math.cos(ANGLE72m)]])

R36j = np.array([[1, 0, 0],
               [0, math.cos(ANGLE36), -math.sin(ANGLE36)],
               [0, math.sin(ANGLE36), math.cos(ANGLE36)]])

R36s = np.array([[1, 0, 0],
               [0, math.cos(ANGLE36m), -math.sin(ANGLE36m)],
               [0, math.sin(ANGLE36m), math.cos(ANGLE36m)]])


Rf = np.array([[math.cos(math.radians(-180)), 0, math.sin(math.radians(-180))],
               [0, 1, 0],
               [-math.sin(math.radians(-180)), 0, math.cos(math.radians(-180))]])


if not os.path.exists(os.path.join(curr_directory,"renders")):
    os.makedirs(os.path.join(curr_directory, "renders"))


scene = mesh.scene()
scene.camera.fov = [70., 80.]
mesh_name = "temp"

#top photo
try:
    file_name = os.path.join(curr_directory, "renders",
                                mesh_name + '_' + "1" + '_render' + '.png')
    # save a render of the object as a png
    png = scene.save_image(resolution=[600, 400], visible=True)

    with open(file_name, 'wb') as f:
        f.write(png)
        f.close()
except BaseException as E:
    print("unable to save image", str(E))

transformed = R72j.dot(np.transpose(mesh.vertices))
mesh.vertices = np.transpose(transformed)

# side photos
try:
    file_name = os.path.join(curr_directory, "renders",
                                mesh_name + '_' + "2" + '_render' + '.png')
    # save a render of the object as a png
    png = scene.save_image(resolution=[600, 400], visible=True)

    with open(file_name, 'wb') as f:
        f.write(png)
        f.close()
except BaseException as E:
    print("unable to save image", str(E))

transformed = R36s.dot(np.transpose(mesh.vertices))
mesh.vertices = np.transpose(transformed)


for i in range(3,7):
    transformed = Rx.dot(np.transpose(mesh.vertices))
    mesh.vertices = np.transpose(transformed)

    transformed = R36j.dot(np.transpose(mesh.vertices))
    mesh.vertices = np.transpose(transformed)

    try:
        file_name = os.path.join(curr_directory, "renders",
                                    mesh_name + '_' + str(i)+ '_render' + '.png')
        # save a render of the object as a png
        png = scene.save_image(resolution=[600, 400], visible=True)

        with open(file_name, 'wb') as f:
            f.write(png)
            f.close()
    except BaseException as E:
        print("unable to save image", str(E))
    transformed = R36s.dot(np.transpose(mesh.vertices))
    mesh.vertices = np.transpose(transformed)

transformed = Rx.dot(np.transpose(mesh.vertices))
mesh.vertices = np.transpose(transformed)

transformed = R36s.dot(np.transpose(mesh.vertices))
mesh.vertices = np.transpose(transformed)

transformed = Rf.dot(np.transpose(mesh.vertices))
mesh.vertices = np.transpose(transformed)



#bottom photo
try:
    file_name = os.path.join(curr_directory, "renders",
                                mesh_name + '_' + "7" + '_render' + '.png')

    # save a render of the object as a png
    png = scene.save_image(resolution=[600, 400], visible=True)

    with open(file_name, 'wb') as f:
        f.write(png)
        f.close()
except BaseException as E:
    print("unable to save image", str(E))



transformed = R72j.dot(np.transpose(mesh.vertices))
mesh.vertices = np.transpose(transformed)

#side photos
try:
    file_name = os.path.join(curr_directory, "renders",
                                mesh_name + '_' + "8" + '_render' + '.png')
    # save a render of the object as a png
    png = scene.save_image(resolution=[600, 400], visible=True)

    with open(file_name, 'wb') as f:
        f.write(png)
        f.close()
except BaseException as E:
    print("unable to save image", str(E))


for i in range(9,13):

    transformed = R36s.dot(np.transpose(mesh.vertices))
    mesh.vertices = np.transpose(transformed)

    transformed = Rx.dot(np.transpose(mesh.vertices))
    mesh.vertices = np.transpose(transformed)

    transformed = R36j.dot(np.transpose(mesh.vertices))
    mesh.vertices = np.transpose(transformed)

    try:
        file_name = os.path.join(curr_directory, "renders",
                                    mesh_name + '_' +str(i)+ '_render' + '.png')
        # save a render of the object as a png
        png = scene.save_image(resolution=[600, 400], visible=True)

        with open(file_name, 'wb') as f:
            f.write(png)
            f.close()
    except BaseException as E:
        print("unable to save image", str(E))
        continue


for filename in os.listdir(os.path.join(curr_directory, "renders")):
    if filename.startswith("."):
        continue

    extension = os.path.splitext(filename)[1]
    mesh_name = os.path.splitext(filename)[0]

    if extension != ".png":
        continue

    image = cv2.imread(os.path.join(curr_directory, "renders", filename))
    (thresh, image) = cv2.threshold(image, 254, 255, cv2.THRESH_BINARY)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # Get area 
    area = cv2.countNonZero(image)
    print("Area: " + str(area))

    # Get perimeter (total for all contours)
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    perimeter = 0
    for contour in contours:
        perimeter += int(cv2.arcLength(contour,True))
    print("Perimeter: " + str(perimeter))

    # Compute compactness
    area_2 = cv2.contourArea(contours[0])
    compactness = (perimeter ** 2) / (4 * math.pi * area_2)
    print("Compactness: " + str(compactness))

    # Compute circularity
    circularity = 1 / compactness
    print("Circularity: " + str(circularity))

    # Compute centroid
    M = cv2.moments(contours[0])
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    print("Centroid: (" + str(cX) + ", " + str(cY) + ")")

    # Get axis-aligned bounding box
    x,y,w,h = cv2.boundingRect(contours[0])
    print("\nAxis-aligned bounding box:")
    print("Top-left coordinate: (" + str(x) + ", " + str(y) + ")")
    print("Width: " + str(w))
    print("Height: " + str(h) + "\n")

    # Compute rectangularity (using object oriented bounding box)
    rect = cv2.minAreaRect(contours[0])
    rectangularity = area_2 / (rect[1][0] * rect[1][1])
    print("Rectangularity: " + str(rectangularity))

    # Get diameter
    _,radius = cv2.minEnclosingCircle(contours[0])
    diameter_1 = radius*2
    print("Diameter: " + str(diameter_1))

    # Compute eccentricity
    _,(MA,ma),angle = cv2.fitEllipse(contours[0])
    eccentricity = MA / ma
    print("Eccentricity: " + str(eccentricity))

    # Get length of skeleton
    # Install library opencv-contrib-python to use this!
    skeleton = cv2.ximgproc.thinning(image, thinningType=1)
    skeleton_length = cv2.countNonZero(skeleton)
    print("Length of skeleton: " + str(skeleton_length))
    cv2.imshow("Skeleton", cv2.bitwise_not(skeleton))
    cv2.waitKey()

    print("\n\n")