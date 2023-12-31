import cdsapi
import numpy as np
import os
from netCDF4 import Dataset
from moudles.name_file import name_era5_upper_ncfile, name_era5_surface_ncfile

def get_input_npy(input_TIME, save_path):
    input_upper_ncfile_name = get_hourly_upper_npy(input_TIME, save_path)
    input_surface_ncfile_name = get_hourly_surface_npy(input_TIME, save_path)
    return input_upper_ncfile_name, input_surface_ncfile_name

def get_hourly_upper_npy(TIME, save_path):
    # Download nc file
    ncfile_name = name_era5_upper_ncfile(TIME)
    ncfile = os.path.join(save_path, ncfile_name)
    if os.path.isfile(ncfile):
        print("The input upper netCDF data already exists. No need to download.")
    else:
        print("Downloading the input upper netCDF data:")
        download_hourly_upper_nc(TIME, save_path)
    
    # Get variables in nc file
    upper_data = Dataset(ncfile)
    z = upper_data.variables['z']
    q = upper_data.variables['q']
    t = upper_data.variables['t']
    u = upper_data.variables['u']
    v = upper_data.variables['v']

    # Get numpy file
    input_upper = np.concatenate([z,q,t,u,v]).data.astype(np.float32)
    np.save(os.path.join(save_path, 'input_upper.npy'), input_upper)
    
    return ncfile_name

def get_hourly_surface_npy(TIME, save_path):
    # Download nc file
    ncfile_name = name_era5_surface_ncfile(TIME)
    ncfile = os.path.join(save_path, ncfile_name)
    if os.path.isfile(ncfile):
        print("The input surface netCDF data already exists. No need to download.")
    else:
        print("Downloading the input surface netCDF data:")
        download_hourly_surface_nc(TIME, save_path)
    
    # Get variables in nc file
    surface_data = Dataset(ncfile)
    msl = surface_data.variables['msl']
    u10 = surface_data.variables['u10']
    v10 = surface_data.variables['v10']
    t2m = surface_data.variables['t2m']

    # Get numpy file
    input_surface = np.concatenate([msl,u10,v10,t2m]).data.astype(np.float32)
    np.save(os.path.join(save_path, 'input_surface.npy'), input_surface)

    return ncfile_name

def download_hourly_upper_nc(TIME, download_path):
    ncfile_name = name_era5_upper_ncfile(TIME)
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type'  : 'reanalysis',
            'format'        : 'netcdf', 
            'variable'      : ['geopotential', 'specific_humidity', 'temperature',
                               'u_component_of_wind', 'v_component_of_wind',],
            'pressure_level': ['1000', '925', '850', '700', '600', '500', '400', 
                               '300', '250', '200', '150', '100', '50'],
            'year'          : str(TIME.year).zfill(4),
            'month'         : str(TIME.month).zfill(2),
            'day'           : str(TIME.day).zfill(2),
            'time'          : str(TIME.hour).zfill(2) + ':00',
        },
        os.path.join(download_path, ncfile_name)
    )

def download_hourly_surface_nc(TIME, download_path):
    ncfile_name = name_era5_surface_ncfile(TIME)
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type'  : 'reanalysis',
                'format'        : 'netcdf', 
                'variable'      : ['10m_u_component_of_wind', '10m_v_component_of_wind', 
                                   'mean_sea_level_pressure', '2m_temperature'], 
                'year'          : str(TIME.year).zfill(4),
                'month'         : str(TIME.month).zfill(2),
                'day'           : str(TIME.day).zfill(2),
                'time'          : str(TIME.hour).zfill(2) + ':00',
        },
        os.path.join(download_path, ncfile_name)
    )