# ClimXtract: A Python Toolkit for Standardizing High-Resolution Climate Datasets on Regional Domains

ClimXtract provides a modular pipeline for preparing high-resolution climate datasets for regional analysis. Its three capabilities are **downloading**, **regridding**, and **masking**, all designed to support interoperability and reproducability. Although the toolkit is designed with Austria and ÖKS15 in mind, all components can be configured to work with any user-defined target grid.

ClimXtract was developed as part of the Austrian Climate Research Programme (ACRP) project **HighResLearn**. One goal of HighResLearn is to enable the Austrian climate community to effictiently access and process high-resolution global climate model data in conjunction with national-scale reference datasets like ÖKS15. As such, the ClimXtract toolkit lays the foundation for downstream applications, including machine learrning based analysis of climate model performance on regional scales.

## Repository structure

The repository is organized as follows:

- **climxtract** contains the actual source code. ```__init__.py``` is acting as the control center. The individual download functions can be called here, whereby each function returns a tuple containing both the path of the downloaded file (as string) and an xarray object. The regridding function (```regrid.py```) requires the path of the target-grid, as well as the path of the input file to be regridded. The masking function (```mask.py```) requires again the path of the target-grid and the path of the previously regridded file. Note that all functions can also be used independently of each other.
- **example_data**: Sample datasets for testing.
- **example_data_processed**: Output data generated from [test script](https://github.com/meindlm97/ClimXtract/blob/main/tests/test.py).
- **example_notebooks** contains example notebooks that illustrate the use of climxtract (for processing temperature and preciptation data). These notebooks can be adapted by the needs of the user, but provide the general procedure for regridding und masking the data as well as some plotting routines to make a first visual comparison between the different datasets.
- **tests**: Include reference test to validate functionality of the code.

**⚠️Note:** Depending on the timeperiod and therefore the size of the data to be processed, the use of the package within a Jupyter notebook for processing large amounts of data is not recommended.

## Availability and installation

Climxtract is hosted on Github and is also available from pypi.

It can be installed via pip:

```pip install climxtract```

To run the code and also the example books you can use the environment.yml file provided to create a conda environment that can run the code. The following commands create the environment and also create an ipykernel called climxtract that can be used in Jupyter notebooks if selected.

```
# create conda environment named 'climxtract'
conda create -n climxtract -c conda-forge -y python=3.10

# update the environment using specifications in environment.yml
conda env update -n climxtract -f environment.yml

# activate the 'climxtract' 
conda activate climxtract

# set climxtract environment to the default used by ipykernels
python3 -m ipykernel install --user --name=climxtract
```

## Running a test using sample data

Below we provide step-by-step instruction on how to install the software in order to run a test using the provided sample data.

1. Clone or download the repository
```
git clone https://github.com/meindlm97/ClimXtract.git
cd ClimXtract
```

2. Set up Python environment
```
conda create -n climxtract -c conda-forge -y python=3.10
conda env update -n climxtract -f environment.yml
conda activate climxtract
```

3. Verify the installation: Inside the environment run python and import the package
```
python
import climxtract
exit()
```

4. Run a test with sample data: The repository contains example data and scripts in the [test folder](https://github.com/meindlm97/ClimXtract/tree/main/tests). To run the reference test:
```
cd tests
python reference.py
```

## Introduction

As the demand for high-resolution climate data has increased rapidly in recent years, so too has its availability. The sources of high-resolution data are manifold and include observations, reanalyses, as well as simulations with regional and global models. This can make working with these datasets technically challenging, as they use different file formats, spatial resolutions, coordinate systems, variable naming conventions, and physical units.

ClimXtract simplifies access to km-scale climate data by bridging global and regional data sources and adresses the technical challenges mentioned above by providing an easy-to-use and customizable solution that:

  - unifies access to observational, model, and reanalysis data,
  - remaps diverse spatial grids to a consistent, high-resolution target grid,
  - resolves inconsistencies in variable naming, units, and metadata, and
  - supports a reproducible and modular workflow.

## Overview

ClimXtract includes dedicated download functions to access and retrieve data from seven major climate datasets relevant for the Austrian domain:

| Name               | Category        | Spatial res. | Temporal res. | Domain        |
|--------------------|-----------------|--------------|---------------|---------------|
| ÖKS15              | Model           | 1 km         | daily         | Austria       |
| SPARTACUS          | Observational   | 1 km         | daily         | Austria       |
| EURO-CORDEX        | Model           | 12.5 km      | daily         | Europe        |
| E-OBS              | Observational   | 11 km        | daily         | Europe        |
| DestinE Climate DT | Model           | 5 km         | hourly        | Global        |
| ERA5               | Reanalysis      | 30 km        | hourly/daily  | Global        |
| ERA5-Land          | Reanalysis      | 9 km         | hourly/daily  | Global (Land) |

*Table 1: Selection of datasets to be used in this data recipes, inlcuding the axpproximate resolution and covered domain.*

## Accessing datasets and variables

**⚠️Note**: DestinE Climate DT and ERA5(-Land) data are only available after registration via the respective platforms, while all other datasets are freely accessible. 

### ÖKS15

To analyze regional climate change in Austria the latest generation of regional climate models can be used. As part of the European branch of the Regional Downscaling Experiment (EURO-CORDEX), 13 regional climate simulations are available for the greenhouse gas scenarios RCP4.5 and RCP8.5.


| Nr. | Global Model                   | Regional Model          |
| --- | ------------------------------ | ----------------------- |
| 1   | CNRM-CERFACS-CNRM-CM5          | CLMcom-CCLM4-8-17       |
| 2   | CNRM-CERFACS-CNRM-CM5          | CNRM-ALADIN53           |
| 3   | CNRM-CERFACS-CNRM-CM5          | SMHI-RCA4               |
| 4   | ICHEC-EC-EARTH                 | CLMcom-CCLM4-8-17       |
| 5   | ICHEC-EC-EARTH                 | SMHI-RCA4               |
| 6   | ICHEC-EC-EARTH                 | KNMI-RACMO22E           |
| 7   | ICHEC-EC-EARTH                 | DMI-HIRHAM5             |
| 8   | IPSL-IPSL-CM5A-MR              | IPSL-INERIS-WRF331F     |
| 9   | IPSL-IPSL-CM5A-MR              | SMHI-RCA4               |
| 10  | MOHC-HadGEM2-ES                | CLMcom-CCLM4-8-17       |
| 11  | MOHC-HadGEM2-ES                | SMHI-RCA4               |
| 12  | MPI-M-MPI-ESM-LR               | CLMcom-CCLM4-8-17       |
| 13  | MPI-M-MPI-ESM-LR               | SMHI-RCA4               |

*Table 3: Combination of global (GCMs) and regional models (RCMs) from EURO-CORDEX used by ÖKS15.*

Data is available at the  [Datahub of Geosphere Austria](https://data.hub.geosphere.at/dataset/oks15_bias_corrected) and can be downloaded either via a HTTP file list or via the THREDDS Data Server (TDS). In addition to daily mean near-surface temperature (tas) and daily precipitation (pr), the daily minimum (tasmin) and maximum temperature (tasmax) as well as solar shortwave radiation (rsds) are available. Each dataset spans the timperiod 1951-2100.

In ÖKS15, the data of the RCMs from the EURO-CORDEX initiative (12.5 km) is interpolated to the grid of the observations (1 km), whereby the transition to the fine high-resolution grid (1 km) is accomplished using [statistical methods](https://hess.copernicus.org/articles/21/2649/2017/hess-21-2649-2017-discussion.html).

### SPARTACUS

The gridded dataset describes the spatial distribution of observed air temperature (minimum temperature TN and maximum temperature TX), precipitation (RR) and absolute sunshine duration (SA) on a daily basis since 1961 in a horizontal resolution of 1 km over Austria. 

The dataset is available for download on the [Datahub of Geosphere Austria](https://data.hub.geosphere.at/dataset/spartacus-v2-1d-1km) and can be obtained in different ways (spatial subset download, filearchive, API).

A gridded data set of the daily mean temperature is calculated by averaging the available temperature datasets of daily minimum and daily maximum temperatures. This leads to a continuous dataset for the daily mean temperature from 1961-present over Austria and will be used in the course of the project especially for the evaluation of climate model data for the Austrian domain.

### EURO-CORDEX

[CORDEX](https://cordex.org/) (Coordinated Regional Climate Downscaling Experiment) is a global initiative led by the [World Climate Research Program](https://www.wcrp-climate.org/) (WCRP). Its goal is to improve regional climate projections by downscaling global climate models (GCMs) to higher resolutions, whereby EURO-CORDEX is the European branch of this initiative, focusing specifically on the European region.

The data is available either via [ESGF (Earth System Grid Federation system)](https://esgf-metagrid.cloud.dkrz.de/search) or via the [Copernius Climate Data Store](https://cds.climate.copernicus.eu/datasets/projections-cordex-domains-single-levels?tab=overview).

Within these data recipes, CORDEX data is accessed via a special Python interface. The [ESGF PyClient](https://esgf-pyclient.readthedocs.io/en/latest/index.html) is a Python package designed for interacting with the ESGF system. This tool can be used to find the corresponding download links. The Python package [wget](https://pypi.org/project/wget/) is then used to download the files for further processing.

EURO-CORDEX provides a wide range of meteorological and climatological variables, including daily mean, max, min temperatures, precipitation rate, longwave and shortwave radiation and many others. Additionaly, the simulations are onducted at two different spatial resolutions, the general CORDEX resolution of 0.44 degree (EUR-44, ~50 km) and additionally the finer resolution of 0.11 degree (EUR-11, ~12.5km).

As for ÖKS15, there are also simulations for different climate scenarios available:

- Historical (1950-2005)
- Future Scenarios (2006–2100, from CMIP5)
    - RCP2.6 (Low emissions)
    - RCP4.5 (Medium emissions)
    - RCP8.5 (High emissions)

### E-OBS

E-OBS is a daily gridded observational dataset that provides comprehensive information on various meteorological variables across Europe. It includes data on precipitation, temperature (mean, minimum, and maximum), sea level pressure, global radiation, wind speed, and relative humidity. The dataset spans from January 1950 to the present.

To access and download the E-OBS dataset, visit the official [data access page](https://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php?utm_source=chatgpt.com). The data is available in NETCDF-4 format on regular latitude-longitude grids with spatial resolutions of 0.1° x 0.1° and 0.25° x 0.25°.

### Destination Earth

Destination Earth is a flagship initiative of the European Commission to develop a highly-accurate digital model of the Earth (a digital twin of the Earth) to model, monitor and simulate natural phenomena, hazards and the related human activities. This initiative presents the first ever attempt to operationalise the production of global multi-decadal climate projections at km-scale resolutions of 5 to 10km. To access the datasets from the [Earth Data Hub](https://earthdatahub.destine.eu/) you need to register on the [Destination Earth Platform](https://platform.destine.eu/). In order to get full access to the data, one has to [upgrade the access](https://platform.destine.eu/access-policy-upgrade/) by selecting the appropriate user category (e.g Academia & research). Your request will reviewed and you will be notified on the acceptance.

**⚠️Note**: 
- Data is provided on a hierachical [HEALPix](https://healpix.sourceforge.io/) grid for both models (ICON & IFS-FESOM/IFS-NEMO). 
- Data is provided on various levtype values, for different parameters: 2 metre temperature has the parameter 167, Total precipitation rate has the parameter 260048.

The easiest way to access the Destination Earth DT data is via the [Polytope web service](https://github.com/destination-earth-digital-twins/polytope-examples/tree/main) hosted on the LUMI databride.

1. The polytope-client can be installed from PyPI:

```pip install --upgrade polytope-client```

2. Retrieve a token from the Destination Earth Service Platform (DESP) by running the script included in the repository:

```python desp-authentication.py```

You will then be prompted to enter your username and password which were set during the registration process.

You will also nedd some dependencies to run the script, which can be installed using pip:

```pip install --upgrade lxml conflator```

The script automatically places your token in ```~/.polytopeapirc``` where the client will pick it up. The token is a long-lived ("offline_access") token.

### ERA5

ERA5 is the fifth generation ECMWF reanalysis for the global climate and weather for the past 8 decades. It spans atmospheric, land and ocean variables and includes hourly data with global coverage at 30 km resolution.

Data is avaiable at the [Copernius Climate Data Store](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview) and can be downloaded via the [CDS API](https://cds.climate.copernicus.eu/how-to-api). In addition, [ERA5-Land](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=overview) hourly data from 1950 to present is also available at a resolution of 9 km. 

In oder to use the CDS API, the CDS API personal access token has to be setup:
1. If you do not have an account yet, please [register](https://accounts.ecmwf.int/auth/realms/ecmwf/login-actions/registration?execution=c4f93b9c-f4e7-40e7-a6d4-94fb59e7a5e6&client_id=cds&tab_id=KEZjPuIIXiQ).
2. If you are not logged in, please [login](https://accounts.ecmwf.int/auth/realms/ecmwf/protocol/openid-connect/auth?client_id=cds&scope=openid%20email&response_type=code&redirect_uri=https%3A%2F%2Fcds.climate.copernicus.eu%2Fapi%2Fauth%2Fcallback%2Fkeycloak&state=HLLwusl7uPsbQsnaNS-Io99y_x6i7UXOJKreQvpjbAA&code_challenge=HHjm_PSoGrq-0l8Fpyi9gSYIC9WHRe1AQL2q59Wpbx0&code_challenge_method=S256).
3. Once logged in, copy the url and the key displayed to the file `$HOME/.cdsapirc`

## Variables and naming convention

In particular, for the purpose of the project, we are interested in temperature and precipitation, whereby other atmospheric variables can also be considered depending on the needs of the community. The datasets used have different naming conventions for the variables mentioned before. These deviating variable names and their units are addressed and resolved in the recipes provided by a standardized adaption to the ÖKS15 format:

| Variable      | ÖKS15        | SPARTACUS                             |
|---------------|--------------|---------------------------------------|
| Temperature   | tas [°C]     | (TN+TX)/2 [°C]                        |      
| Precipitation | pr  [kg m-2] | daily precipitation sum (RR) [kg m-2] |  

| Variable      | EURO-CORDEX                           | E-OBS                              |
|---------------|---------------------------------------|------------------------------------|
| Temperature   | 2m_air_temperature (tas) [K]          | daily mean temperature (tg) [°C]   |
| Precipitation | precipitation flux (pr) [kg m-2 s-1]  | daily precipitation sum (rr) [mm]  |

| Variable      | DestinE Climate DT                             | ERA5-(Land)                    |
|---------------|----------------------------------------------- |--------------------------------|
| Temperature   | 2 metre temperature (t2m) [K]                  | 2m_temperature (t2m) [K]       |
| Precipitation | Total precipitation rate (tprate) [kg m-2 s-1] | total precipitation (tp) [m/h] |

*Table 2: Variable names and units of the used datasets.*

**⚠️Note**: Hourly data is generally available for ERA5(-Land) and DestinE Climate DT data.

Generally, to convert temperature data from Kelvin (K) to degrees Celsius (°C), we use the formula:

$tas_{\text{[°C]}} = tas_{\text{K}} - 273.15$

To convert [hourly ERA5](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview) total precipitation data from meters (m) into daily total precipitation in millimeters (mm):

$pr_{\text{d[mm]}} = (Σ_{h=1}^{23} pr_{d,h[m]} + pr_{d+1,00UTC[m]}) \times 1000$

where h is the hour and d the day of interest (d+1 is the following day). The total precipitation over 24 hours is the sum of the individual total precipiation values for each hour.

To convert [daily ERA5](https://cds.climate.copernicus.eu/datasets/derived-era5-single-levels-daily-statistics?tab=overview) total precipitation data from meters (m) into daily total precipitation in millimeters (mm):

$pr_{\text{d[mm]}} =  pr_{d[m]} \times 1000$

To convert [hourly ERA5-Land](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=overview) total precipitation data from meters (m) into daily total precipitation in millimeters (mm):

$pr_{\text{d[mm]}} = pr_{\text{d+1,00UTC[m]}} \times 1000$

where d is the day for which the total precipitation is being computed. This time step should be taken because it contains the accumulated precipitation over the previous 24 hours.

**⚠️Note**: More information on the [conversion for accumulated variables](https://confluence.ecmwf.int/pages/viewpage.action?pageId=197702790).

To convert a precipiation flux respectively a precipitation rate, as provided by EURO-CORDEX and DestinE Climate DT, into daily precipitation, we are following these steps:

**1. Unterstand the units:**
- Precipitation flux is given in kg per square meter per second [kg m-2 s-1].
- Daily precipitation is required in kg per square meter per day [kg m-2 d-1].
- Since 1 mm precipitation = 1 kg m-2, daily precipitation in kg m-2 is numerically the same as daily precipitation in mm. 

**2. Convert seconds to a day:** 
There are 86.400 seconds in a day (24 hours x 60 minutes x 60 seconds).

**3. Perform the conversion:**
$pr_{\text{d[mm]}} = pr_{\text{flux}} \times 86400$

## Interpolation of climatological data (Regridding)

Climate datasets from difference sources typically come on different horizontal grids (regular lat-lon, rotated pole, Lambert conformal, HEALPix, etc.). ClimXtract offers automated regridding  to a user-defined target grid, making it easy to harmonize inputs for multi-source analysis. To interpolate data from an existing horizontal field to a finer or coarser grid or another grid type, [CDO](https://code.mpimet.mpg.de/projects/cdo) provides a set of interpolation operators. Within ClimXtract we are offering four different methods for regridding climatological datasets:

- nearest neighbor: `remapnn`
- distance: `remapdis`
- conservative: `remapcon`
- bilinear: `remapbil`

The interpolation methods are implemented using the **CDO command-line interface** wrapped in Python. Note that this wrapper does not include the `CDO` binary itself, which must be installed separately and made available in the system environment (i.e., accessible via the system PATH). In our setup, `CDO` version 2.5.0 was installed within a conda environment. However, the wrapper is compatible with any exisitng `CDO` installation. Users specify source and target grids and can switch between interpolation methods by means of the keywords `depending on the variable and use case.

There is no one-size-fits-all interpolation method. The best approach depends on your specific dataset and objectives. Always carefully consider the characteristics of your variable, especially for discontinuous fields like precipitation. In the following, we briefly outline the properties and advantages of the interpolation methods provided:

**Nearest neighbour regridding:** 
- takes the value of the nearest grid cell of the source grid and writes it into the target grid cell
- can be used for unstructured grids (like HEALPix grid)
- simple method that works most of the time, even when other methods do not

**Distance weighted regridding:**
- inverse distance weighted average remapping of the four (default number, can be changed) nearest neighbour values
- smoother grid, gradients less steep than with nearest neighbour
- no need to provide source grid cell corner coordinates

**Conservative regridding**:
- ensures that a conserved quantity (e.g. mass, energy) is preserved during interpolation
- uses weighted averaging based on overlapping areas of source and target grids
- need to provide source grid cell corner coordiantes

**Bilinear regridding:**
- weighted average of the four nearest grid points in a 2D grid
- smooth interpolation producing continous results
- can introduce discontinuities at cell boundaries

## Process to apply a spatial domain mask (Masking)

After regridding, ClimXtract offers a masking functionality to apply a spatial domain mask from any target dataset. This ensures spatial consistency accross datasets, removes unwanted edge regions, and aligns the data with the target analysis domain (e.g., Austria). In our [example notebooks](https://github.com/meindlm97/ClimXtract/tree/main/example_notebooks), masking is again based on the ÖKS15 grid, which defines the Austrian domain by means of NaN values outside of Austria. The masking step is implemented using `xarray.where`, making it efficient and compatible with NetCDF workflows.

## Authors
Climxtract has been developed by:

- Maximilian Meindl (University of Vienna, Austria)
- Luiza Sabchuk (University of Vienna, Austria)
- Aiko Voigt (University of Vienna, Austria)

## Acknowledgemnts

Climxtract uses a couple of other python libraries, and we are very grateful to the communities of developers and maintainers of these libraries. These libraries are:

- cdsapi, https://pypi.org/project/cdsapi/
- ESGF PyClient, https://esgf-pyclient.readthedocs.io/en/latest/index.html
- numpy, https://numpy.org/
- cdo, https://code.mpimet.mpg.de/projects/cdo/wiki/Cdo%7Brbpy%7D 
- polytope-client, https://github.com/ecmwf/polytope-client
- wget, https://pypi.org/project/wget/
- xarray, http://xarray.pydata.org/
