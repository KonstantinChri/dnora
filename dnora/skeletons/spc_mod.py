from point_skeleton import PointSkeleton
from gridded_skeleton import GriddedSkeleton
import numpy as np
from power_spectrum import PowerSpectrum
from coordinates import include_time, include_frequency, include_direction
from datetime import datetime, timedelta
#@include_time(grid_coord=True)
@include_frequency(grid_coord=False)
class Spectra(PointSkeleton, PowerSpectrum):
    def __init__(self, grid=None, x=None, y=None, lon=None, lat=None, name: str="AnonymousSpectra"):
        self._name = name
        if grid is not None:
            x, y = grid.xy(strict=True)
            lon, lat = grid.lonlat(strict=True)
        self.data = self._create_structure(x, y, lon, lat, freq=np.array([0.1,0.2,0.3]))
        self._reset_vars()

@include_direction(grid_coord=False)
@include_frequency(grid_coord=False)
@include_time(grid_coord=False)
class Boundary(PointSkeleton, PowerSpectrum):
    def __init__(self, grid=None, x=None, y=None, lon=None, lat=None, name: str="AnonymousSpectra"):
        self._name = name
        if grid is not None:
            x, y = grid.xy(strict=True)
            lon, lat = grid.lonlat(strict=True)
        t = np.arange(datetime(2020,1,1), datetime(2020,1,2), timedelta(hours=1)).astype(datetime)
        self.data = self._create_structure(x, y, lon, lat, time=t, freq=np.array([0.1,0.2,0.3]), dirs=np.array([0, 45, 90, 135, 180, 225, 270, 315]))
        self._reset_vars()
# class Boundary(PointSkeleton, WaveSpectrum2D):
#     def __init__(self, grid=None, x=None, y=None, lon=None, lat=None, name: str="AnonymousSpectra"):
#         self._name = name
#         if grid is not None:
#             x, y = grid.xy(strict=True)
#             lon, lat = grid.lonlat(strict=True)
#         self.data = self._create_structure(x, y, lon, lat, freq=np.array([0.1,0.2,0.3]), dirs=np.linspace(0,350,36))
#
#
# class GriddedSpectra(GriddedSkeleton, WaveSpectrum):
#     def __init__(self, grid=None, x=None, y=None, lon=None, lat=None, name: str="AnonymousSpectra"):
#         self._name = name
#         if grid is not None:
#             x, y = grid.x(strict=True), grid.y(strict=True)
#             lon, lat = grid.lon(strict=True), grid.lat(strict=True)
#         self.data = self._create_structure(x, y, lon, lat, freq=np.array([0.1,0.2,0.3]))
