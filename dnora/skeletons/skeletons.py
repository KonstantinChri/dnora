import numpy as np
import pandas as pd
import xarray as xr
import utm

class Skeleton:
    _x_str = 'x'
    _y_str = 'y'
    _name = 'LonelySkeleton'

    def x(self) -> np.ndarray:
        if self.x_str == 'lon':
            x, __, __, __ = utm.from_latlon(self.lat(), self.lon(), force_zone_number=33, force_zone_letter='W')
            return x

        if hasattr(self, 'data') and hasattr(self.data, 'x'):
            return self.data.x.values
        else:
            return None

    def y(self) -> np.ndarray:
        if self.y_str == 'lat':
            __, y, __, __ = utm.from_latlon(self.lat(), self.lon(), force_zone_number=33, force_zone_letter='W')
            return y

        if hasattr(self, 'data') and hasattr(self.data, 'y') :
            return self.data.y.values
        else:
            return None

    def lon(self) -> np.ndarray:
        if self.x_str == 'x':
            __, lon = utm.to_latlon(self.x(), self.y(), 33, zone_letter = 'W', strict = False)
            return lon

        if hasattr(self, 'data') and hasattr(self.data, 'lon'):
            return self.data.lon.values
        else:
            return None

    def lat(self) -> np.ndarray:
        if self.y_str == 'y':
            lat, __ = utm.to_latlon(self.x(), self.y(), 33, zone_letter = 'W', strict = False)
            return lat

        if hasattr(self, 'data') and hasattr(self.data, 'lat') :
            return self.data.lat.values
        else:
            return None

    def lon_edges(self) -> tuple:
        return (np.min(self.lon()), np.max(self.lon()))

    def lat_edges(self) -> tuple:
        return (np.min(self.lat()), np.max(self.lat()))

    def x_edges(self) -> tuple:
        return (np.min(self.x()), np.max(self.x()))

    def y_edges(self) -> tuple:
        return (np.min(self.y()), np.max(self.y()))

    def native_x_edges(self) -> tuple:
        return (np.min(self.native_x()), np.max(self.native_x()))

    def native_y_edges(self) -> tuple:
        return (np.min(self.native_y()), np.max(self.native_y()))

    def nx(self):
        return len(self.native_x())

    def ny(self):
        return len(self.native_y())

    def dlon(self):
        if self.nx() == 1:
            return 0.
        return (self.lon_edges()[1]-self.lon_edges()[0])/(self.nx()-1)

    def dlat(self):
        if self.ny() == 1:
            return 0.
        return (self.lat_edges()[1]-self.lat_edges()[0])/(self.ny()-1)

    def dx(self):
        if self.nx() == 1:
            return 0.
        return (self.x_edges()[1]-self.x_edges()[0])/(self.nx()-1)

    def dy(self):
        if self.ny() == 1:
            return 0.
        return (self.y_edges()[1]-self.y_edges()[0])/(self.ny()-1)

    def native_dx(self):
        if self.nx() == 1:
            return 0.
        return (self.native_x_edges()[1]-self.native_x_edges()[0])/(self.nx()-1)

    def native_dy(self):
        if self.ny() == 1:
            return 0.
        return (self.native_y_edges()[1]-self.native_y_edges()[0])/(self.nx()-1)

    @property
    def x_str(self) -> str:
        return self._x_str

    @x_str.setter
    def x_str(self, new_str):
        if new_str in ['x', 'lon']:
            self._x_str = new_str
        else:
            raise ValueError("x_str need to be 'x' or 'lon'")

    @property
    def y_str(self) -> str:
        return self._y_str

    @y_str.setter
    def y_str(self, new_str):
        if new_str in ['y', 'lat']:
            self._y_str = new_str
        else:
            raise ValueError("y_str need to be 'y' or 'lat'")

    @property
    def name(self) -> str:
        return self._name

    @x_str.setter
    def name(self, new_name):
        if isinstance(new_name, str):
            self._name = new_name
        else:
            raise ValueError("name needs to be a string")

    def native_x(self) -> np.ndarray:
        if self.x_str == 'x':
            return self.x()
        elif self.x_str == 'lon':
            return self.lon()
        else:
            return None

    def native_y(self) -> np.ndarray:
        if self.y_str == 'y':
            return self.y()
        elif self.y_str == 'lat':
            return self.lat()
        else:
            return None

    def time(self):
        if hasattr(self, 'data') and hasattr(self.data, 'time'):
            return self.data.time.values
        else:
            return None

    def _ds_vars_dict(self):
        """Return variable dictionary for creating xarray Dataset"""
        return {}

    def _ds_coords_dict(self):
        """Return variable dictionary for creating xarray Dataset"""
        return {}

    def compile_to_ds(self, data, data_name:str, additional_coords: dict=None):
        def check_consistency():
            for i, key in enumerate(coords_dict.keys()):
                if i > len(data.shape)-1:
                    raise Exception(f'{key} coordinate is {len(coords_dict[key])} long, but that dimension doesnt exist in the data!!!')
                if len(coords_dict[key]) != data.shape[i]:
                    raise Exception(f'{key} coordinate is {len(coords_dict[key])} long, but size of data in that dimension (dim {i}) is {data.shape[i]}!!!')

        # Coordinates
        coords_dict = self._ds_coords_dict()
        if additional_coords is not None:
            for key, value in additional_coords.items():
                coords_dict[key] = value

        # Data variables
        vars_dict = self._ds_vars_dict()
        vars_dict[data_name] = (list(coords_dict.keys()),data)

        check_consistency()

        return xr.Dataset(data_vars=vars_dict, coords=coords_dict)

    def merge_in_ds(self, ds_list: list[xr.Dataset]):
        if not isinstance(ds_list, list):
            ds_list = [ds_list]
        for ds in ds_list:
            self.data = self.data.merge(ds)

