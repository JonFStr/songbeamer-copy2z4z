#!/bin/sh
# This script mounts the Sharepoint-Songs folder as fuse mount,
# establishes a watcher on all files in "2-Zeilig"-folder
# and then copies every changed file to "4-Zeilig" with reformatting applied.
#
# Requirements:
# rclone configured with the SharePoint site at remote "ImmanuelRV-Technik"
# fswatch
# python3

# CONFIG:
workdir=.
mountdir=songs
latency=10s

# Signal handling
sighandler() {
    pkill -INT fswatch
    fusermount -uz $mountdir
    exit
}
trap sighandler INT TERM ABRT

# Setup directories
cd $workdir
mkdir -p $mountdir

# Mount SharePoint
rclone mount --vfs-cache-mode writes --dir-cache-time $latency ImmanuelRV-Technik:Songbeamer/Songs $mountdir &

# Wait for SharePoint
while [ ! -d $mountdir/2-Zeilig ]; do
    sleep 1
done

# Setup watcher pipeline [r: Recurse path; x: Print events; m: Set monitor to polling; 1>&2: Write to stderr and pipeline for monitoring]
fswatch -0rxm poll_monitor --event Created --event Updated --event Removed $mountdir/2-Zeilig |tee asdf |xargs -0n1 python copy2z4z.py
