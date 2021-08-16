FROM alpine
# Copied from github.com/rclone/rclone/blob/master/Dockerfile
RUN apk add --no-cache ca-certificates fuse tzdata rclone python3
#RUN addgroup -g 1009 rclone && adduser -u 1009 -Ds /bin/sh -G rclone rclone

# Install fswatch
WORKDIR /root
RUN apk add --no-cache file git autoconf automake libtool make g++ texinfo curl
RUN curl -L 'https://github.com/emcrisostomo/fswatch/releases/download/1.16.0/fswatch-1.16.0.tar.gz' |tar xvz

WORKDIR /root/fswatch-1.16.0
RUN ./configure && make && make install && make distclean

# Own config
WORKDIR /root

COPY rclone.conf .config/rclone/rclone.conf
COPY copy2z4z* ./

ENTRYPOINT ["/root/copy2z4z.sh"]