class PointSkeleton(Skeleton):
    def __init__(self, x=None, y=None, lon=None, lat=None, time=None, name='PointyData'):
        self.data = self._create_structure(x, y, lon, lat, time)
        self.data.attrs['name'] = name

    def _create_structure(self, x=None, y=None, lon=None, lat=None, time=None):
        native_x, native_y, xvec, yvec = check_input_consistency(x, y, lon, lat)
        if len(xvec) != len(yvec):
            raise Exception('x and y vector has to be equally long!')
        self.x_str = native_x
        self.y_str = native_y

        return self._init_ds(x=xvec,y=yvec, time=time)

    def _init_ds(self, x: np.ndarray, y: np.ndarray, time=None) -> xr.Dataset:
        coords_dict = {'inds': np.arange(len(x))}
        vars_dict = {self.x_str: (['inds'], x), self.y_str: (['inds'], y)}
        if time is not None:
            vars_dict['time'] = (['station'], time)
        return xr.Dataset(coords=coords_dict, data_vars=vars_dict, attrs={'name': self.name})

    def _ds_coords_dict(self):
        """Return coordinate dictionary for creating xarray Dataset"""
        coords_dict = {'inds': self.inds()}
        if self.time() is not None:
            coords_dict['time'] = self.time()
        return coords_dict

    def _ds_vars_dict(self):
        """Return variable dictionary for creating xarray Dataset"""
        vars_dict = {self.x_str: (['inds'], self.native_x()), self.y_str: (['inds'], self.native_y())}
        return vars_dict

    def inds(self) -> np.ndarray:
        if hasattr(self.data, 'inds') :
            return self.data.inds.values
        else:
            return None

class GriddedSkeleton(Skeleton):
    def __init__(self, x=None, y=None, lon=None, lat=None, time=None, name='GriddedData'):
        self.data = self._create_structure(x, y, lon, lat, time)
        self.data.attrs['name'] = name

    def _create_structure(self, x=None, y=None, lon=None, lat=None, time=None):
        native_x, native_y, xvec, yvec = check_input_consistency(x, y, lon, lat)

        self.x_str = native_x
        self.y_str = native_y

        return self._init_ds(x=xvec, y=yvec, time=time)

    def _init_ds(self, x: np.ndarray, y: np.ndarray, time=None) -> xr.Dataset:
        coords_dict = {self.y_str: y, self.x_str: x}
        if time is not None:
            coords_dict['time'] = time
        return xr.Dataset(coords=coords_dict, attrs={'name': self.name})

    def _ds_coords_dict(self):
        """Return coordinate dictionary for creating xarray Dataset"""
        coords_dict = {self.y_str: self.native_y(), self.x_str: self.native_x()}
        if self.time() is not None:
            coords_dict['time'] = self.time()
        return coords_dict

    def size(self) -> tuple[int, int]:
        """Returns the size (nx, ny) of the grid."""
        return (self.ny(), self.nx())

def check_input_consistency(x, y, lon, lat):
    xy = False
    lonlat = False

    if x is not None and y is not None:
        xy = True
        native_x = 'x'
        native_y = 'y'
        xvec = x
        yvec = y

    if lon is not None and lat is not None:
        lonlat = True
        native_x = 'lon'
        native_y = 'lat'
        xvec = lon
        yvec = lat

    if xy and lonlat:
        raise Exception("Can't set both lon/lat and x/y!")

    if not xy and not lonlat:
        raise Exception('Have to set either lon/lat or x/y!')

    return native_x, native_y, np.array(xvec), np.array(yvec)
