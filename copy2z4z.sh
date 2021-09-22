#!/bin/bash
# This script mounts the Sharepoint-Songs folder as fuse mount,
# establishes a watcher on all files in "2-Zeilig"-folder
# and then copies every changed file to "4-Zeilig" with reformatting applied.
#
# Requirements:
# rclone configured with the SharePoint site at remote "ImmanuelRV-Technik"
# fswatch
# python3

# CONFIG:
# Working directory
workdir=.
# Name of the folder where SharePoint is mounted
mountdir=songs
# Time between checks if files have changed
latency=5

# Signal handling
sighandler() {
    echo "Signal caught! Shutting down..."
    # Stop watcher
    kill -INT "$child"
    # Wait for watcher to exit before unmounting SharePoint
    echo -e "Waiting for fswatcher to exit...\n"
    wait "$child"
    # Unmount SharePoint
    fusermount -uz $mountdir
    # Quit the Script
    echo "Done. Exiting..."
    exit
}
trap sighandler INT TERM ABRT

# Setup directories
cd $workdir
mkdir -p $mountdir

# Mount SharePoint
rclone mount --vfs-cache-mode writes --dir-cache-time ${latency}s ImmanuelRV-Technik:Songbeamer/Songs $mountdir &

# Wait for SharePoint
while [ ! -d $mountdir/2-Zeilig ]; do
    sleep 1
done

echo "SharePoint set up! Launching fswatcher..."

# Setup watcher pipeline:
# -0: Separate single events with a NUL-Character, to avoid confusion with possible newlines in filenames
# -r: Recurse path; -x: Print events; -m: Set monitor to polling, since inotify can't handle FUSE filesystems
# --event {Created|Updated|Removed}: Only react when a file was created, modified or deleted
# $mountdir/2-Zeilig: Watch in this directory
# xargs: For every NUL-Seperated entry, launch the python script with this entry as argument
# Watcher has to run in Background so the script can monitor for sent Signals
fswatch -0rxm poll_monitor \
         --event Created --event Updated --event Removed \
         $mountdir/2-Zeilig $mountdir/4-Zeilig \
     |xargs -0rn1 python3 copy2z4z.py &
child=$(jobs -p 2)

# Wait for fswatcher. This prevents the Shell script from exiting so we can still listen for signals
echo "Ready to go."
wait "$child"

# If the watcher exited prematurely (no signal sent from host), call cleanup manually
sighandler
