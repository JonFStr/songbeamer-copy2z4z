FROM alpine
# Dependencies
RUN apk add --no-cache rclone python3

# Own config
WORKDIR /root

RUN mkdir -p /root/.config/rclone/
COPY app/ /app/

ENTRYPOINT ["/usr/bin/python3", "/app/main.py"]
