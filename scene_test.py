import trimesh
import numpy as np
import cv2
import os
import time

curr_directory = os.getcwd()

db_path = os.path.join(curr_directory, "meshes", "flipped")

for filename in os.listdir(db_path):

    extension = os.path.splitext(filename)[1]
    mesh_name = os.path.splitext(filename)[0]

    if extension == ".off" or extension == ".ply":
        mesh_path = os.path.join(db_path, filename)
        mesh = trimesh.load(mesh_path)

    scene = mesh.scene()

    # rotate = trimesh.transformations.rotation_matrix(
    #     angle=np.radians(10.0),
    #     direction=[0, 1, 0],
    #     point=scene.centroid)



    time.sleep(0.5)
    # increment the file name
    try:
        file_name = os.path.join(curr_directory, "images", "renders", mesh_name+'_render' + '.png')
        # save a render of the object as a png
        png = scene.save_image(resolution=[600, 400], visible=True)

        with open(file_name, 'wb') as f:
            f.write(png)
            f.close()
    except BaseException as E:
        print("unable to save image", str(E))
        continue



#black and white images

db_path = os.path.join(curr_directory, "images", "renders")
for filename in os.listdir(db_path):

    extension = os.path.splitext(filename)[1]
    mesh_name = os.path.splitext(filename)[0]

    image = cv2.imread(os.path.join(curr_directory, "images", "renders", mesh_name+'.png'))
    (thresh, blackAndWhiteImage) = cv2.threshold(image, 254, 255, cv2.THRESH_BINARY)
    cv2.imwrite(os.path.join(curr_directory, "images", "bw", mesh_name+'_bw' + '.png'),blackAndWhiteImage)
