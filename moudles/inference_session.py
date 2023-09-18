import os
import time
import netCDF4 as nc
import numpy as np
import onnxruntime as ort

from moudles.work_time import calculate_work_times
from moudles.npy_to_nc import npy2nc_surface, npy2nc_upper
from moudles.name_file import name_output_upper_ncfile, name_output_surface_ncfile

# As there are many variables have 'time' in their names with different meaning
# We use different spelling ways to distinguish them
# TIME: the time of the data in reality, like 'input_TIME = 2019.09.01 00:00'
# Time: the time to record how long the program/function has run, like 'program_run_Time = 5min'
# time: the number of times that models should/have run, like 'work_times = 4'

def initialize_sessions(ort_options, forecast_hour):
    # Record the time to initialize
    start_Time = time.time()

    work_times = calculate_work_times(forecast_hour)
    print(f"All the models used for the {forecast_hour}hr prediction is: 24hr: {work_times[0]} || 6hr: {work_times[1]} || 3hr: {work_times[2]} || 1hr: {work_times[3]}")

    ort_session_24 = ort.InferenceSession('pangu_weather_24.onnx', sess_options=ort_options, providers=['CPUExecutionProvider']) if work_times[0] else None
    ort_session_6 = ort.InferenceSession('pangu_weather_6.onnx', sess_options=ort_options, providers=['CPUExecutionProvider']) if work_times[1] else None
    ort_session_3 = ort.InferenceSession('pangu_weather_3.onnx', sess_options=ort_options, providers=['CPUExecutionProvider']) if work_times[2] else None
    ort_session_1 = ort.InferenceSession('pangu_weather_1.onnx', sess_options=ort_options, providers=['CPUExecutionProvider']) if work_times[3] else None
    
    run_Time = int(time.time() - start_Time)
    print(f"Sessions have initalized. Time cost is {run_Time//60}min {run_Time%60}s.")

    return [ort_session_24, ort_session_6, ort_session_3, ort_session_1]


def run_sessions(input_data_dir, output_data_dir, output_TIME, program_start_Time, ort_sessions,
                forecast_hour, total_forecast_hour, is_iteration ,iteration_index=1):
    # Record the running time of the function
    function_start_Time = time.time()

    # Calculate the number of times of each model works
    work_times = calculate_work_times(forecast_hour)
    not_complete_times = work_times.copy()

    # Load the upper-air and surface numpy arrays 
    if is_iteration and iteration_index>1:
        # If the sessions are in iteration, then get input from intermediate numpy file
        input_upper = np.load(os.path.join(input_data_dir, 'intermediate_upper.npy')).astype(np.float32)
        input_surface = np.load(os.path.join(input_data_dir, 'intermediate_surface.npy')).astype(np.float32)
    else:
        input_upper = np.load(os.path.join(input_data_dir, 'input_upper.npy')).astype(np.float32)
        input_surface = np.load(os.path.join(input_data_dir, 'input_surface.npy')).astype(np.float32)

    # Run the inference session
    hour_str = ['24','6','3','1']
    for model_index in range(4):
        for current_work_time in range(work_times[model_index]):
            program_run_Time = int(time.time() - program_start_Time)

            not_complete_times[model_index] -= 1

            print(f"Running the {hour_str[model_index]}hr-model: {current_work_time+1}/{work_times[model_index]} || " +
                    f"Running time till now: {program_run_Time//60}min {program_run_Time%60}s || " +
                    f"Models remain: 24hr: {not_complete_times[0]}, 6hr: {not_complete_times[1]}, 3hr: {not_complete_times[2]}, 1hr: {not_complete_times[3]}")
            
            output_upper, output_surface = ort_sessions[model_index].run(None, {'input':input_upper, 'input_surface':input_surface})
            input_upper, input_surface = output_upper, output_surface

    # Save the results
    if is_iteration:
        # If the sessions need to iterate, then save the results as intermediate numpy file
        np.save(os.path.join(input_data_dir, 'intermediate_upper.npy'), output_upper)
        np.save(os.path.join(input_data_dir, 'intermediate_surface.npy'), output_surface)

    np.save(os.path.join(output_data_dir, 'output_upper.npy'), output_upper)
    np.save(os.path.join(output_data_dir, 'output_surface.npy'), output_surface)

    # Transform the format of results from numpy to netCDF
    output_upper_ncfile_name = name_output_upper_ncfile(output_TIME, total_forecast_hour)
    output_surface_ncfile_name = name_output_surface_ncfile(output_TIME, total_forecast_hour)

    output_TIME_nc = nc.date2num(output_TIME, "hours since 1900-01-01 00:00:00.0")
    npy2nc_upper(output_upper, output_TIME_nc, output_upper_ncfile_name, output_data_dir)
    npy2nc_surface(output_surface, output_TIME_nc, output_surface_ncfile_name, output_data_dir)

    # End
    function_run_Time = int(time.time() - function_start_Time)
    print(f"Results have saved. Time cost of this session is {function_run_Time//60}min {function_run_Time%60}s.")
    return output_upper_ncfile_name, output_surface_ncfile_name