import trimesh
import numpy as np

mesh = trimesh.load('C:\\Users\\trekk\\Desktop\\MR\\scaled\\Armadillo_284.ply')


scene = mesh.scene()

rotate = trimesh.transformations.rotation_matrix(
        angle=np.pi/2,
        direction=[0, 0, 1],
        point=mesh.centroid)

for i in range(6):

        try:
            # increment the file name
            file_name = 'render_' + str(i) + '.png'
            # save a render of the object as a png
            png = scene.save_image(resolution=[1920, 1080], visible=True)
            with open(file_name, 'wb') as f:
                f.write(png)
                f.close()


        except BaseException as E:
            print("unable to save image", str(E))

        # rotate the camera view transform
        camera_old, _geometry = scene.graph[scene.camera.name]
        camera_new = np.dot(rotate, camera_old)

        # apply the new transform
        scene.graph[scene.camera.name] = camera_new