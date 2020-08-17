# Deployment

## Deployment dependencies
Run the _Install from source_ instructions, but install with the **deploy** option:
```sh
python -m pip install ".[deploy]"
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
pyinstaller --clean -y pi_monitor.spec
```

The resulting distribution file will be copied to `deployment/bundles`.

## Troubleshooting
**The computer running Pupil Invisible Monitor and the Pupil Invisible Companion device are connected to the same network, but the Companion device still does not show up in Pupil Invisible Monitor!**

If you are connected to a large/public WiFi network, there is a chance that UDP transport is blocked. If this is the case, Pupil Invisible Monitor and Pupil Invisible Companion will not be able to communicate.

You could try setting up a hotspot on the machine running Pupil Invisible Monitor instead. For optimal latency, you would ideally use a dedicated router. Note that internet is not a requirement for the usage of Pupil Invisible Monitor.

