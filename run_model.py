import datetime
from moudles.era5_download import get_input_npy
from moudles.inference_session import initialize_sessions, run_sessions
from moudles.result_visualization import plot_surface_wind_temp

from parameters import (
    input_data_dir, output_data_dir,
    input_time, single_forecast_hour, forecast_times, extent, t2m_levels,
    ort_options                   
    )

# Downloading the data of the inital field
print("=== Downloading the ERA5 data ===")
input_upper_ncfile_name, input_surface_ncfile_name = get_input_npy(input_time, input_data_dir)
print("\n=== Ploting the figures of the input data ===")
plot_surface_wind_temp(input_surface_ncfile_name, extent, t2m_levels, input_data_dir, 0, 'figure')

# Initialize onnxruntime session for Pangu-Weather Models
print("\n=== Initialize onnxruntime session for Pangu-Weather Models ===")
ort_sessions = initialize_sessions(ort_options, single_forecast_hour)

# Doing forecast
if forecast_times > 1:
    intermediate_time = input_time
    # Iterate to forcast
    for i in range(forecast_times):
        # Run the sessions
        intermediate_time = intermediate_time + datetime.timedelta(hours=single_forecast_hour)
        print(f"\n=== Running the inference sessions to forecast (iteration): {i+1}/{forecast_times} || Forecast time: {intermediate_time} ===")
        output_upper_ncfile_name, output_surface_ncfile_name = \
            run_sessions(input_data_dir, output_data_dir, intermediate_time, ort_sessions, single_forecast_hour, single_forecast_hour*(i+1), True, i+1)
        # Plot the results
        print("\n=== Ploting the figures ===")
        plot_surface_wind_temp(output_surface_ncfile_name, extent, t2m_levels, output_data_dir, single_forecast_hour*(i+1),'figure')
else:
    # Run the sessions
    print(f"\n=== Running the inference sessions to forecast ===")
    output_upper_ncfile_name, output_surface_ncfile_name = \
        run_sessions(input_data_dir, output_data_dir, input_time, ort_sessions, single_forecast_hour, False)
    # Plot the results
    print("\n=== Ploting the figures ===")
    plot_surface_wind_temp(output_surface_ncfile_name, extent, t2m_levels, output_data_dir, single_forecast_hour,  'figure')

print("\n=== END ===")