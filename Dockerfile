# Redis 2.2.12
#
# VERSION       1.0

FROM ubuntu
MAINTAINER James Brink, brink.james@gmail.com

# Make sure the package repository is up to date
RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get update

RUN apt-get install -y redis-server
RUN chown -R redis:redis /etc/redis/

ADD ./scripts/redis.sh /var/lib/redis/redis.sh
RUN chmod +x /var/lib/redis/redis.sh

ADD ./scripts/edit-redis-config.py /var/lib/redis/edit-redis-config.py
RUN chmod +x /var/lib/redis/edit-redis-config.py

USER redis

# Configuration options
ENV TIMEOUT 300
ENV LOGLEVEL notice
ENV DATABASES 16
ENV RDBCOMPRESSION yes
ENV DBFILENAME dump.rdb
ENV APPENDONLY no
ENV APPENDFSYNC everysec
ENV NO-APPEND-FSYNC-ON-REWRITE no
ENV VM-ENABLED no
ENV VM-MAX-MEMORY 0
ENV VM-PAGE-SIZE 32
ENV VM-PAGES 134217728
ENV VM-MAX-THREADS 4
ENV HASH-MAX-ZIPMAP-ENTRIES 512
ENV HASH-MAX-ZIPMAP-VALUE 64
ENV LIST-MAX-ZIPMAP-ENTRIES 512
ENV LIST-MAX-ZIPMAP-VALUE 64
ENV SET-MAX-INTSET-ENTRIES 512
ENV ACTIVEREHASHING yes

# Run in foreground and listen on all addresses.
RUN sed -ri 's/^daemonize (yes|no)$/daemonize no/g' /etc/redis/redis.conf
RUN sed -ri 's/^bind .*$/bind 0.0.0.0/g' /etc/redis/redis.conf
# Send logs to foreground as well
RUN sed -ri 's/^logfile \/var\/log\/redis\/redis-server.log$/logfile \/var\/log\/redis\/redis-server.log\nlogfile stdout/g' /etc/redis/redis.conf

EXPOSE 6379
CMD ["/var/lib/redis/redis.sh"]


