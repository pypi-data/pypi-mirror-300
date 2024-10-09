from pygridsio.grid import Grid
from pygridsio.grid_to_xarray import grid_to_xarray, grids_to_xarray


def read_grid(filename):
    """
    providing the filename of a grid (in either .asc or .zmap) read in the grid and return a grid object
    """
    if type(filename) != str:
        filename = str(filename)
    return Grid(filename)

def read_grid_to_xarray(filename):
    """
    providing the filename of a grid (in either .asc or .zmap) read in the grid and
    return an xarray object with dimensions:
    x, y, grid
    """
    return grid_to_xarray(filename)

def read_grids_to_xarray(filenames, labels=None):
    """
    providing a list of filenames of multiple grids (in either .asc or .zmap) read in each grid and return
    a xarray object with dimensions:
    x, y, grid

    All grids must have the same dimensions.
    Optionally: provide a list of labels, to name each grid under the xarray "grid" dimension.
    """
    return grids_to_xarray(filenames, labels)
