import datetime
import onnxruntime as ort
import numpy as np

# Inital time
year = 2019
month = 8
day = 7
hour = 6

input_TIME = datetime.datetime(year,month,day,hour)

# Time to forecast in hour
single_forecast_hour = 6
forecast_times = 5

# Extent to plot
lon_west = 110
lon_east = 130
lat_south = 20
lat_north = 30

extent = [lon_west, lon_east, lat_south, lat_north]

# Temperature levels
t2m_levels = np.linspace(0, 40, 21)

# The directory of data and figures
input_data_dir = './data/input_data'
output_data_dir = './data/output_data'
figure_dir = './figure'

# Options of  onnxruntime
ort_options = ort.SessionOptions()
ort_options.enable_cpu_mem_arena = False
ort_options.enable_mem_pattern   = False
ort_options.enable_mem_reuse     = False
# Increase the number for faster inference and more memory consumption
ort_options.intra_op_num_threads = 1