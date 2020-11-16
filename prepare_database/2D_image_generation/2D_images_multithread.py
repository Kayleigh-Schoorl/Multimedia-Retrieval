import trimesh
import numpy as np
import cv2
import os
import time
import multiprocessing
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

db_path = os.path.join(curr_directory, "meshes", "flipped")

directions = ["front", "side", "top"]

def get_image_renders(class_name):

    current_files = os.listdir(db_path)

    files = [f for f in current_files if class_name in f]
    for filename in files:

        extension = os.path.splitext(filename)[1]
        mesh_name = os.path.splitext(filename)[0]

        if extension != ".off" and extension != ".ply":
            continue

        if not os.path.exists(os.path.join(curr_directory, "images", "renders", mesh_name)):
            os.makedirs(os.path.join(curr_directory, "images", "renders", mesh_name))

        mesh_path = os.path.join(db_path, filename)
        mesh = trimesh.load(mesh_path)

        for direction in directions:

            if direction == "side":
                R = np.array([[0, 0, 1],
                                [0, 1, 0],
                                [-1, 0, 0]])

                transformed = R.dot(np.transpose(mesh.vertices))
                mesh.vertices = np.transpose(transformed)
            
            elif direction == "top":
                R = np.array([[1, 0, 0],
                    [0, 0, 1],
                    [0, -1, 0]])

                transformed = R.dot(np.transpose(mesh.vertices))
                mesh.vertices = np.transpose(transformed)

            scene = mesh.scene()

            # increment the file name
            try:
                file_name = os.path.join(curr_directory, "images", "renders", mesh_name, mesh_name+'_'+direction+'_render' + '.png')
                # save a render of the object as a png
                png = scene.save_image(resolution=[x, y], visible=True)

                with open(file_name, 'wb') as f:
                    f.write(png)
                    f.close()
            except BaseException as E:
                print("unable to save image", str(E))
                continue


class_names = []
for filename in os.listdir(db_path):
    mesh_name = os.path.splitext(filename)[0]
    class_name = mesh_name.split('_')[0]
    if class_name not in class_names:
        class_names.append(class_name)

if __name__ == '__main__':
    jobs = []
    for c in class_names:
        p = multiprocessing.Process(target=get_image_renders,args=(c,))
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()


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
