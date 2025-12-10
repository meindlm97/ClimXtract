# spartacus_download.py
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Maximilian Meindl, University of Vienna
"""

import os
import shutil
import wget
import xarray as xr
from cdo import Cdo
from importlib.resources import files
from .dictionary import dictionary


def download_yearly_files(dataset, year, output_path):
    """
    Download daily SPARTACUS v2.1 data on a yearly basis
    from the Geosphere Austria Datahub.

        Input:
            dataset    str      type of the dataset (e.g tn)
            year       int      year to be downloaded (e.g 1971)

        Output:
            Returns the temporary output path, where the yearly downloaded
            files are saved.
    """
    # Putting together the download link (url)
    base_url = (
        "https://public.hub.geosphere.at/datahub/resources/"
        "spartacus-v2-1d-1km/filelisting"
    )

    url_directory = f"{base_url}/{dataset.upper()}/"
    file = f"SPARTACUS2-DAILY_{dataset.upper()}_{year}.nc"

    # Construct the full URL
    url = f"{url_directory}{file}"

    # Define temporary directory
    temp_dir = os.path.join(output_path, "tmp")

    # Ensure the temporary directory exsists
    os.makedirs(temp_dir, exist_ok=True)

    # Define filname for temporal output
    temp_file = os.path.join(temp_dir, file)

    # Download the file using the wget package
    wget.download(url, out=temp_file)

    return temp_file


def load_spartacus(variable, start, end, output_path):
    """
    Function that calls download_yearly_files to download SPARTACUS data.
    The individual downloaded years are merged into one file.
    The temperature is calculated as the mean of daily maximum and
    minimum temperature.

        Input:
            variable          str      variable name (e.g. tas)
            start             str      start year (e.g. 1961)
            end               str      end year (e.g. 2024)
            output_path       str      path where netCDF file is stored

        Output:
            Returns the path of the netCDF file containing the SPARTACUS data.
    """
    # Validate variable
    if variable not in dictionary:
        raise ValueError(f"Variable must be one of {list(dictionary.keys())}")

    spartacus_info = dictionary[variable]['spartacus']
    variable_long = spartacus_info['name']
    standard_key = next(iter(dictionary[variable]))
    standard_unit = dictionary[variable][standard_key]['units']

    # Define filename
    tmp_file = (
        f"{variable}_spartacusv2.1_"
        f"{start}-{end}_tmp.nc"
    )

    file = (
        f"{variable}_spartacusv2.1_"
        f"{start}-{end}.nc"
    )

    tmp_file = os.path.join(output_path, tmp_file)
    output_file = os.path.join(output_path, file)

    # Check whether the file already exists and return the path of the file
    if os.path.exists(output_file):
        print("Loaded SPARTACUS data successfully.")
        return output_file

    else:

        try:
            # Initialize list to hold data arrays
            data_list = []

            # Loop through years and download data
            for year in range(int(start), int(end) + 1):
                if variable == 'tas':
                    # Download tn and tx datasets
                    tasmin_path = download_yearly_files('tn', year, output_path)
                    tasmax_path = download_yearly_files('tx', year, output_path)

                    # Load the datasets
                    tasmin = xr.open_dataset(tasmin_path)
                    tasmax = xr.open_dataset(tasmax_path)

                    # Append the data arrays to the list
                    data_list.append((tasmin['TN'] + tasmax['TX']) / 2)

                elif variable == 'pr':
                    # Download rr dataset
                    rr_path = download_yearly_files('rr', year, output_path)

                    # Load the dataset
                    rr = xr.open_dataset(rr_path)

                    # Appaned the data arrays to the list
                    data_list.append(rr['RR'])

            # Concatenate all years together along the time dimension
            dataset = xr.concat(data_list, dim='time')

            # Standardize variable and units for temperature
            if variable == 'tas':
                dataset.name = variable
                units = dataset.attrs.get("units", None)
                if units is None or units not in standard_unit:
                    dataset.attrs['units'] = standard_unit

            # Standardize varibale and units for precipitation
            if variable == 'pr':
                dataset.allname = variable
                units = dataset.attrs.get("units", None)
                if units is None or units not in standard_unit:
                    dataset.attrs['units'] = standard_unit

            # Save dataset to netCDF file
            dataset.to_netcdf(tmp_file)
            print("Downloaded SPARTACUS data successfully.")

            # If cdo is not in the path, add it manually
            conda_bin = os.path.expanduser('~/.conda/envs/climxtract/bin')
            os.environ['PATH'] += f':{conda_bin}'

            # Initialize the Cdo object
            cdo = Cdo()

            # Dynamically get the file path to spartacus_grid.txt inside the package
            spartacus_grid_path = files('climxtract').joinpath('spartacus_grid.txt')

            # Set spartacus grid for conservative regridding
            cdo.setgrid(str(spartacus_grid_path), input=tmp_file, output=output_file)

        except Exception as e:
            print(f"Failed to download SPARTACUS data.\nError: {e}")
            return None

        # Clean temporary directory
        shutil.rmtree(os.path.join(output_path, "tmp"))

        # Remove tmp_file with old grid
        os.remove(tmp_file)

        return output_file
