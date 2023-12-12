#!/bin/sh
# Change to script location
cd "$(dirname "$0")" || exit
# Build image
docker build -t songscopy .
exec docker run songscopy "$@"
