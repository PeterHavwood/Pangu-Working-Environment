## Pangu-Working-Environment
This is a working envrionment to run Pangu-Weather model on CPU environment.

This environment can download the input data, run the models for a given time or several time interval, and plot the results with given parameters.

The official repository of Pangu-Weather model is: https://github.com/198808xc/Pangu-Weather/tree/main

## Installation
Download and install Pangu models from the official repository: https://github.com/198808xc/Pangu-Weather/tree/main

The four onnx models (pangu_weather_*.onnx) is needed. 

And run the `requirements_cpu.txt` in the official repository:
```
pip install -r requirements_cpu.txt
```

Then you shall download files from this repository, and organize them with the onnx models as the following hierarchy:

```plain
├── root
│   ├── data
│   |  ├── input_data
│   |  ├── output_data
│   ├── pangu_weather_1.onnx
│   ├── pangu_weather_3.onnx
│   ├── pangu_weather_6.onnx
│   ├── pangu_weather_24.onnx
│   ├── moudles
│   |  ├── era5_download.py
│   |  ├── era5_download.py
│   |  ├── npy_to_nc.py
│   |  ├── result_visualization.py
│   |  ├── work_time.py
│   ├── run_model.py
│   ├── parameters.py
```
