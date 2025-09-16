# test.py
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Maximilian Meindl, University of Vienna
"""


from climxtract_utils import (
    load_datasets,
    regrid_all,
    mask_all,
    spatial_mean_timeseries,
    save_reference,
    load_reference,
    compare_to_reference,
)


# Example paths
example_data_path = '/jetfs/scratch/mmeindl/HighResLearn/download/example_data'
processed_data_path = '/jetfs/scratch/mmeindl/HighResLearn/download/example_data_processed'

# Load datasets
datasets = load_datasets(example_data_path)

# Regird datasets
regridded_files = regrid_all(datasets, datasets[0][0], processed_data_path)

# Mask datasets
masked_files = mask_all(regridded_files, datasets[0][0], processed_data_path)

# Merge target and regridded/masked datasets
all_datasets = [datasets[0]] + masked_files

# Calculate spatial means
spatial_means = [spatial_mean_timeseries(ds) for ds in all_datasets]

# First run: save reference
# save_reference(spatial_means, reference_file)

# Later runs: load reference
reference_da = load_reference("reference.nc")

# Comapare to reference
compare = compare_to_reference(spatial_means, reference_da, tol=1e-6)