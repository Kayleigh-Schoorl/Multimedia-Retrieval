# Multimedia-Retrieval
By:
- Kayleigh Schoorl, k.schoorl@students.uu.nl, 7000286
- Andrei Ungureanu, a.ungureanu@students.uu.nl, 7003218

This repository contains our solution for building a content-based 3D model retrieval system for the assignment for the course Multimedia Retrieval.
This system finds and shows the user the most similar 3D shapes from a 3D shape database, given as input a 3D shape.

## Set up:
First, Meshlab will need to be installed on your computer. To do so, please download here: https://www.meshlab.net/#download

Please make sure make sure the path to your Meshlab installation is included in the environment path variables on your system! You can test this by opening a terminal screen and typing 'meshlab'; this should open the Meshlab program.

This project is written in Python 3.7 and has been tested on Windows and macOS.

The required python libraries can be installed by running the setup.py sript like this:
```
python setup.py develop --user
```
This should install all required libraries automatically. It is recommended to run this on a clean Python 3.7 environment to avoid conflicts with previously installed packages.

Alternatively, the libraries can be installed one by one (or if one is still missing or not working after running setup.py, check the following list if something is missing).
To be able to run all of the scripts in this project, the following Python libraries need to be installed using *pip install*:
- appdirs
- argparse
- llvmlite (possibly needs deinstalling existing installation and reinstalling in order to run pynndescent)
- matplotlib
- meshlabxml
- numba
- numpy
- opencv-contrib-python (deintall previously existing installation of opencv-python and  opencv-contrib-python before installing this!)
- pillow
- pynndescent
- pyvista
- trimesh
- xlsxwriter
- scipy==1.4.1 (it is important that this specific version is installed)
- scikit-learn==0.21.3 (it is important that this specific version is installed)
- vtk
- scooby
- imageio
- meshio
- networkx
- pyglet

## Running the querying system:
First, run the following command:
```
python create_ann_model.py
```
This script creates an Approximate Nearest Neighbor model for searching shapes. This model is stored in a config file which is environment and system specific, so it needs to be remade when running the system on a new system or environment.

Next, the querying system can be called like this:
```
python query_all_steps -M path/to/mesh
```
This will use ANN for searching shapes by default. An optional parameter *-E* or *--exact* can be used to use an exact distance function for searching shapes.

To run any of the scripts, first navigate to the folder they are in and then run it instead of running from a different folder, otherwise it won't be able to find the database.
