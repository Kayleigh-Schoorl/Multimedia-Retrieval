import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MMR-Project-KSchoorl-AUngureanu", # Replace with your own username
    version="0.0.1",
    author="Kayleigh Schoorl & Andrei Ungureanu",
    author_email="k.schoorl@students.uu.nl",
    description="Multimedia retrieval project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kayleigh-Schoorl/Multimedia-Retrieval",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyglet',
	    'networkx',
        'meshlabxml',
        'matplotlib',
        'pillow',
        'opencv-contrib-python',
        'pyvista',
        'trimesh',
        'argparse',
        'appdirs',
        'pynndescent',
        'vtk',
        'scooby',
        'imageio',
        'meshio',
        'scipy==1.4.1',
        'scikit-learn==0.21.3',
        'llvmlite',
        'numba',
        'numpy'
    ],
    python_requires='>=3.6',
)