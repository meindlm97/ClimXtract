# ch2025_download.py
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Maximilian Meindl, University of Vienna
"""

import re
import os
import xarray as xr
import urllib.request
from pystac_client import Client
from .dictionary import dictionary


def find_matching_urls(variable, gwl, model_global, model_regional):
    """
    """
    # Convert GWL numeric to label
    gwl_label = None
    if isinstance(gwl, (int, float)):
        gwl_label = f"gwl{gwl:.1f}".replace(".", "_").replace("_", ".")
    elif isinstance(gwl, str):
        gwl_label = gwl.lower()

    # Strict variable matching pattern
    variable = variable.lower()
    variable_pattern = re.compile(rf"_({variable})_", re.IGNORECASE)

    # Open CH2025 catalog
    catalog = Client.open("https://data.geo.admin.ch/api/stac/v1/")
    collection = catalog.get_collection(
        "ch.meteoschweiz.ogd-climate-scenarios-ch2025-grid"
    )

    # Collect all assets
    all_assets = {}
    for item in collection.get_items():
        all_assets |= item.assets

    # Filter matching assets
    matches = []

    for key, asset in all_assets.items():

        key_low = key.lower()

        # Strict variable match
        if not variable_pattern.search(key_low):
            continue

        if variable == "tas" and ("tasmin" in key_low or "tasmax" in key_low):
            continue

        # Filter GWL or ref
        if gwl_label:
            if gwl_label not in key_low:
                continue

        # Extract model string: "..._tas_smhi-rca-mpiesm_gwl3.0.nc"
        m = re.search(r"_(.*?)_(gwl|ref)", key_low)
        if not m:
            continue

        model_str = m.group(1)
        parts = model_str.split("-")

        if len(parts) < 3:
            continue

        inst = parts[0]
        rcm = parts[1]
        gcm = "-".join(parts[2:])

        # Filter by model_global
        if model_global:
            if model_global.lower() not in gcm:
                continue

        # Filter by model_regional
        if model_regional:
            if model_regional.lower() not in f"{inst}-{rcm}":
                continue

        matches.append((key, asset.href))

    if len(matches) == 0:
        print("No matching CH2025 data found for your criteria.")
        return None, None, None

    asset_key, href = matches[0]

    return asset_key, href


def load_ch2025(model_global, model_regional, variable, experiment, output_path):
    """
    Download CH2025 daily gridded dataset filtered by variable, global warming level
    
        Input:
            model_global         string      name of the global climate model
            model_regional       string      name of the regional model
            variable             string      variable name (tass, tasmin, tasmax, pr)
            experiment           string      global warming level (1.5, 2.0, 2.5, 3.0, ref91-20)
            ens                  string      name of ensemble member
            output_path          string      path where netCDF file is stored
            
        Output:
            Returns the path of the netCDF file containing the CH2025 data.
    """
    # Validate variable
    if variable not in dictionary:
        raise ValueError(f"Variable must be one of {list(dictionary.keys())}")

    ch2025_info = dictionary[variable]['ch2025']
    variable_long = ch2025_info['name']
    #standard_key = next(iter(dictionary[variable]))
    #standard_unit = dictionary[variable][standard_key]['units']
    
    # Define filename
    file = (
        f"{variable}_{model_global}_{experiment}_"
        f"{model_regional}.nc"
    )

    output_file = os.path.join(output_path, file)
    
    # Check whether the file already exists and return the path of the file
    if os.path.exists(output_file):
        print("Loaded CH2025 data successfully.")
        return output_file

    else:
        # Download CH2025 data
        try:
            #
            asset_key, href = find_matching_urls(variable, experiment, model_global, model_regional)
            print("Downloading:", asset_key)
            
            # Download the file using urllib
            urllib.request.urlretrieve(href, output_file)
            print("Downloaded CH2025 data successfully.")
            
        except Exception as e:
            print(f"Failed to download CH2025 data.\nError: {e}")

        return output_file