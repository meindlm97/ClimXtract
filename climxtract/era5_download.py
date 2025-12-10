# era5_download.py
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Maximilian Meindl, University of Vienna
"""

import cdsapi
import shutil
import os
import xarray as xr
import numpy as np
from datetime import datetime, timedelta
from .dictionary import dictionary


def load_era5(model_global, variable, start, end, output_path):
    """
    Download ERA5 data from the Copernicus Climate Data Store using the CDS API.

        Input:
            model_global          str          name of the dataset
            variable_long         str          variable name
            start                 str          start date (e.g. 20200901)
            end                   str          end date (e.g. 20200930)
            output_path           str          path where netCDF file is stored

        Output:
            Returns the path of the netCDF file containing the ERA5 data.
    """
    # Validate variable
    if variable not in dictionary:
        raise ValueError(f"Variable must be one of {list(dictionary.keys())}")

    era5_info = dictionary[variable]['era5']
    variable_long = era5_info['name']
    standard_unit = dictionary[variable]['oeks15']['units']

    # Define filename
    file = f"{variable}_{model_global}_{start}-{end}.nc"
    output_file = os.path.join(output_path, file)

    # Check whether the file already exists and return the path of the file
    if os.path.exists(output_file):
        print("Loaded ERA5 data successfully.")
        return output_file

    else:
        # Create temporary directory
        temp_dir = os.path.join(output_path, "tmp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_file = os.path.join(temp_dir, file)

        # Download ERA5 data
        try:
            # Initialize the API client
            client = cdsapi.Client()

            # Convert strings to datetime objects
            start_date = datetime.strptime(start, "%Y%m%d")
            end_date = datetime.strptime(end, "%Y%m%d")

            # Generate list of years, months, and days
            date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

            years = sorted(list(set(date.strftime("%Y") for date in date_range)))
            months = sorted(list(set(date.strftime("%m") for date in date_range)))
            days = sorted(list(set(date.strftime("%d") for date in date_range)))

            dataset = model_global
            request = {
                "product_type": ["reanalysis"],
                "variable": variable_long,
                "year": years,
                "month": months,
                "day": days,
                "area": [80, -50, 20, 75],
                "data_format": "netcdf",
            }

            # Daily statistic products
            if model_global in [
                "derived-era5-single-levels-daily-statistics",
                "derived-era5-land-daily-statistics",
            ]:

                # Use daily mean for temperature
                if variable == 'tas':
                    request.update({
                        "daily_statistic": "daily_mean",
                        "time_zone": "utc+00:00",
                        "frequency": "1_hourly",
                    })

                # Use daily_sum for precipitation, daily_mean for temperature
                if variable == 'pr' and model_global == "derived-era5-single-levels-daily-statistics":
                    request.update({
                        "daily_statistic": "daily_sum",
                        "time_zone": "utc+00:00",
                        "frequency": "1_hourly",
                    })

            # ERA5-Land total precipitation
            elif variable == 'pr' and model_global == 'reanalysis-era5-land':
                request["time"] = ["00:00"]
                request["download_format"] = ["unarchived"]

            client.retrieve(dataset, request, temp_file)
            print("Downloaded ERA5 data successfully.")

        except Exception as e:
            print(f"Failed to download ERA5 data.\nError: {e}")
            return None

        # Open previously downloaded dataset
        dataset = xr.open_dataset(temp_file)

        # Standardize ERA5 and ERA5-Land temperature
        if variable == 'tas':

            # Rename the variable and time coordinate
            dataset = dataset.rename({'t2m': variable, 'valid_time': 'time'})

            # Convert from kelvin to celsius
            dataset[variable] = dataset[variable] - 273.15
            units = dataset[variable].attrs.get("units", None)
            if units is None or units not in standard_unit:
                print(f"Warning: {variable} has no or wrong unit attribute.")
                dataset[variable].attrs['units'] = standard_unit
                print(f"Note: Unit attribute of {variable} changed to {standard_unit}.")

            # Write dataset to netCDF file
            dataset.to_netcdf(output_file)

        # Standardize ERA5 precipitation
        if variable == 'pr' and model_global == 'derived-era5-single-levels-daily-statistics':

            # Rename the variable and time coordiante
            dataset = dataset.rename({'tp': variable,  'valid_time': 'time'})

            # Convert from m to mm
            dataset[variable] = dataset[variable]*1000
            units = dataset[variable].attrs.get("units", None)
            if units is None or units not in standard_unit:
                print(f"Warning: {variable} has no or wrong unit attribute.")
                dataset[variable].attrs['units'] = standard_unit
                print(f"Note: Unit attribute of {variable} changed to {standard_unit}.")

            # Write dataset to netCDF file
            dataset.to_netcdf(output_file)

        # Standardize ERA5-Land precipitation
        if variable == 'pr' and model_global == 'reanalysis-era5-land':

            # Rename the variable and time coordinate
            dataset = dataset.rename({'tp': variable, 'valid_time': 'time'})

            # Assign the precipitation to the previous day explicitly:
            dataset = dataset.assign_coords(
                time=(dataset.time - np.timedelta64(1, 'D'))
            )

            # Convert from meters to millimeters
            dataset[variable] = dataset[variable]*1000
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
