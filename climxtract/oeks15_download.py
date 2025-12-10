# oeks15_download.py
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Maximilian Meindl, University of Vienna
"""

import wget
import os
from .dictionary import dictionary


def load_oeks15(model_global, model_regional, variable,
                experiment, ens, output_path):
    """
    Download ÖKS15 data from the Geosphere Austria Datahub and save as netCDF
    file in the corresponding output path. The complete dataset from 1951-2100
    is downloaded.

        Input:
            model_global         string      name of the global climate model
            model_regional       string      name of the regional model
            variable             string      variable name (e.g. tas)
            experiment           string      climate change scenario
            ens                  string      name of ensemble member
            output_path          string      path where netCDF file is stored

        Output:
            Returns the path of the netCDF file containing the ÖKS15 data.
    """
    # Validate variable
    if variable not in dictionary:
        raise ValueError(f"Variable must be one of {list(dictionary.keys())}")

    oeks15_info = dictionary[variable]['oeks15']
    variable_long = oeks15_info['name']
    #standard_key = next(iter(dictionary[variable]))
    #standard_unit = dictionary[variable][standard_key]['units']

    # Define filename
    file = (
        f"{variable}_SDM_{model_global}_{experiment}_"
        f"{ens}_{model_regional}.nc"
    )

    output_file = os.path.join(output_path, file)

    # Check whether the file already exists and return the path of the file
    if os.path.exists(output_file):
        print("Loaded ÖKS15 data successfully.")
        return output_file

    else:
        # Check version for temperature and maximum temperature
        if variable == 'tas' or variable == 'tx':
            version = '-v02/'

        # Check version for precipitation
        if variable == 'pr':
            version = '-v01/'

        # Download ÖKS15 data
        try:
            # Put together the download link (url)
            base_url = (
                "https://public.hub.geosphere.at/public/resources/oks15/"
                "bias_corrected/oks15_bias_corrected_"
            )

            url_directory = (
                f"{base_url}{variable_long}_{variable}_"
                f"{str.lower(model_global)}_{experiment}_"
                f"{ens}_{str.lower(model_regional)}{version}"
            )

            # Construct the full URL
            url = f"{url_directory}{file}"

            # Download the file using wget
            output_file = wget.download(url, out=output_file)
            print("Downloaded ÖKS15 data successfully.")

        except Exception as e:
            print(f"Failed to download ÖKS15 data.\nError: {e}")
            return None

        return output_file
