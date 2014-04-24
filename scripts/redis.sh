#!/usr/bin/env bash
/var/lib/redis/edit-redis-config.py && exec /usr/bin/redis-server /etc/redis/redis.conf
