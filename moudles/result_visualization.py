import os
import numpy as np
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

def plot_surf_wind_temp(surf_ncfile_name, extent, t2m_levels, data_path, save_path):
    [lon_west, lon_east, lat_south, lat_north] = extent

    # Import the data, sort by latitude and choose the range
    surf_ncfile = os.path.join(data_path, surf_ncfile_name)
    with xr.open_dataset(surf_ncfile,decode_times=False) as surf_data:
        surf_data = surf_data.sortby(surf_data.latitude)
        surf_data = surf_data.sel(
            longitude = slice(lon_west, lon_east),
            latitude = slice(lat_south,lat_north)
        )
        surf_data.t2m.values -= 273.15  # Change the unit of temperature to °C

    # Get the time of the file, and then cut the time dimension
    data_time = surf_data.time[0]
    data_time_units = surf_data.time.units
    file_time = str(nc.num2date(data_time, data_time_units))
    surf_data = surf_data.isel(time=0)

    # Create the figure and axis
    proj = ccrs.PlateCarree()
    fig = plt.figure(dpi=500)
    ax = fig.add_subplot(111, projection=proj)
    ax.set_title(file_time)
    ax_add_feature(ax, feature_scale='50m')
    ax_add_ticks(ax, proj, extent, 'small')

    # Plot the contour figure of t2m
    cf = ax.contourf(surf_data.longitude,surf_data.latitude,surf_data.t2m, levels=t2m_levels, cmap='RdYlBu_r')
    cb = fig.colorbar(cf, ax=ax, orientation='horizontal', shrink=0.5)
    cb.set_label('2m Temperature (°C)')
    cb.ax.tick_params(labelsize='small')

    # Plot the wind
    q = ax.quiver(surf_data.longitude,surf_data.latitude,surf_data.u10.values,surf_data.v10.values,
        scale_units='inches', scale=180, angles='uv',
              units='inches', width=0.005, headwidth=3, regrid_shape = 50, transform=proj)
    # Add the lengend of the wind
    w, h, u_show = -0.2, 0.3, 10 
    ax.quiverkey(
        q, X=1-w/2, Y=0.7*h, U=u_show,
        label=f'10m wind:\n{u_show} m/s', labelpos='S', labelsep=0.05,
        fontproperties={'size': 'x-small'}
    )
    
    fig_name = file_time + ' surf_wind_temp'
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