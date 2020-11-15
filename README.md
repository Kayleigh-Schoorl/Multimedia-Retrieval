# Multimedia-Retrieval
By:
- Kayleigh Schoorl, k.schoorl@students.uu.nl, 7000286
- Andrei Ungureanu, a.ungureanu@students.uu.nl, 7003218

This repository contains our solution for building a content-based 3D model retrieval system for the assignment for the course Multimedia Retrieval.
This system finds and shows the user the most similar 3D shapes from a 3D shape database, given as input a 3D shape.

To run scripts, first navigate to the folder they are in and then run it!

To be able to run all of the scripts in this project, the following Python libraries need to be installed first (please note this list might not be fully exhaustive):
- appdirs
- argparse
- json
- llvmlite (possibly needs deinstalling existing installation en reinstalling to run pynndescent)
- matplotlib
- meshlabxml
- numba
- numpy
- opencv-contrib-python (deintall opencv-python and possible existing installation of opencv-contrib-python before installing this!)
- pillow
- pylab
- pynndescent
- pyvista
- trimesh
- xlsxwriter

Also, Meshlab will need to be installed on your computer. To do so, please download here: https://www.meshlab.net/#download
Please make sure make sure the path to your Meshlab installation is included in the environment path variables on your system!! You can test this by opening a terminal screen and typing 'meshlab'; this should open the Meshlab program.
