# pygridsio



## Introduction

This is a python submodule containing IO functionality for reading and writing .asc and .zmap grids, frequently used within the property modelling and temperature modelling pre- and post- processing codes.

## Usage

`from pygridsio.pygridsio import read_grid`

`read_grid(filename)`


## Installation

### Anaconda virtual environment
#### Create/update anaconda environment
The file `environment.yml` can be used to create a working python environment with the needed packages.
For this open an `Anaconda Prompt` and:

`conda env create -f environment.yml`

Or to update the existing anaconda environment (with an updated version of the`environment.yml`file :

`conda env update -n pygridsio -f environment.yml`

#### Export (updated) anaconda environment
The `environment.yml` file needs to be updated when new packages are added:

`conda env export --from-history -n pygridsio > environment.yml`

#### Use anaconda environment in PyCharm
To connect the anaconda environment to Pycharm you can go to `File` , `Settings`, `Project`, `Python Interpreter`, `add interpreter`, `add local interpreter`, `conda environment` and then select the environment you created using the above steps.

## Verify Installation
You can verify the installation of the different python packages by running the tests stored in `tests`. 
In pycharm: Right click on the folder marked `tests` and click on `Run python tests in test`
