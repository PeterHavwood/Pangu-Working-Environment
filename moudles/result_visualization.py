import os
import numpy as np
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

def plot_surface_wind_temp(surface_ncfile_name, extent, t2m_levels, data_path, forecast_TIME, save_path):
    # Import the data, sort by latitude and choose the range
    surface_ncfile = os.path.join(data_path, surface_ncfile_name)
    surface_data, file_TIME = process_surface_data(surface_ncfile, extent)
    
    # Create the figure and axis
    proj = ccrs.PlateCarree()
    fig = plt.figure(dpi=500)
    ax = fig.add_subplot(111, projection=proj)
    ax_add_feature(ax, feature_scale='50m')
    ax_add_ticks(ax, proj, extent, 'small')
    if not forecast_TIME:
        data_source = " ERA5 data"
    else:
        data_source = f" From {forecast_TIME}hr forecast"
    ax.set_title(file_TIME+data_source)

    # Plot the contour figure of t2m
    cf = ax.contourf(surface_data.longitude,surface_data.latitude,surface_data.t2m, levels=t2m_levels, extend = 'both', cmap='RdYlBu_r')
    cb = fig.colorbar(cf, ax=ax, orientation='horizontal', shrink=0.5)
    cb.set_label('2m Temperature (°C)')
    cb.ax.tick_params(labelsize='small')

    # Plot the wind
    q = ax.quiver(surface_data.longitude,surface_data.latitude,surface_data.u10.values,surface_data.v10.values,
        scale_units='inches', scale=180, angles='uv',
              units='inches', width=0.005, headwidth=3, regrid_shape = 50, transform=proj)
    # Add the lengend of the wind
    w, h, u_show = -0.2, 0.3, 10 
    ax.quiverkey(
        q, X=1-w/2, Y=0.7*h, U=u_show,
        label=f'10m wind:\n{u_show} m/s', labelpos='S', labelsep=0.05,
        fontproperties={'size': 'x-small'}
    )
    
    fig_name = file_TIME + ' surface_wind_temp' + data_source
    fig_file = os.path.join(save_path, fig_name)
    fig.savefig(fig_file)

def ax_add_feature(ax, feature_scale):
    # Add some feature: coastline, rivers and borders
    ax.add_feature(cfeature.COASTLINE.with_scale(feature_scale),lw=0.5)
    ax.add_feature(cfeature.RIVERS.with_scale(feature_scale),lw=0.3,edgecolor='grey')
    ax.add_feature(cfeature.BORDERS.with_scale(feature_scale), linestyle='-',lw=0.3)

def ax_add_ticks(ax, proj, extent, fontsize='small'):
    xticks = np.arange(-180,190,10)
    yticks = np.arange(-90,100,10)
    ax.set_xticks(xticks, crs=proj)
    ax.set_yticks(yticks, crs=proj)
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.set_extent(extent, crs=proj)
    ax.tick_params(labelsize=fontsize)

def process_surface_data(surface_ncfile, extent):
    [lon_west, lon_east, lat_south, lat_north] = extent

    with xr.open_dataset(surface_ncfile,decode_times=False) as surface_data:
        surface_data = surface_data.sortby(surface_data.latitude)
        surface_data = surface_data.sel(
            longitude = slice(lon_west, lon_east),
            latitude = slice(lat_south,lat_north)
        )
        surface_data.t2m.values -= 273.15  # Change the unit of temperature to °C

    # Get the time of the file, and then cut the time dimension
    data_TIME = surface_data.time[0]
    data_TIME_units = surface_data.time.units
    file_TIME = str(nc.num2date(data_TIME, data_TIME_units))
    surface_data = surface_data.isel(time=0)

    return surface_data, file_TIME