import numpy as np
import xarray as xr

def grids_to_xarray(grids, labels=None):
    Ngrids = len(grids)
    if labels is None:
        labels = list(range(len(grids)))

    yarray = grids[0].gridy
    xarray = grids[0].gridx

    data = np.zeros(shape=(len(yarray), len(xarray), Ngrids))
    for i,grid in enumerate(grids):
        if not np.array_equal(grid.gridy,yarray) or not np.array_equal(grid.gridx,xarray):
            raise ValueError("grids do not have same geometry")
        data[:,:,i] = grid.z

    model = xr.DataArray(data, coords=[("y", yarray), ("x", xarray), ("grid",labels)], dims=["y", "x", "grid"])
    return model

def grid_to_xarray(grid):
    yarray = grid.gridy
    xarray = grid.gridx
    grid_xarray = xr.DataArray(grid.z, coords=[("y", yarray), ("x", xarray)], dims=["y", "x"])
    return grid_xarray
