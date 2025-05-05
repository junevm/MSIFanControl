# MSIFanControl

- Provides a UI and automated scripts in order to control MSI Laptops. Check the #Supported section to see what models are supported.
- Made for Linux, as MSI does not have a native Linux client.

# INSTALLATION / UPDATING

- `cd` into the download folder and execute the following commands:
  - `chmod +x file_1.sh`
  - `chmod +x file_2.sh`
  - `chmod +x install.sh`
- Now run the `install.sh`, That will install all the dependencies and create a virtual python environment on desktop for the script to work.
- If you get any like `FileNotFoundError: [Errno 2] No such file or directory: '/sys/kernel/debug/ec/ec0/io'` then run the following command:
  - `sudo modprobe ec_sys write_support=1`
- (ONLY FOR INSTALLATION) `Reboot` after the script complete the first run.

# RUNNING

- Run `install.sh` from the desktop folder.

## Supported Laptop models (tested)

- MSI GF65 Thin 9SD

## Supported Linux Distro (tested)

- Zorin

## Acknowledgements

- https://github.com/YoyPa/isw
- https://github.com/YoCodingMonster/OpenFreezeCenter
