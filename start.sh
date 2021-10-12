#!/bin/sh
cd $(dirname $0)
docker build -t songscopy .
exec docker run --cap-add SYS_ADMIN --device /dev/fuse --privileged=True songscopy $@
