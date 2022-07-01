import numpy as np
import pandas as pd
import xarray as xr
import utm
from copy import copy
from skeleton import Skeleton
from skeleton_dataset import SkeletonDataset

class PointSkeleton(Skeleton, SkeletonDataset):
    """Gives a unstructured structure to the Skeleton.

    In practise this means that:

    1) Grid coordinates are defined with and index (inds),
    2) x,y / lon/lat values are data variables of the index.
    3) Methods x(), y() / lon(), lat() will returns all points.
    4) Methods xy() / lonlat() are identical to e.g. (x(), y()).
    """

    # def __init__(self, x=None, y=None, lon=None, lat=None, time=None, name='PointyData'):
    #     self.data = super()._create_structure(x, y, lon, lat, time)
    #     self.data.attrs['name'] = name

    def _init_ds(self, x: np.ndarray, y: np.ndarray, **kwargs) -> xr.Dataset:
        """Creates a Dataset containing the index variable as a coordinate and
        spatial coordinates as data variables on this index.

        Any additional keyword arguments are also added to the coordinate list.
        """
        coords_dict = {'inds': np.arange(len(x))}

        for key, value in kwargs.items():
            coords_dict[key] = value

        vars_dict = {self.x_str: (['inds'], x), self.y_str: (['inds'], y)}

        return xr.Dataset(coords=coords_dict, data_vars=vars_dict, attrs={'name': self.name})

    def inds(self) -> np.ndarray:
        return super()._get('inds')

    def lonlat(self, mask: np.array=None, strict=False) -> tuple[np.ndarray, np.ndarray]:
        """Returns a tuple of longitude and latitude of all points.
        Identical to (.lon(), .lat()) (with no mask)

        mask is a boolean array (default True for all points)
        """
        if mask is None:
            mask = np.full((self.nx(),), True)

        lon, lat = super().lon(strict=strict)[mask], super().lat(strict=strict)[mask]

        if lon is None:
            return None, None

        return lon[mask], lat[mask]

    def xy(self, mask: np.array=None, strict=False) -> tuple[np.ndarray, np.ndarray]:
        """Returns a tuple of x and y of all points.
        Identical to (.x(), .y()) (with no mask)

        mask is a boolean array (default True for all points)
        """
        if mask is None:
            mask = np.full((super().nx(),), True)

        x, y = super().x(strict=strict)[mask], super().y(strict=strict)[mask]

        if x is None:
            return None, None

        return x[mask], y[mask]

    def native_xy(self, mask: np.array=None, **kwargs) -> tuple[np.ndarray, np.ndarray]:
        """Returns a tuple of native x and y of all points.
        Identical to (.native_x(), .native_y()) (with no mask)

        mask is a boolean array (default True for all points)
        """
        if mask is None:
            mask = np.full((super().nx(),), True)

        return super().native_x()[mask], super().native_y()[mask]
