## Pangu-Working-Environment
This is a working envrionment to run Pangu-Weather model on CPU environment.

This environment can download the input data, run the models for a given time or several time interval, and plot the results with given parameters.

The official repository of Pangu-Weather model is: https://github.com/198808xc/Pangu-Weather/tree/main

## Installation
**First** download and install Pangu models from the official repository: https://github.com/198808xc/Pangu-Weather/tree/main

The four onnx models (pangu_weather_*.onnx) is needed. 

And run the `requirements_cpu.txt` (which from the official respository):
```
pip install -r requirements_cpu.txt
```

**Then** you shall download files from this repository, and organize them with the onnx models as the following hierarchy:

```plain
├── root
│   ├── data
│   |  ├── input_data
│   |  ├── output_data
│   ├── figure
│   ├── pangu_weather_1.onnx
│   ├── pangu_weather_3.onnx
│   ├── pangu_weather_6.onnx
│   ├── pangu_weather_24.onnx
│   ├── moudles
│   |  ├── __init__.py
│   |  ├── era5_download.py
│   |  ├── inference_session.py
│   |  ├── npy_to_nc.py
│   |  ├── result_visualization.py
│   |  ├── work_time.py
│   ├── run_model.py
│   ├── parameters.py
```

## Usage
To simply use Pangu models, you can just change the parameters to controll the inital date and the extent to plot in `parameters.py`, then:
```
python run_model.py
```
You can find the output data of netCDF format in the directory `/data/output_data` (you can create your own dirt to save these data), and figures in `/figure` (you can change it as well).

