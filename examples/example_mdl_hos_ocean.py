# =============================================================================
# IMPORT dnora
# =============================================================================
import sys
dnora_directory = '../'
sys.path.insert(0, dnora_directory)
from dnora import grd, mdl, inp
# =============================================================================
# DEFINE MODEL OBJECT
# =============================================================================
grid = grd.Grid()
model = mdl.HOS_ocean(grid=grid)
# =============================================================================
# WRITE OUTPUT FOR HOS-ocean RUN
# =============================================================================
model.write_input_file(input_file_writer=inp.HOS_ocean(
                       xlen=80, ylen=20,T_stop=100,f_out=1,
                       depth = 100, Tp_real=10.5,Hs_real=4.0))
# =============================================================================
# =============================================================================
# HOS-ocean RUN
# =============================================================================
model.run_model()