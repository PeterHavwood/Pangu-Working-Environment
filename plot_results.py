import datetime

import moudles.name_file as nf
from moudles.result_visualization import plot_surface_wind_temp

from parameters import (
    input_data_dir, output_data_dir, figure_dir,
    input_TIME, single_forecast_hour, forecast_times, extent, t2m_levels,
    )

# Plot for the input data
plot_surface_wind_temp(nf.name_era5_surface_ncfile(input_TIME), extent, t2m_levels, input_data_dir, figure_dir)

# Plot for the output results
for i in range(forecast_times):
    intermediate_TIME = input_TIME + datetime.timedelta(hours=single_forecast_hour*(i+1))
    plot_surface_wind_temp(nf.name_output_surface_ncfile(intermediate_TIME,single_forecast_hour*(i+1)), extent, t2m_levels, output_data_dir, figure_dir, single_forecast_hour*(i+1))