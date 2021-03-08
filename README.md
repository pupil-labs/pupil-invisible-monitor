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

## Getting Started

<a
href="https://github.com/pupil-labs/pupil-invisible-monitor/releases/latest#user-content-downloads"
rel="noopener"
target="_blank">
	<p align="center">
		<img 
		src="https://raw.githubusercontent.com/wiki/pupil-labs/pupil-invisible-monitor/media/pupil_labs_pupil_invisible_app_banner.png" 
		alt="Pupil Labs - Pupil Invisible Monitor: desktop app to monitor real-time scene video and gaze data."/>
	</p>
</a>


To use Pupil Invisible Monitor app, please note the following: 
- Pupil Invisible Monitor app and Pupil Invisible Companion devices need to be connected to the **same WiFi** network. 
- **Public WiFi** networks often block the required communication protocols and typically they can **not** be used. 
- Some **anti-virus programs** may block the required communication protocols by default. 
- We recommend using a **dedicated wifi router** for low latency and ease of use.

### Using Pupil Invisible Companion

When Pupil Invisible Monitor is able to detect the Pupil Invisible Companion app, you will see a button appear at the bottom of the monitor window. Press the button to connect to your Pupil Invisible Companion Device. You can also press the key of the button's first letter on your keyboard.

The two letters of the button are the first two letters of the name of your Pupil Invisible Companion Device. This way you can easily differentiate between multiple Companion Devices in the same network.


## Developers

The below steps are only required for software developers looking to work with the source-code of the Pupil Invisible Monitor app. If you just want to use the app, download the latest release, from the link above. 

### Install from source

We recommend to setup a clean Python virtual environment for installing Pupil Invisible Monitor from source.

```sh
git clone git@github.com:pupil-labs/pupil-invisible-monitor.git
# Clone via HTTPS if you did not configure SSH correctly
# git clone https://github.com/pupil-labs/pupil-invisible-monitor.git

cd pupil-invisible-monitor/

# Use the Python 3 installation of your choice
python -m pip install -U pip
python -m pip install .

# Or if you want to use an editable installation:
python -m pip install -e .
```

### Run as Python module

After installating, Pupil Invisible Monitor is registered as a Python console script and can be executed from the command line via:

```sh
# equivalent to running `python -m pupil_invisible_monitor`
pupil_invisible_monitor
```

### Troubleshooting

- [ImportError: DLL load failed on Windows](https://github.com/pupil-labs/pupil-invisible-monitor/issues/24)
