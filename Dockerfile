FROM alpine
# Dependencies
RUN apk add --no-cache rclone python3

# Own config
WORKDIR /root

COPY rclone.conf .config/rclone/rclone.conf
COPY *.py /app/

ENTRYPOINT ["/usr/bin/python3", "/app/main.py"]
