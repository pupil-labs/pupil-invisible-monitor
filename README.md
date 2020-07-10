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
		src="https://raw.githubusercontent.com/wiki/pupil-labs/pupil-invisible-monitor/media/pupil_labs_pupil_invisible_app_banner.jpg" 
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

### Setup Dependencies

#### Linux
Pupil Invisible Monitor depends on GLFW-3.3 or above. Note that currently Ubuntu only offers packages for version 3.2, so you might need to install GLFW-3.3 [from source](https://github.com/glfw/glfw/releases/tag/3.3). Make sure to compile as a shared library! You might use the following snippet:
```bash
# install dependencies
sudo apt install xorg-dev

# download and unzip
wget https://github.com/glfw/glfw/releases/download/3.3/glfw-3.3.zip
unzip glfw-3.3.zip
cd glfw-3.3

# build and install as shared library
cmake . -DBUILD_SHARED_LIBS=ON
make -j4
sudo make install

# cleanup downloaded files
cd ..
rm glfw-3.3.zip
rm -r glfw-3.3
```

#### Windows
On Windows you will need to setup glfw correctly:
1. Download the 64-bit Windows binaries from https://www.glfw.org/download.html
1. Extract the downloaded zip file.
1. Copy the file `glfw3.dll` from the extracted `lib-vc2015` folder to the `windows_dlls` folder of this repository.
1. Add the `windows_dlls` folder to your Windows environment variable `Path`

### Install from source
After setting up the required dependencies, you can download the source code for Pupil Invisible Monitor and proceed with the installation:

```sh
git clone git@github.com:pupil-labs/pupil-invisible-monitor.git
# Clone via HTTPS if you did not configure SSH correctly
# git clone https://github.com/pupil-labs/pupil-invisible-monitor.git

cd pupil-invisible-monitor/

# Use the Python 3 installation of your choice
python -m pip install -U pip
python -m pip install -r requirements.txt
```

### Run as Python module

```sh
# equivalent to running `python -m pupil_invisible_monitor`
pupil_invisible_monitor
```
