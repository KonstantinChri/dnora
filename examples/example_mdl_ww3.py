# =============================================================================
# IMPORT dnora
# =============================================================================
import sys
dnora_directory = '../'
sys.path.insert(0, dnora_directory)
from dnora import bnd, grd, mdl, wnd

lon_min = 4.0
lat_min = 60.53
lon_max = 5.73
lat_max = 61.25

grid = grd.Grid(lon_min, lon_max, lat_min, lat_max, name='Skjerjehamn250')

model = mdl.WW3(grid, start_time = '2018-08-25T00:00', end_time = '2018-08-25T18:00')

model.import_boundary(bnd.read.MetNo_NORA3())
model.import_forcing(wnd.read.MetNo_NORA3())
model.export_boundary()
model.export_forcing()
