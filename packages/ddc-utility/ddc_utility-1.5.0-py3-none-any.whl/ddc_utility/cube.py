
import xarray as xr
from fsspec import AbstractFileSystem
from fsspec.asyn import AsyncFileSystem

from typing import Union
from zarr.storage import FSStore


def open_cube(path: str, fs: Union[AbstractFileSystem, AsyncFileSystem] = None, group: str = None, mode: str = "r", **kwargs):

    store = FSStore(path, mode=mode, fs=fs)

    return xr.open_zarr(store, group=group, **kwargs)
