# Deployment / Bundling

1. Install `pyinstaller`
1. Change working directory to `<repository root>`
1. Install all requirements listed in `requirements.txt`
1. Install pi_monitor via `pip install pi_monitor`
1. Change working directory to `deployment/`
1. Run `pyinstaller -y pi_monitor.spec`
