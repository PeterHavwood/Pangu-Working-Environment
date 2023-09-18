import datetime
import time
from moudles.era5_download import get_input_npy
from moudles.inference_session import initialize_sessions, run_sessions
from moudles.result_visualization import plot_surface_wind_temp

from parameters import (
    input_data_dir, output_data_dir, figure_dir,
    input_TIME, single_forecast_hour, forecast_times, extent, t2m_levels,
    ort_options                   
    )

# As there are many variables have 'time' in their names with different meaning
# We use different spelling ways to distinguish them
# TIME: the time of the data in reality, like 'input_TIME = 2019.09.01 00:00'
# Time: the time to record how long the program/function has run, like 'program_run_Time = 5min'
# time: the number of times that models should/have run, like 'work_times = 4'

# Record the running time
program_start_Time = time.time()

# Downloading the data of the inital field
print("=== Downloading the ERA5 data ===")
input_upper_ncfile_name, input_surface_ncfile_name = get_input_npy(input_TIME, input_data_dir)
print("\n=== Ploting the figures of the input data ===")
plot_surface_wind_temp(input_surface_ncfile_name, extent, t2m_levels, input_data_dir, 0, figure_dir)

# Initialize onnxruntime session for Pangu-Weather Models
print("\n=== Initialize onnxruntime sessions for Pangu-Weather Models ===")
ort_sessions = initialize_sessions(ort_options, single_forecast_hour)


# Doing forecast
if forecast_times > 1:
    intermediate_TIME = input_TIME
    # Iterate to forcast
    for i in range(forecast_times):
        # Run the sessions
        print(f"\n=== Running the inference sessions to forecast (iteration): {i+1}/{forecast_times} || Forecast time: {intermediate_TIME} ===")
        intermediate_TIME = intermediate_TIME + datetime.timedelta(hours=single_forecast_hour)
        output_upper_ncfile_name, output_surface_ncfile_name = \
            run_sessions(input_data_dir, output_data_dir, intermediate_TIME, program_start_Time, ort_sessions, single_forecast_hour, single_forecast_hour*(i+1), True, i+1)
        # Plot the results
        print("\n=== Ploting the figures ===")
        plot_surface_wind_temp(output_surface_ncfile_name, extent, t2m_levels, output_data_dir, single_forecast_hour*(i+1),figure_dir)
else:
    # Run the sessions
    print(f"\n=== Running the inference session to forecast ===")
    output_TIME = input_TIME + datetime.timedelta(hours=single_forecast_hour)
    output_upper_ncfile_name, output_surface_ncfile_name = \
        run_sessions(input_data_dir, output_data_dir, output_TIME, program_start_Time, ort_sessions, single_forecast_hour, single_forecast_hour, False)
    # Plot the results
    print("\n=== Ploting the figures ===")
    plot_surface_wind_temp(output_surface_ncfile_name, extent, t2m_levels, output_data_dir, single_forecast_hour,  figure_dir)

print("\n=== END ===")
program_run_Time = int(time.time() - program_start_Time)
print(f"Totoal time cost: {program_run_Time//60}min {program_run_Time%60}s")