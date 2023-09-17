import numpy as np

def calculate_work_times(forecast_time):
    work_times = np.zeros(4, dtype=np.int32)
    work_times[0] = forecast_time//24
    work_times[1] = (forecast_time%24)//6
    work_times[2] = (forecast_time%24%6)//3
    work_times[3] = forecast_time%24%6%3

    return work_times