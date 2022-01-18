# AnatomyConstructor

## Description
Multipurpose set of packages for application in the construction of heart anatomical models

to start the application run the main_frame.py

## Requirements
1. PyQt5 (verison = 4)
2. vtk (version >= 6)
3. numpy
4. scipy

## Code features

Java-style code formatting:

Every file contains only one class

Getters and setters methods instead of properties decorators (not a pythonic way)

Methods:

Underscore (_) in front of protected/private methods (not distinguish them)

## Packages

**SplineMeasurement:**

*To provide left ventricle measurement based on var-base spline algorithm*

**LVSplineReconstruction:**

*To reconstruct left ventricle anatomical model based on var-base spline algorithm* 

**CUDACubeFiles:**

*To prepare the binary files needed to compute on CUDA-program (Panfilov group)*

**DiffuseFibrosis:**

*Diffuse fibrosis modeling for a CUDA-program (Panfilov group)*

## Additions

**GuiStylizedWidgets:**

*New style for a Qt gui widgets*

**DataExamples:**

Contains vtk slices for SplineMeasurement package

## Problems

*LVSplineReconstruction:*

Problems with a delaunay2D vtk algorithm in case of strong curvature of left ventricle
model gives a bad triangles near the base

Problems with a delaunay2D vtk algorithm for triangulation with a holes. May lead to
a program crashes


