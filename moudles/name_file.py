def name_era5_upper_ncfile(TIME):
    ncfile_name = 'era5_upper_'+str(TIME.year).zfill(4)+str(TIME.month).zfill(2)+str(TIME.day).zfill(2)+str(TIME.hour).zfill(2)+'.nc'
    return ncfile_name
def name_era5_surface_ncfile(TIME):
    ncfile_name = 'era5_surface_'+str(TIME.year).zfill(4)+str(TIME.month).zfill(2)+str(TIME.day).zfill(2)+str(TIME.hour).zfill(2)+'.nc'
    return ncfile_name

def name_output_upper_ncfile(TIME, forecast_hour):
    ncfile_name = f'output_{forecast_hour}_upper_'+str(TIME.year).zfill(4)+str(TIME.month).zfill(2)+str(TIME.day).zfill(2)+str(TIME.hour).zfill(2)+'.nc'
    return ncfile_name
def name_output_surface_ncfile(TIME, forecast_hour):
    ncfile_name = f'output_{forecast_hour}_surface_'+str(TIME.year).zfill(4)+str(TIME.month).zfill(2)+str(TIME.day).zfill(2)+str(TIME.hour).zfill(2)+'.nc'
    return ncfile_name