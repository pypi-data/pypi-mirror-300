[![Build status](https://github.com/ElenaTerzic/Basins/actions/workflows/build_python.yml/badge.svg)](https://github.com/ElenaTerzic/Basins/actions)
[![Build status](https://github.com/ElenaTerzic/Basins/actions/workflows/build_gcc.yml/badge.svg)](https://github.com/ElenaTerzic/Basins/actions)
[![Build status](https://github.com/ElenaTerzic/Basins/actions/workflows/build_intel.yml/badge.svg)](https://github.com/ElenaTerzic/Basins/actions)
[![License](https://img.shields.io/badge/license-GPL3-orange)](https://opensource.org/license/gpl-3-0/)

# Basins

This project contains tools to specify regions of interest when analysing float, satellite or model data. They are managed through a C++ interface for maximum performance and contain data extracted from shapefiles.

The code has been optimized under AVX/AVX2 vectorization directives using the Intel(r) C++ compiler (icpc). Although this is the **default** compilation mode, it is not strictly required as the makefile will automatically default to GNU if the Intel compilers are not found.

The default optimization mode is *fast* although it can be changed using the variable **OPTL**, e.g.,
```bash
make OPTL=2
```

## Deployment

A _Makefile_ is provided within the tool to automate the installation for easiness of use for the user. To install the tool simply create a virtual environment as stated below or use the system Python. Once this is done simply type:
```bash
make
```
This will install all the requirements and install the package to your active python. To uninstall simply use
```bash
make uninstall
```

The previous operations can be done one step at a time using
```bash
make requirements
```
to install all the requirements;
```bash
make python
```
to compile and;
```bash
make install
```
to install the tool.

### Virtual environment

The package can be installed in a Python virtual environement to avoid messing with the system Python installation.
Next, we will use [Conda](https://docs.conda.io/projects/conda/en/latest/index.html) for this purpose.
Assuming that Conda is already installed, we can create a virtual environment with a specific python version and name (`my_env`) using
```bash
conda create -n my_env python=3.8
```
The environment is placed in `~/.conda/envs/my_env`.
Next we activate it be able to install packages using `conda` itself or another Python package manager in the environment directory:
```bash
conda activate my_env
```
Then just follow the instructions as stated above.

## Python implementation

The basins module solves the 2D point in polygon problem in order to verify if a point is inside a geometry.

It defines the following basic entities:
* *Point*
* *Vector (internal)*
* *Ball*
* *Polygon*
* Line
* SimpleRectangle
* Rectangle
* Plane
* SimpleCube
* Cube

as well as the *basin* entity defined by an array of points. A number of predefined basins are included from different sources. The generic basins are:
* **med**, Mediterranean Sea
* **wmed**, Western Mediterranean
* **emed**, Eastern Mediterranean
* **socean**, Southern Ocean
* **kotor**, Bay of Kotor

The methods *isinside(Point)* or *areinside(np.array)* can be used to check if a point or a set of points are inside (True) or outside (False) the region.
```python
p1 = Basins.Point(0.5,0.5,0.5)
inside = Basins.med.isinside(p1)
inside = Basins.med > p1 # alternative to isinside
```
and the same works for numpy arrays using *areinside*
```python
xyzp   = np.array([[.5,.5,0.1],[1.,.35,0.6],[0.2,0.5,1.2],[.35,.15,0.5]])
inside = Basins.med.areinside(xyzp)
inside = Basins.med > xyzp
```
Note that the operator *>* is more generic and is able to understand if the input data is a Point or a numpy array of points.

### Basins information tool

The command line tool *basins_info* provides basic info about the available basins inside this tool. To list all the basins just run:
```bash
basins_info -l
```

Information on different basins can be obtained by the command:
```bash
basins_info -b <module>.<basin>
```
where **module** is the group where the basin belongs (eg., worldseas) and **basin** its name (eg. kotor). Using either _-d_ or _--display__ a plot of the basin will be generated. The polygon that forms the basin can be dumped to a text file as shown in this example:
```bash
basins_info -b worldseas.adr -p poly_adr.txt
```
which will store the polygon forming the Adriatic sea into the file **poly_adr.txt**.