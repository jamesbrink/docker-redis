# Redis 2.2.12
#
# VERSION       1.0

FROM ubuntu
MAINTAINER James Brink, brink.james@gmail.com

# make sure the package repository is up to date
RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get update

RUN apt-get install -y redis-server
RUN chown -R redis:redis /etc/redis/

USER redis

# Configuration options


# Run in foreground and listen on all addresses.
RUN sed -ri 's/^daemonize (yes|no)$/daemonize no/g' /etc/redis/redis.conf
RUN sed -ri 's/^bind .*$/bind 0.0.0.0/g' /etc/redis/redis.conf
# Send logs to foreground as well
RUN sed -ri 's/^logfile \/var\/log\/redis\/redis-server.log$/logfile \/var\/log\/redis\/redis-server.log\nlogfile stdout/g' /etc/redis/redis.conf

EXPOSE 6379
CMD ["/usr/bin/redis-server", "/etc/redis/redis.conf"]


