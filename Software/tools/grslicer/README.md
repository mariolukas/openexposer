# About #

GRSlicer is a simple 3D model slicer that produces 3D printing instructions in a form of RepRap flavored G-Code.
The printing path is optimized so that it takes the shortest travel paths (paths on which material is not extruded).

GRSlicer is written in Python and uses the following packages:

- [Pyclipper](https://github.com/greginvm/pyclipper) Python bindings for [Angus Johnson's Clipper library](http://www.angusj.com/delphi/clipper.php) for polygon clipping and offseting operations,
- [numpy](http://www.numpy.org/) for vector and matrix operations,
- [QuadTree](https://pypi.python.org/pypi/Quadtree/) for path optimization,
- [Cython](http://cython.org/docs/0.22/) for making some things a bit faster.

This repository is a rewrite of a GRSlicer that I made last year and never published. The rewrite is still work in progress, so stay tuned if you are interested in another slicer.

The full graphical user interface in a form of a web application will be published soon in a separate repository [GRSlicer-web](https://github.com/greginvm/grslicer-web).

## Supported formats ##

Input:

- ASCII STL
- Binary STL

Output:

- G-Code (RepRap flavored)