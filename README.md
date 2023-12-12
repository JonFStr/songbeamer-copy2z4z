# Songbeamer Version Control
This Script scans predefined directories from OneDrive for changes in [SongBeamer](https://songbeamer.de) (`.sng`) files and copies them to another directory after removing certain slide seperators to increase the number of lines per slide (or vice-versa)

# OneDrive authentication
This script uses [Rclone](https://rclone.org) for access to Microsoft OneDrive.

For generating the `rclone.conf` file, please refer to the [Rclone docs](https://rclone.org/onedrive/)

The name of the Rclone remote as well as the root directory of songs is set in [`config.py`](/config.py#L4) (
currently: `remote:Songbeamer/Songs`).  
The subdirectories for the different versions are set in [here](/config.py#L6) (`2-Zeilig/` and `4-Zeilig/`).
