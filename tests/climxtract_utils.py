# climxtract_utils.py
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Maximilian Meindl, University of Vienna
"""

import os
import xarray as xr
import numpy as np
import climxtract as cxt


def load_datasets(path, extension=".nc", max_files=6):
    """
    Load up to 'max_files' xarray datasets from a directory using os.

    Args:
        path (str): Root directory where example datasets are stored
        extentsion (str): File extension to search for. Default is ".nc".
        max_files (int): Maximum number of files to load. Default is 6.

    Returns:
        list of of tuples: Each element is (filepath, xarray.Dataset)
    """

    # List all files
    files = []
    for root, _, filenames in os.walk(path):
        for fname in filenames:
            if fname.endswith(extension):
                files.append(os.path.join(root, fname))

    files = sorted(files, key=lambda f: os.path.getmtime(f))
    datasets = [(f, xr.open_dataset(f)) for f in files]
    return datasets


def regrid_all(datasets, target_file, output_path_regrid):
    """
    Regrid a list of datasets using cxt.regrid

    Args:
        datasets (list): List of (path, xr.Dataset) tuples
        target_file (str): Path to target grid
        output_path_regrid (str): Directory to save regridded files

    Returns:
        list of regridded file paths
    """
    os.makedirs(output_path_regrid, exist_ok=True)
    results = []

    for (path, _) in datasets:
        # skip target file
        if os.path.abspath(path) == os.path.abspath(target_file):
            continue

        result = cxt.regrid(
            type='distance',
            target_file=target_file,
            input_file=path,
            output_path_regrid=output_path_regrid
        )
        results.append(result)

    return results


def mask_all(regridded_files, target_grid, output_path_mask):
    """
    Apply spatial masking to regridded datasets.

    Args:
        regridded_datasets (list): List of (path, xr.Dataset) tuples returned by regrid_all
        target_grid (str): Path to target grid
        output_mask_mask (str): Directory to save masked files

    Returns:
        list: Results
    """
    os.makedirs(output_path_mask, exist_ok=True)
    results = []

    for (path, _) in regridded_files:
        if os.path.abspath(path) == os.path.abspath(target_grid):
            continue

        result = cxt.mask(
            target_grid=target_grid,
            input_grid=path,
            output_path_mask=output_path_mask
        )
        results.append(result)

    return results


def spatial_mean_timeseries(dataset, var='tas', start_date='2020-09-01', end_date='2020-09-30'):
    """
    Calculate spatial mean over x and y for a given dataset and time slice.

    Args:
        dataset (xr.Dataset):
        var (str): Variable name to calculate mean for (default: 'tas')
        start_date (str): Start of time slice
        end_date (str): End of time slice

    Returns:
        xr.DataArray: Time series of spatial mean
    """
    # extract xr.Dataset if it's a tuple
    ds = dataset[1] if isinstance(dataset, tuple) else dataset

    # normalize time to to make daily values align
    ds['time'] = ds['time'].dt.floor('D')

    # select time slice and variable
    ds_slice = ds[var].sel(time=slice(start_date, end_date))

    # calculate mean over spatial dimensions
    return ds_slice.mean(dim=['x', 'y'])


def save_reference(spatial_means, output_path):
    """
    Save spatial means (list of xarray.DataArray) as a single NetCDF for reference.

    Args:
        spatial_means (list of xr.DataArray): List of 6 DataArrays
        output_path (str): File path to save reference NetCDF
    """
    combined = xr.concat(spatial_means, dim='dataset')
    combined = combined.assign_coords(dataset=[f'dataset_{i}' for i in range(len(spatial_means))])
    combined.to_netcdf(output_path)
    print(f"Reference results saved to {output_path}")


def load_reference(reference_path):
    """
    Load reference NetCDF of spatial means.

    Returns:
        xr.DataArray
    """
    if not os.path.exists(reference_path):
        raise FileNotFoundError(f"No reference file found at {reference_path}")
    return xr.open_dataarray(reference_path)


def compare_to_reference(spatial_means, reference_da, tol=1e-6):
    """
    Compare newly calculated spatial means to reference.

    Args:
        spatial_means (list of xr.DataArray): Newly calculated results
        reference_da (xr.DataArray): Loaded reference DataArray
        tol (float): Absolute tolerance for comparison

    Returns:
        bool: True if all datasets match within tolerance
    """
    combined = xr.concat(spatial_means, dim='dataset')
    combined = combined.assign_coords(dataset=[f'dataset_{i}' for i in range(len(spatial_means))])

    # Compare
    comparison = np.allclose(combined.values, reference_da.values, atol=tol)
    if comparison:
        print("All datasets match the reference. ✅")
    else:
        print("Some datasets deviate from reference! ⚠️")
        # Optionally, report which dataset(s) differ
        for i in range(len(spatial_means)):
            if not np.allclose(combined.isel(dataset=i).values,
                               reference_da.isel(dataset=i).values, atol=tol):
                print(f"- Dataset {i} differs from reference")
    return comparison
