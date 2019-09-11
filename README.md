# Pupil Invisible Monitor
Stand alone desktop app to monitor present Pupil Invisible Companions.

## Installation from source

```sh
git clone git@github.com:pupil-labs/pupil-invisible-monitor.git
# Clone via HTTPS if you did not configure SSH correctly
# git clone https://github.com/pupil-labs/pupil-invisible-monitor.git

cd pupil-invisible-monitor/

# Use the Python 3 installation of your choice
python -m pip install -U pip
python -m pip install -r requirements.txt
```

### Windows DLLs
On Windows, additional steps are required:
1. Follow the [Pupil download instructions for the GLFW dll](https://docs.pupil-labs.com/#glfw-to-pupil-external)
1. Place the `glfw3.dll` file in the `windows_dlls` folder of this repository
1. Add the `windows_dlls` folder path to your Windows environment variable `Path`

## Run as Python module

```sh
# equivalent to running `python -m pupil_invisible_monitor`
pupil_invisible_monitor
```

## Deployment

### Deployment dependencies
Run the _Installation from source_ instructions but replace the last step with
```sh
python -m pip install -r requirements_deploy.txt
```

### Icon files

Install platform-specific icons to `deployment/icons`.

Expected icon file names:
- macOS: `pupil_invisible_monitor.icns`
- Linux: `pupil_invisible_monitor.svg`
- Windows: `pupil_invisible_monitor.ico`

### macOS signing

macOS requires your bundle to be signed if you you want to distribute it.
The deployment procedure will attempt to sign the bundle using a private key named
`Developer ID Application: Pupil Labs UG (haftungsbeschrankt) (R55K9ESN6B)`.

If this key is not present in your keychain the deployment procedure will log a warning
and not sign the bundle. This might result in problems when the bundle is started on
a different Mac.

### Bundling
```sh
cd deployment/
git clean -dxf -e icons/  # remove previously built files
pyinstaller -y pi_monitor.spec
```

The resulting distribution file will be copied to `deployment/bundles`.