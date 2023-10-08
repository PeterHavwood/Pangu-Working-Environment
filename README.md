## Pangu-Working-Environment
This is a working envrionment to run Pangu-Weather model on CPU environment.

This environment can download the input data, run the models for a given time or several time interval, and plot the results with given parameters.

The official repository of Pangu-Weather model is: https://github.com/198808xc/Pangu-Weather/tree/main

## Installation
**First** download Pangu models (The 4 links below are from the official repository of Pangu-Weather model).

* The 1-hour model (pangu_weather_1.onnx): [Google drive](https://drive.google.com/file/d/1fg5jkiN_5dHzKb-5H9Aw4MOmfILmeY-S/view?usp=share_link)/[Baidu netdisk](https://pan.baidu.com/s/1M7SAigVsCSH8hpw6DE8TDQ?pwd=ie0h)

* The 3-hour model (pangu_weather_3.onnx): [Google drive](https://drive.google.com/file/d/1EdoLlAXqE9iZLt9Ej9i-JW9LTJ9Jtewt/view?usp=share_link)/[Baidu netdisk](https://pan.baidu.com/s/197fZsoiCqZYzKwM7tyRrfg?pwd=gmcl)

* The 6-hour model (pangu_weather_6.onnx): [Google drive](https://drive.google.com/file/d/1a4XTktkZa5GCtjQxDJb_fNaqTAUiEJu4/view?usp=share_link)/[Baidu netdisk](https://pan.baidu.com/s/1q7IB7tNjqIwoGC7KVMPn4w?pwd=vxq3)

* The 24-hour model (pangu_weather_24.onnx): [Google drive](https://drive.google.com/file/d/1lweQlxcn9fG0zKNW8ne1Khr9ehRTI6HP/view?usp=share_link)/[Baidu netdisk](https://pan.baidu.com/s/179q2gkz2BrsOR6g3yfTVQg?pwd=eajy)


**Then** download files from this repository, and organize them with the onnx models as the following hierarchy:

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
│   |  ├── result_visualization.py
│   |  ├── ...
│   ├── run_model.py
│   ├── parameters.py
```

Set your python environment, and install all packages required using:
```
pip install -r requirements_cpu.txt
```

**Note** that to use the `cdsapi` package, you need follow the guide here to get the access to CDS data:
[How to use the CDS API](https://cds.climate.copernicus.eu/api-how-to)

The step 1 `Install the CDS API key` and step 2 `Install the CDS API client` are needed. And functions in `era5_download.py` will do the donwload for you automatically.

## Usage
To simply use Pangu models, you can just change the parameters to controll the inital date and the extent to plot in `parameters.py`, then:
```
python run_model.py
```
You can find the output data of netCDF format in the directory `/data/output_data` (you can create your own dirt to save these data), and figures in `/figure` (you can change it as well).

## Further Expand
* Add more plot functions.
* Fix any bug.
* [DONE] Add a python program only to plot the results.

## Code Explaination
#### Other
As there are many variables have 'time' in their names with different meanings, we use different spelling ways to distinguish them:
* TIME: the time of the data in reality, like 'input_TIME = 2019.09.01 00:00'
* Time: the time to record how long the program/function has run, like 'program_run_Time = 5min'
* time: the number of times that models should/have run, like 'work_times = 4'
