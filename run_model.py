from moudles.era5_download import get_input_npy
from moudles.inference_session import initialize_sessions, run_sessions
from moudles.result_visualization import plot_surf_wind_temp

from parameters import (
    input_data_dir, output_data_dir,
    input_time, forecast_time, extent, t2m_levels,
    ort_options                   
    )

# Downloading the data of the inital field
print("=== Downloading the ERA5 data ===")
input_upper_ncfile_name, input_surface_ncfile_name = get_input_npy(input_time, input_data_dir)

# Initialize onnxruntime session for Pangu-Weather Models
print("\n=== Initialize onnxruntime session for Pangu-Weather Models ===")
ort_sessions = initialize_sessions(ort_options, forecast_time)

# Run the sessions
print("\n=== Running the inference sessions ===")
output_upper_ncfile_name, output_surface_ncfile_name = run_sessions(input_data_dir, output_data_dir, input_time, forecast_time, ort_sessions)

# Plot the input data and the results
print("\n=== Ploting the figures ===")
plot_surf_wind_temp(input_surface_ncfile_name, extent, t2m_levels, input_data_dir, 'figure')
plot_surf_wind_temp(output_surface_ncfile_name, extent, t2m_levels, output_data_dir, 'figure')

print("\n=== END ===")