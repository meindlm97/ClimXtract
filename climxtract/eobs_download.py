# eobs_download.py
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Maximilian Meindl, University of Vienna
"""

import os
import wget
import shutil
import xarray as xr
from .dictionary import dictionary


def load_eobs(variable, start, end, output_path):
    """
    Download daily E-OBS data from European Climate Assessment & Dataset.
    The complete dataset from 1950 onwards is downloaded.

        Input:
            variable       str          variable name (e.g. 2m_temperature)
            start          str          start date (20200101)
            end            str          end date (20201231)
            output_path    str          path where netCDF file is stored

        Output:
            Returns the path of the netCDF file containing the daily E-OBS data.
    """
    # Validate variable
    if variable not in dictionary:
        raise ValueError(f"Variable must be one of {list(dictionary.keys())}")

    eobs_info = dictionary[variable]['eobs']
    variable_long = eobs_info['name']
    standard_key = next(iter(dictionary[variable]))
    standard_unit = dictionary[variable][standard_key]['units']

    # Define output filename
    file = f"{variable}_e-obs31.e_{start}-{end}.nc"
    output_file = os.path.join(output_path, file)

    # Check whether the file already exists and return the path of the file
    if os.path.exists(output_file):
        print("Loaded E-OBS data successfully.")
        return output_file

    else:
        # Create temporary directory
        temp_dir = os.path.join(output_path, "tmp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_file = os.path.join(temp_dir, file)

        # Download E-OBS data
        try:
            base_url = "https://knmi-ecad-assets-prd.s3.amazonaws.com/ensembles/data/"
            url_directory = base_url + "Grid_0.1deg_reg_ensemble/"
            filename = str(variable_long) + "_" + "ens_mean_0.1deg_reg_v30.0e.nc"
            url = url_directory + filename
            wget.download(url, out=temp_file)
            print("Downloaded E-OBS data successfully.")
        except Exception as e:
            print(f"Failed to download E-OBS data.\nError: {e}")
            return None

        # Open previously downloaded dataset
        dataset = xr.open_dataset(temp_file)

        # Select the data range
        dataset = dataset.sel(time=slice(start, end))

        # Standardize variable and units for temperature
        if variable == 'tas':
            dataset = dataset.rename({variable_long: variable})
            units = dataset[variable].attrs.get("units", None)
            if units is None or units not in standard_unit:
                print(f"Warning: {variable} has no or wrong unit attribute.")
                dataset[variable].attrs['units'] = standard_unit
                print(f"Note: Unit attribute of {variable} changed to {standard_unit}.")

        # Standardize variable and units for precipitation
        if variable == 'pr':
            dataset = dataset.rename({variable_long: variable})
            units = dataset[variable].attrs.get("units", None)
            if units is None or units not in standard_unit:
                print(f"Warning: {variable} has no or wrong unit attribute.")
                dataset[variable].attrs['units'] = standard_unit
                print(f"Note: Unit attribute of {variable} changed to {standard_unit}.")

        # Write dataset to netCDF file
        dataset.to_netcdf(output_file)

        # Clean temporary directory
        shutil.rmtree(temp_dir)

        return output_file
