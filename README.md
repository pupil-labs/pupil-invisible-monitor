# Pupil Invisible Monitor
<a
href="https://pupil-labs.com/products/invisible"
rel="noopener"
target="_blank">
	<p align="center">
		<img 
		src="https://raw.githubusercontent.com/wiki/pupil-labs/pupil-invisible-monitor/media/pupil_labs_pupil_invisible_monitor_repo_banner.jpg" 
		alt="Pupil Labs - Pupil Invisible Monitor: desktop app to monitor real-time scene video and gaze data."/>
	</p>
</a>


Stand-alone desktop app used to view real-time video and gaze data from all Pupil Invisible Companion Devices on the same Wifi network.

## Users
[Download the latest Pupil Invisible Monitor app](https://github.com/pupil-labs/pupil-invisible-monitor/releases/latest "Pupil Invisible Monitor: desktop app to monitor real-time scene video and gaze data")

<a
href="https://github.com/pupil-labs/pupil-invisible-monitor/releases/latest"
rel="noopener"
target="_blank">
	<p align="center">
		<img 
		src="https://raw.githubusercontent.com/wiki/pupil-labs/pupil-invisible-monitor/media/pupil_labs_pupil_invisible_app_banner.jpg" 
		alt="Pupil Labs - Pupil Invisible Monitor: desktop app to monitor real-time scene video and gaze data."/>
	</p>
</a>


## Developers

The below sections are only required for software developers. If you just want to use the app, download the latest release, from the link above. 

### Install from source

```sh
git clone git@github.com:pupil-labs/pupil-invisible-monitor.git
# Clone via HTTPS if you did not configure SSH correctly
# git clone https://github.com/pupil-labs/pupil-invisible-monitor.git

cd pupil-invisible-monitor/

# Use the Python 3 installation of your choice
python -m pip install -U pip
python -m pip install -r requirements.txt
```

#### Windows DLLs
On Windows, additional steps are required:
1. Follow the [Pupil download instructions for the GLFW dll](https://docs.pupil-labs.com/#glfw-to-pupil-external)
1. Place the `glfw3.dll` file in the `windows_dlls` folder of this repository
1. Add the `windows_dlls` folder path to your Windows environment variable `Path`

### Run as Python module

```sh
# equivalent to running `python -m pupil_invisible_monitor`
pupil_invisible_monitor
```

