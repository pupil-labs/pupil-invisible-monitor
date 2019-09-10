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

## Run as Python module

```sh
# Use the Python 3 installation of your choice
python -m pupil_invisible_monitor
```

## Deployment

### Deployment dependencies
Run the _Installation from source_ instructions but replace the last step with
```sh
python -m pip install -r requirements_deploy.txt
```

### Bundling
```sh
cd deployment/
pyinstaller -y pi_monitor.spec
```

The resulting distribution file will be copied to `deployment/bundles`.