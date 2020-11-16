import math
import numpy as np
import os
import platform

def generate(mesh):

    visible = True

    x = 1200
    y = 800
    
    # Check for OSX since for some reason it will double the image size
    if platform.system() == 'Darwin':
        x = int(x/2)
        y = int(y/2)

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
        png = scene.save_image(resolution=[1200, 800], visible=visible)

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
        png = scene.save_image(resolution=[x, y], visible=visible)

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
            png = scene.save_image(resolution=[x, y], visible=visible)

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
        png = scene.save_image(resolution=[x, y], visible=visible)

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
        png = scene.save_image(resolution=[x, y], visible=visible)

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
            png = scene.save_image(resolution=[x, y], visible=visible)

            with open(file_name, 'wb') as f:
                f.write(png)
                f.close()
        except BaseException as E:
            print("unable to save image", str(E))
            continue
