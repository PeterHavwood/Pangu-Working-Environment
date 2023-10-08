import datetime
import onnxruntime as ort
import numpy as np

# Inital time
year = 2023
month = 10
day = 1
hour = 0

input_TIME = datetime.datetime(year,month,day,hour)

# Time to forecast in hour
single_forecast_hour = 6
forecast_times = 4*6

# Extent to plot
lon_west = 100
lon_east = 150
lat_south = 10
lat_north = 30

extent = [lon_west, lon_east, lat_south, lat_north]

# Temperature levels
t2m_levels = np.linspace(0, 40, 21)

# The directory of data and figures
input_data_dir = './data/input_data'
output_data_dir = './data/output_data'
figure_dir = './figure/Koinu_23'

# Options of  onnxruntime
ort_options = ort.SessionOptions()
ort_options.enable_cpu_mem_arena = False
ort_options.enable_mem_pattern   = False
ort_options.enable_mem_reuse     = False
# Increase the number for faster inference and more memory consumption
ort_options.intra_op_num_threads = 1