from pygridsio.grid import Grid

def read_grid(filename):
    """
    providing the location of a grid (in either .asc or .zmap) read in the grid and return a grid object
    """
    if type(filename) != str:
        filename = str(filename)
    return Grid(filename)
