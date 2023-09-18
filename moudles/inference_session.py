import os
import time
import datetime
import netCDF4 as nc
import numpy as np
import onnxruntime as ort

from moudles.work_time import calculate_work_times
from moudles.npy_to_nc import npy2nc_surface, npy2nc_upper

def initialize_sessions(ort_options, forecast_time):
    # Record the time to initialize
    start_time = time.time()

    work_times = calculate_work_times(forecast_time)
    print(f"All the models used for the {forecast_time}hr prediction is: 24hr: {work_times[0]} || 6hr: {work_times[1]} || 3hr: {work_times[2]} || 1hr: {work_times[3]}")

    ort_session_24 = ort.InferenceSession('pangu_weather_24.onnx', sess_options=ort_options, providers=['CPUExecutionProvider']) if work_times[0] else None
    ort_session_6 = ort.InferenceSession('pangu_weather_6.onnx', sess_options=ort_options, providers=['CPUExecutionProvider']) if work_times[1] else None
    ort_session_3 = ort.InferenceSession('pangu_weather_3.onnx', sess_options=ort_options, providers=['CPUExecutionProvider']) if work_times[2] else None
    ort_session_1 = ort.InferenceSession('pangu_weather_1.onnx', sess_options=ort_options, providers=['CPUExecutionProvider']) if work_times[3] else None
    
    run_time = int(time.time() - start_time)
    print(f"Sessions have initalized. Time cost is {run_time//60}min {run_time%60}s.")

    return [ort_session_24, ort_session_6, ort_session_3, ort_session_1]


def run_sessions(input_data_dir, output_data_dir, input_time, ort_sessions,
                forecast_hour, total_forecast_hour, is_iteration ,iteration_index=1):
    # Record the running time
    start_time = time.time()

    # Calculate the number of times of each model works
    work_times_24 = forecast_hour//24
    work_times_6 = (forecast_hour%24)//6
    work_times_3 = (forecast_hour%24%6)//3
    work_times_1 = forecast_hour%24%6%3

    # Load the upper-air and surface numpy arrays 
    if is_iteration and iteration_index>1:
        # If the sessions are in iteration, then get input from intermediate numpy file
        input_upper = np.load(os.path.join(input_data_dir, 'intermediate_upper.npy')).astype(np.float32)
        input_surface = np.load(os.path.join(input_data_dir, 'intermediate_surface.npy')).astype(np.float32)
    else:
        input_upper = np.load(os.path.join(input_data_dir, 'input_upper.npy')).astype(np.float32)
        input_surface = np.load(os.path.join(input_data_dir, 'input_surface.npy')).astype(np.float32)

    # Run the inference session
    for i in range(work_times_24):
        run_time = int(time.time() - start_time)
        print(f"Running the 24hr-model: {i+1}/{work_times_24} || Running time: {run_time//60}min {run_time%60}s || Models remain: 24hr: {work_times_24-i-1}, 6hr: {work_times_6}, 3hr: {work_times_3}, 1hr: {work_times_1}")
        output_upper, output_surface = ort_sessions[0].run(None, {'input':input_upper, 'input_surface':input_surface})
        input_upper, input_surface = output_upper, output_surface

    for i in range(work_times_6):
        run_time = int(time.time() - start_time)
        print(f"Running the 6hr-model: {i+1}/{work_times_6} || Running time: {run_time//60}min {run_time%60}s || Models remain: 6hr: {work_times_6-i-1}, 3hr: {work_times_3}, 1hr: {work_times_1}")
        output_upper, output_surface = ort_sessions[1].run(None, {'input':input_upper, 'input_surface':input_surface})
        input_upper, input_surface = output_upper, output_surface

    for i in range(work_times_3):
        run_time = int(time.time() - start_time)
        print(f"Running the 3hr-model: {i+1}/{work_times_3} || Running time: {run_time//60}min {run_time%60}s || Models remain: 3hr: {work_times_3-i-1}, 1hr: {work_times_1}")
        output_upper, output_surface = ort_sessions[2].run(None, {'input':input_upper, 'input_surface':input_surface})
        input_upper, input_surface = output_upper, output_surface

    for i in range(work_times_1):
        run_time = int(time.time() - start_time)
        print(f"Running the 1hr-model: {i+1}/{work_times_1} || Running time: {run_time//60}min {run_time%60}s || Models remain: 1hr: {work_times_1-i-1}")
        output_upper, output_surface = ort_sessions[3].run(None, {'input':input_upper, 'input_surface':input_surface})
        input_upper, input_surface = output_upper, output_surface

    # Save the results
    if is_iteration:
        # If the sessions need to iterate, then save the results as intermediate numpy file
        np.save(os.path.join(input_data_dir, 'intermediate_upper.npy'), output_upper)
        np.save(os.path.join(input_data_dir, 'intermediate_surface.npy'), output_surface)

    np.save(os.path.join(output_data_dir, 'output_upper.npy'), output_upper)
    np.save(os.path.join(output_data_dir, 'output_surface.npy'), output_surface)

    # Transform the format of results from numpy to netCDF
    output_time = input_time + datetime.timedelta(hours=forecast_hour)
    output_year, output_month, output_day, output_hour = output_time.year, output_time.month, output_time.day, output_time.hour

    output_upper_ncfile_name = f'output_{total_forecast_hour}_upper_'+str(output_year).zfill(4)+str(output_month).zfill(2)+str(output_day).zfill(2)+str(output_hour).zfill(2)+'.nc'
    output_surface_ncfile_name = f'output_{total_forecast_hour}_surface_'+str(output_year).zfill(4)+str(output_month).zfill(2)+str(output_day).zfill(2)+str(output_hour).zfill(2)+'.nc'

    output_time_nc = nc.date2num(output_time, "hours since 1900-01-01 00:00:00.0")
    npy2nc_upper(output_upper, output_time_nc, output_upper_ncfile_name, output_data_dir)
    npy2nc_surface(output_surface, output_time_nc, output_surface_ncfile_name, output_data_dir)

    # End
    run_time = int(time.time() - start_time)
    print(f"Results have saved. Total time cost is {run_time//60}min {run_time%60}s.")
    return output_upper_ncfile_name, output_surface_ncfile_name