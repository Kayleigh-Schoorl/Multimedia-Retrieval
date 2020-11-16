import trimesh
import numpy as np
import os
import math
import cv2
import platform 

os.chdir("..")
os.chdir("..")
curr_directory = os.getcwd()

x = 1200
y = 800

# Check for OSX since for some reason it will double the image size
if platform.system() == 'Darwin':
    x = int(x/2)
    y = int(y/2)

ANGLE72 = math.radians(72)
ANGLE36 = math.radians(36)
ANGLE72m = math.radians(-72)
ANGLE36m = math.radians(-36)

db_path = os.path.join(curr_directory, "meshes", "test")

# Rx = np.array([[1, 0, 0],
#                [0, math.cos(ANGLE72), -math.sin(ANGLE72)],
#                [0, math.sin(ANGLE72), math.cos(ANGLE72)]])
#
# R72j = np.array([[math.cos(ANGLE72), 0, math.sin(ANGLE72)],
#                [0, 1, 0],
#                [-math.sin(ANGLE72), 0, math.cos(ANGLE72)]])
#
# R36j = np.array([[math.cos(ANGLE36), 0, math.sin(ANGLE36)],
#                [0, 1, 0],
#                [-math.sin(ANGLE36), 0, math.cos(ANGLE36)]])
#
# R72s = np.array([[math.cos(ANGLE72m), 0, math.sin(ANGLE72m)],
#                [0, 1, 0],
#                [-math.sin(ANGLE72m), 0, math.cos(ANGLE72m)]])
#
# R36s = np.array([[math.cos(ANGLE36m), 0, math.sin(ANGLE36m)],
#                [0, 1, 0],
#                [-math.sin(ANGLE36m), 0, math.cos(ANGLE36m)]])


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


for filename in os.listdir(db_path):

    extension = os.path.splitext(filename)[1]
    mesh_name = os.path.splitext(filename)[0]

    if extension != ".off" and extension != ".ply":
        continue

    if not os.path.exists(os.path.join(curr_directory, "images", "renders", mesh_name)):
        os.makedirs(os.path.join(curr_directory, "images", "renders", mesh_name))

    mesh_path = os.path.join(db_path, filename)
    mesh = trimesh.load(mesh_path)

    scene = mesh.scene()
    scene.camera.fov = [70., 80.]

    #top photo
    try:
        file_name = os.path.join(curr_directory, "images", "renders", mesh_name,
                                 mesh_name + '_' + "1" + '_render' + '.png')
        # save a render of the object as a png
        png = scene.save_image(resolution=[x, y], visible=True)

        with open(file_name, 'wb') as f:
            f.write(png)
            f.close()
    except BaseException as E:
        print("unable to save image", str(E))
        continue

    transformed = R72j.dot(np.transpose(mesh.vertices))
    mesh.vertices = np.transpose(transformed)

    # side photos
    try:
        file_name = os.path.join(curr_directory, "images", "renders", mesh_name,
                                 mesh_name + '_' + "2" + '_render' + '.png')
        # save a render of the object as a png
        png = scene.save_image(resolution=[x, y], visible=True)

        with open(file_name, 'wb') as f:
            f.write(png)
            f.close()
    except BaseException as E:
        print("unable to save image", str(E))
        continue

    transformed = R36s.dot(np.transpose(mesh.vertices))
    mesh.vertices = np.transpose(transformed)


    for i in range(3,7):
        transformed = Rx.dot(np.transpose(mesh.vertices))
        mesh.vertices = np.transpose(transformed)

        transformed = R36j.dot(np.transpose(mesh.vertices))
        mesh.vertices = np.transpose(transformed)

        try:
            file_name = os.path.join(curr_directory, "images", "renders", mesh_name,
                                     mesh_name + '_' + str(i)+ '_render' + '.png')
            # save a render of the object as a png
            png = scene.save_image(resolution=[x, y], visible=True)

            with open(file_name, 'wb') as f:
                f.write(png)
                f.close()
        except BaseException as E:
            print("unable to save image", str(E))
            continue
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
        file_name = os.path.join(curr_directory, "images", "renders", mesh_name,
                                 mesh_name + '_' + "7" + '_render' + '.png')

        # save a render of the object as a png
        png = scene.save_image(resolution=[x, y], visible=True)

        with open(file_name, 'wb') as f:
            f.write(png)
            f.close()
    except BaseException as E:
        print("unable to save image", str(E))
        continue



    transformed = R72j.dot(np.transpose(mesh.vertices))
    mesh.vertices = np.transpose(transformed)

    #side photos
    try:
        file_name = os.path.join(curr_directory, "images", "renders", mesh_name,
                                 mesh_name + '_' + "8" + '_render' + '.png')
        # save a render of the object as a png
        png = scene.save_image(resolution=[x, y], visible=True)

        with open(file_name, 'wb') as f:
            f.write(png)
            f.close()
    except BaseException as E:
        print("unable to save image", str(E))
        continue


    for i in range(9,13):

        transformed = R36s.dot(np.transpose(mesh.vertices))
        mesh.vertices = np.transpose(transformed)

        transformed = Rx.dot(np.transpose(mesh.vertices))
        mesh.vertices = np.transpose(transformed)

        transformed = R36j.dot(np.transpose(mesh.vertices))
        mesh.vertices = np.transpose(transformed)

        try:
            file_name = os.path.join(curr_directory, "images", "renders", mesh_name,
                                     mesh_name + '_' +str(i)+ '_render' + '.png')
            # save a render of the object as a png
            png = scene.save_image(resolution=[x, y], visible=True)

            with open(file_name, 'wb') as f:
                f.write(png)
                f.close()
        except BaseException as E:
            print("unable to save image", str(E))
            continue


rendered_images_path = os.path.join(curr_directory, "images", "renders")

for folder in os.listdir(rendered_images_path):
    if folder.startswith("."):
        continue
    for filename in os.listdir(os.path.join(rendered_images_path, folder)):

        extension = os.path.splitext(filename)[1]
        mesh_name = os.path.splitext(filename)[0]

        if extension != ".png":
            continue

        if not os.path.exists(os.path.join(curr_directory, "images", "bw", folder)):
            os.makedirs(os.path.join(curr_directory, "images", "bw", folder))

        image = cv2.imread(os.path.join(curr_directory, "images", "renders", folder, mesh_name+'.png'))
        (thresh, blackAndWhiteImage) = cv2.threshold(image, 254, 255, cv2.THRESH_BINARY)
        cv2.imwrite(os.path.join(curr_directory, "images", "bw", folder, mesh_name+'_bw' + '.png'),blackAndWhiteImage)
