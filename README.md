# AnatomyConstructor

## Description
Software for left ventricle anatomical models construction.

It consist of a number of packages (currently four) which can exchange data with each other using data frame. Packages descriptions and manuals are listed below.

The software was created as a part of my master degree (2017). Some of its tools was initially developed to solve a specific kind of tasks in cardiac modeling and not assumed to be shared beyond this area.

The anatomical model used in this project and its spline implementation is based on:

> Pravdin, S. A Mathematical Spline-Based Model of Cardiac Left Ventricle Anatomy and Morphology. Computation 2016, 4(4), 42; https://doi.org/10.3390/computation4040042

## Installation & run
Here you can find the source code of the project. To start the software run the main_frame.py in terminal (command line):

```
python main_frame.py
```

or you can mark the main_frame.py as executable python program.  

Before the start you must install all the required packages. The best way to do this is to install anaconda project: https://www.anaconda.com/products/individual

Then in terminal:

```
conda install numpy scipy pyqt vtk
```

All the packages will be installed.

## Requirements (last tested version)
1. Python 3 (3.8.11)
2. PyQt5 (5.15.2)
3. vtk (9.0.3)
4. numpy (1.19.5)
5. scipy (1.7.1)

## Full packages description

### SplineMeasurement

The main package to start with. Designed to measure the the left ventricle walls for each of the presented slices using splines. The measured slices will become the basis for the formation of a 3D anatomical model.

To start workin with this package prepare a folder with files containing information about heart slices with a projection on the long axis (apex and base should be visible on the slice). Such information can be given, for example, by an echocardiography procedure. It's better to keep the equal angle between the slices for the reconstruction accuracy. Recommended file formats: jpg, png images with the slices (other possible formats are specified below).

Load the folder with the files (load button). The package will treat the set of files in the folder as left ventricle slices rotated by the same angle along its long axis.

Measurement tools may vary depending on uploaded files formats:
- Image tool if the uploaded formats are: jpg, png.
- Mesh tool if the uploaded format is vtk (2d slices).

Other possible formats: dcm, bmp (image tool), but not tested well.

#### Short control description:

Data:

- Load - load the data folder.

- Upload - save measurements to the data frame (to use in other packages).

Positioning:

- Mark - mark apex-base-base points to change the coordinate system. Model requires apex to be the (0, 0) point.

- Set - change the coordinate system. Use this button when finish marking.

- Remove - remove marking points (visually, if you don't need them).

Geometry:

- Level - set the apex thickness (distance between the epi-endo apex layers). Marked as a small line which is moves along the long axis.

- Set - set apex thickness.

- Ruler - to scale the model (if is needed). Some images may contain ruler with mm details. Set this ruler on the image ruler, change number of mm along the ruler and tap 'Scale'.

Measurements:

- Left/Right meridian - epi-endo wall splines. Epi-endo base points are bind together.

- Reset - reset splines to the default state.

Interaction mode:

Edit left/right epi/endo - add (left mouse click), delete (right mouse click) point to/from the spline. Don't forget to switch off the interaction mode to move the spline points again.

It's recommended to first set positioning and apex thickness for all the slices (actual apex thickness will be taken as average between all the slices). Try to not make the apex thickness vary too much between the slices.   

When all the measurements are finished - tap 'Upload' button and move to Reconstruction package tab.

Comments:

1. Splines used in the package are not "regular" splines used in many graphical packages. Their behavior is closely related to the mathematical formulation of the model and therefore has more restrictions. So, the order of the spline vertices should be preserved, and their location should be in such a way as to preserve the continuity of the spline. If the splines disappear, then try to click several times in the area of their vertices (to interact with the spline object) or tap "Reset" and try to set the vertices again.

### LVSplineReconstruction:

When all spline measurements for all slices are done, you can switch to the reconstruction widget to assemble 3D anatomical model.

Tap "Update" button to load the spline data and then ''Construct" for the Finite-difference mesh. You will see the reconstructured 3D model which can be rotated and zoomed with the vtk engine inside the window.

Several parameters can be set to tune the model:
- psi, phi, gamma - here you can change the model detalization using the special coordinate system (see the paper link in the beginning Readme section). For example, to increase the the number of layers between the epi-endo layers - increase gamma value.
- gamma0, gamma1 - set the transmural rotational angle for the fibers field. When gamma0 = 0 and gamma1 = 1 - you will get 180&deg; rotational angle.  

Tap "Export" near the "Construct" button to export constructed mesh as vtk file.

It's better to visualize the full model with Paraview if you want to better see the fiber fields (problems with the fibers visual scaling so far).

### CUDACubeFiles:

Binary files preparation (switched off by default).

Pass this package if you don't need electrophysiological modeling and don't use weighted scheme.

### DiffuseFibrosis:

Diffuse fibrosis distribution (switched off by default).

Pass this package if you don't need electrophysiological modeling and don't use weighted scheme.
