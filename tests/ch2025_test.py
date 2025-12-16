# ch2025_test.py
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Maximilian Meindl, University of Vienna
"""

# import load, regrid and mask function from climxtract package
from climxtract import load
from climxtract import regrid
from climxtract import mask


# Define test parameters 
variable = "tas"
variable = "tasmax"

# Define output paths for downloading climate data
output_path_ch2025 = "/jetfs/scratch/mmeindl/HighResLearn/download/CH2025"
output_path_destine = "/jetfs/scratch/mmeindl/HighResLearn/download/DESTINE"
output_path_cordex = "/jetfs/scratch/mmeindl/HighResLearn/download/CORDEX"

# Define output paths for regridding and masking 
output_path_regridded = "/jetfs/home/mmeindl/ClimXtract/tests"
output_path_masked = "/jetfs/home/mmeindl/ClimXtract/tests"

"""
1. Download example data for CH2025 (statistically downscaled climate scenarios for Switzerland)
"""

# Download CH2025 data
t_ch2025 = load(
    type="ch2025",
    model_global = "mpiesm",
    model_regional = "smhi-rca",
    resolution = None,
    variable = variable,
    experiment = "ref91-20",
    ens = None,
    start = None,
    end = None,
    output_path = output_path_ch2025
)

# Download DestinE data
t_destine = load(
    type="destine",
    model_global = "ICON",
    model_regional = None,
    resolution = None,
    variable = variable,
    experiment = "SSP3-7.0",
    ens = None,
    start = "20200901",
    end = "20200930",
    output_path = output_path_destine
)

# Download EURO-CORDEX data
t_cordex = load(
    type="eurocordex",
    model_global = "MPI-M-MPI-ESM-LR",
    model_regional = "RCA4",
    resolution = "EUR-11"
    variable = variable,
    experiment = "rcp45",
    ens = "r1i1p1",
    start = "20160101",
    end = "20201231",
    output_path = output_path_cordex
)


"""
2. Regridding
"""

# Regrid the destine dataset to the CH 2025 grid
t_regrid_cordex = regrid(type='distance', target_file=t_ch2025[0], input_file=t_cordex[0], output_path_regrid=output_path_regridded)
t_regrid_destine = regrid(type='distance', target_file=t_ch2025[0], input_file=t_destine[0], output_path_regrid=output_path_regridded)

"""
3. Masking
"""

# Apply the CH2025 spatial mask to the regridded destine dataset
t_mask_cordex = mask(target_grid=t_ch2025[0], input_grid=t_regrid_cordex[0], output_path_mask=output_path_masked)
t_mask_destine = mask(target_grid=t_ch2025[0], input_grid=t_regrid_destine[0], output_path_mask=output_path_masked)
