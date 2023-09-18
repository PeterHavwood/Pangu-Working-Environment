import os
import numpy as np
import netCDF4 as nc

def npy2nc_upper(upper_npy, file_TIME, ncfile_name, save_path):
    # Create the new nc file
    upper_nc = nc.Dataset(os.path.join(save_path,ncfile_name), 'w', format='NETCDF4')

    # Define the dimensions
    upper_nc.createDimension('latitude', size=721)
    upper_nc.createDimension('longitude', size=1440)
    upper_nc.createDimension('level', size=13)
    upper_nc.createDimension('time', size=1)

    # Define the variables
    upper_nc.createVariable('latitude', 'f4', dimensions='latitude')
    upper_nc.createVariable('longitude', 'f4', dimensions='longitude')
    upper_nc.createVariable('level', 'i4', dimensions='level')
    upper_nc.createVariable('time', 'i4', dimensions='time')
    upper_nc.createVariable('z', 'f4', dimensions=('time', 'level', 'latitude', 'longitude'))
    upper_nc.createVariable('q', 'f4', dimensions=('time', 'level', 'latitude', 'longitude'))
    upper_nc.createVariable('t', 'f4', dimensions=('time', 'level', 'latitude', 'longitude'))
    upper_nc.createVariable('u', 'f4', dimensions=('time', 'level', 'latitude', 'longitude'))
    upper_nc.createVariable('v', 'f4', dimensions=('time', 'level', 'latitude', 'longitude'))

    # Add data to variables
    upper_nc.variables['longitude'][:]  = np.linspace(0, 359.75, 1440)
    upper_nc.variables['latitude'][:]  = np.linspace(90, -90, 721)
    upper_nc.variables['level'][:]  = np.array([1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50])
    upper_nc.variables['time'][:] = file_TIME
    upper_nc.variables['time'].units = "hours since 1900-01-01 00:00:00.0"
    upper_nc.variables['z'][:]  = upper_npy[0]
    upper_nc.variables['q'][:]  = upper_npy[1]
    upper_nc.variables['t'][:]  = upper_npy[2]
    upper_nc.variables['u'][:]  = upper_npy[3]
    upper_nc.variables['v'][:]  = upper_npy[4]

    upper_nc.close()

def npy2nc_surface(surface_npy, file_TIME, ncfile_name, save_path):
    # Create the new nc file
    surface_nc = nc.Dataset(os.path.join(save_path,ncfile_name), 'w', format='NETCDF4')

    # Define the dimensions
    surface_nc.createDimension('latitude', size=721)
    surface_nc.createDimension('longitude', size=1440)
    surface_nc.createDimension('time', size=1)

    # Define the variables
    surface_nc.createVariable('latitude', 'f4', dimensions='latitude')
    surface_nc.createVariable('longitude', 'f4', dimensions='longitude')
    surface_nc.createVariable('time', 'i4', dimensions='time')
    surface_nc.createVariable('msl', 'f4', dimensions=('time', 'latitude', 'longitude'))
    surface_nc.createVariable('u10', 'f4', dimensions=('time', 'latitude', 'longitude'))
    surface_nc.createVariable('v10', 'f4', dimensions=('time', 'latitude', 'longitude'))
    surface_nc.createVariable('t2m', 'f4', dimensions=('time', 'latitude', 'longitude'))

    # Add data to variables
    surface_nc.variables['longitude'][:] = np.arange(0,360,0.25)
    surface_nc.variables['latitude'][:] = np.linspace(90, -90, 721)
    surface_nc.variables['time'][:] = file_TIME
    surface_nc.variables['time'].units = "hours since 1900-01-01 00:00:00.0"
    surface_nc.variables['msl'][:] = surface_npy[0]
    surface_nc.variables['u10'][:] = surface_npy[1]
    surface_nc.variables['v10'][:] = surface_npy[2]
    surface_nc.variables['t2m'][:] = surface_npy[3]
    
    surface_nc.close()