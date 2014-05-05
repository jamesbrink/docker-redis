Docker Container for Redis 2.8.4
============

A highly configurable Docker container running [Redis 2.8.4](http://redis.io/)

##Usage##

To run with default settings

```
james@ubuntu:~$ docker run -P --name redis jamesbrink/redis
```

To run with customized settings, for example log level debug (see the Enviroment Variables section below for configuration options).

```
james@ubuntu:~$ docker run -P --name redis -e LOGLEVEL=debug jamesbrink/redis
```

This will fire off Redis with debug logging. See the following example of the output.

    james@ubuntu:~$ docker run -P --name redis -e LOGLEVEL=debug jamesbrink/redis
    ================================================================================
    Altering coniguration using the following settings:
    ================================================================================
    timeout value: 300
    loglevel value: debug
    databases value: 16
    rdbcompression value: yes
    dbfilename value: dump.rdb
    appendonly value: no
    appendfsync value: everysec
    no-append-fsync-on-rewrite value: no
    vm-enabled value: no
    vm-max-memory value: 0
    vm-page-size value: 32
    vm-pages value: 134217728
    vm-max-threads value: 4
    hash-max-zipmap-entries value: 512
    hash-max-zipmap-value value: 64
    list-max-zipmap-entries value: 512
    list-max-zipmap-value value: 64
    set-max-intset-entries value: 512
    activerehashing value: yes
    ================================================================================
    Configuration updated
    ================================================================================
    [1] 24 Apr 03:24:08 * Server started, Redis version 2.2.12
    [1] 24 Apr 03:24:08 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix     this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
    [1] 24 Apr 03:24:08 * The server is now ready to accept connections on port 6379
    [1] 24 Apr 03:24:08 - 0 clients connected (0 slaves), 790664 bytes in use



##Container Linking##

Here is a simple example of container linking. First fire up redis with desired options, here I will be using debug logging.

```
james@ubuntu:~$ docker run -P --name redis -e LOGLEVEL=debug jamesbrink/redis
```

    james@ubuntu:~$ docker run -P --name redis -e LOGLEVEL=debug jamesbrink/redis
    ================================================================================
    Altering coniguration using the following settings:
    ================================================================================
    timeout value: 300
    loglevel value: debug
    databases value: 16
    rdbcompression value: yes
    dbfilename value: dump.rdb
    appendonly value: no
    appendfsync value: everysec
    no-append-fsync-on-rewrite value: no
    vm-enabled value: no
    vm-max-memory value: 0
    vm-page-size value: 32
    vm-pages value: 134217728
    vm-max-threads value: 4
    hash-max-zipmap-entries value: 512
    hash-max-zipmap-value value: 64
    list-max-zipmap-entries value: 512
    list-max-zipmap-value value: 64
    set-max-intset-entries value: 512
    activerehashing value: yes
    ================================================================================
    Configuration updated
    ================================================================================
    [1] 24 Apr 03:24:08 * Server started, Redis version 2.2.12
    [1] 24 Apr 03:24:08 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix     this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
    [1] 24 Apr 03:24:08 * The server is now ready to accept connections on port 6379
    [1] 24 Apr 03:24:08 - 0 clients connected (0 slaves), 790664 bytes in use
    ....
    
    
Now that we have redis up and running, lets link it in to a new container using the alias `redis`

```
james@ubuntu:~/repositories/docker-redis$ docker run -i -t --link redis:redis ubuntu bash
```

You can see below that all of the configured options are available as ENV variables

    james@ubuntu:~/repositories/docker-redis$ docker run -i -t --link redis:redis ubuntu bash
    root@685dbc559232:/# env
    REDIS_PORT_6379_TCP_PROTO=tcp
    REDIS_ENV_HASH-MAX-ZIPMAP-VALUE=64
    HOSTNAME=685dbc559232
    REDIS_ENV_LOGLEVEL=debug
    REDIS_ENV_RDBCOMPRESSION=yes
    TERM=xterm
    REDIS_ENV_DBFILENAME=dump.rdb
    REDIS_NAME=/romantic_shockley/redis
    REDIS_ENV_LIST-MAX-ZIPMAP-ENTRIES=512
    REDIS_PORT_6379_TCP_ADDR=172.17.0.9
    REDIS_ENV_DATABASES=16
    REDIS_ENV_NO-APPEND-FSYNC-ON-REWRITE=no
    REDIS_PORT_6379_TCP_PORT=6379
    REDIS_ENV_LIST-MAX-ZIPMAP-VALUE=64
    REDIS_ENV_TIMEOUT=300
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    REDIS_ENV_VM-ENABLED=no
    PWD=/
    REDIS_ENV_SET-MAX-INTSET-ENTRIES=512
    REDIS_ENV_VM-PAGES=134217728
    REDIS_PORT_6379_TCP=tcp://172.17.0.9:6379
    REDIS_ENV_ACTIVEREHASHING=yes
    REDIS_ENV_HASH-MAX-ZIPMAP-ENTRIES=512
    REDIS_ENV_VM-MAX-MEMORY=0
    SHLVL=1
    REDIS_PORT=tcp://172.17.0.9:6379
    HOME=/
    REDIS_ENV_VM-MAX-THREADS=4
    REDIS_ENV_APPENDONLY=no
    REDIS_ENV_VM-PAGE-SIZE=32
    REDIS_ENV_APPENDFSYNC=everysec
    _=/usr/bin/env

    
So now we can connect to the redis host like so (Make sure to install the redis-cli, on Ububtu use apt-get install redis-server. There is no standard cli package on Ubuntu).

    root@685dbc559232:/# redis-cli -h $REDIS_PORT_6379_TCP_ADDR
    redis 172.17.0.9:6379> set myname james
    OK
    redis 172.17.0.9:6379> get myname
    "james"
    
    
If you look at the output of the redis container you will also see something like the following.

    [1] 24 Apr 03:50:03 - Accepted 172.17.0.10:35526
    [1] 24 Apr 03:50:07 - 1 clients connected (0 slaves), 798768 bytes in use
    [1] 24 Apr 03:50:57 * 1 changes in 900 seconds. Saving...
    [1] 24 Apr 03:50:57 * Background saving started by pid 8
    [8] 24 Apr 03:50:57 * DB saved on disk
    [1] 24 Apr 03:50:58 * Background saving terminated with success
    [1] 24 Apr 03:50:58 - DB 0: 1 keys (0 volatile) in 4 slots HT.
    [1] 24 Apr 03:50:58 - 1 clients connected (0 slaves), 799016 bytes in use
    


##Environment Variables##
Below are the avaiable variables that can be set. Each section lists the default values - `VARIABLE_NAME=default_value`. These settings can be set at runtime, and are optional.


####TIMEOUT####
`TIMEOUT=300`

Close the connection after a client is idle for N seconds (0 to disable).


####LOGLEVEL####
`LOGLEVEL=notice`

Set server verbosity. The following options are available:

* `debug` A lot of information, useful for development/testing.
* `verbose` Many rarely useful info, but not a mess like the debug level.
* `notice` Moderately verbose, what you want in production probably.
* `warning` Only very important / critical messages are logged.


####DATABASES####
`DATABASES=16`

Set the number of databases. The default database is DB 0, you can select a different one on a per-connection basis using SELECT <dbid> where dbid is a number between 0 and 'databases'-1.


####RDBCOMPRESSION####
`RDBCOMPRESSION=yes`

Compress string objects using LZF when dump .rdb databases? For default that's set to 'yes' as it's almost always a win. If you want to save some CPU in the saving child set it to 'no' but the dataset will likely be bigger if you have compressible values or keys.


####DBFILENAME####
`DBFILENAME=dump.rdb`

The filename where to dump the DB


####APPENDONLY####
`APPENDONLY=no`

By default Redis asynchronously dumps the dataset on disk. If you can live with the idea that the latest records will be lost if something like a crash happens this is the preferred way to run Redis. If instead you care a lot about your data and don't want to that a single record can get lost you should enable the append only mode: when this mode is enabled Redis will append every write operation received in the file appendonly.aof. This file will be read on startup in order to rebuild the full dataset in memory. Note that you can have both the async dumps and the append only file if you like (you have to comment the "save" statements above to disable the dumps). Still if append only mode is enabled Redis will load the data from the log file at startup ignoring the dump.rdb file.


**IMPORTANT:** Check the BGREWRITEAOF to check how to rewrite the append log file in background when it gets too big.


####APPENDFSYNC####
`APPENDFSYNC=everysec`

The fsync() call tells the Operating System to actually write data on disk instead to wait for more data in the output buffer. Some OS will really flush data on disk, some other OS will just try to do it ASAP.

Redis supports three different modes:


* `no` Don't fsync, just let the OS flush the data when it wants. Faster.
* `always` Fsync after every write to the append only log . Slow, Safest.
* `everysec` Fsync only if one second passed since the last fsync. Compromise.


The default is "everysec" that's usually the right compromise between speed and data safety. It's up to you to understand if you can relax this to "no" that will will let the operating system flush the output buffer when it wants, for better performances (but if you can live with the idea of some data loss consider the default persistence mode that's snapshotting), or on the contrary, use "always" that's very slow but a bit safer than everysec.


If unsure, use "everysec".


####NO-APPEND-FSYNC-ON-REWRITE####
`NO-APPEND-FSYNC-ON-REWRITE=no`

When the AOF fsync policy is set to always or everysec, and a background saving process (a background save or AOF log background rewriting) is performing a lot of I/O against the disk, in some Linux configurations Redis may block too long on the fsync() call. Note that there is no fix for this currently, as even performing fsync in a different thread will block our synchronous write(2) call.

In order to mitigate this problem it's possible to use the following option that will prevent fsync() from being called in the main process while a BGSAVE or BGREWRITEAOF is in progress.

This means that while another child is saving the durability of Redis is the same as "appendfsync none", that in pratical terms means that it is possible to lost up to 30 seconds of log in the worst scenario (with the default Linux settings).

If you have latency problems turn this to `yes`. Otherwise leave it as `no` that is the safest pick from the point of view of durability.


####VM-ENABLED####
`VM-ENABLED=no`

Virtual Memory allows Redis to work with datasets bigger than the actual amount of RAM needed to hold the whole dataset in memory. In order to do so very used keys are taken in memory while the other keys are swapped into a swap file, similarly to what operating systems do with memory pages.

To enable VM just set 'vm-enabled' to yes, and set the following three VM parameters accordingly to your needs.


####VM-MAX-MEMORY####
`VM-MAX-MEMORY=0`

vm-max-memory configures the VM to use at max the specified amount of RAM. Everything that deos not fit will be swapped on disk *if* possible, that is, if there is still enough contiguous space in the swap file.

With vm-max-memory 0 the system will swap everything it can. Not a good default, just specify the max amount of RAM you can in bytes, but it's better to leave some margin. For instance specify an amount of RAM that's more or less between 60 and 80% of your free RAM.


####VM-PAGE-SIZE####
`VM-PAGE-SIZE=32`

Redis swap files is split into pages. An object can be saved using multiple contiguous pages, but pages can't be shared between different objects. So if your page is too big, small objects swapped out on disk will waste a lot of space. If you page is too small, there is less space in the swap file (assuming you configured the same number of total swap file pages).

If you use a lot of small objects, use a page size of 64 or 32 bytes. If you use a lot of big objects, use a bigger page size. If unsure, use the default :)


####VM-PAGES####
`VM-PAGES=134217728`

Number of total memory pages in the swap file.

Given that the page table (a bitmap of free/used pages) is taken in memory, every 8 pages on disk will consume 1 byte of RAM.

The total swap size is vm-page-size * vm-pages

With the default of 32-bytes memory pages and 134217728 pages Redis will use a 4 GB swap file, that will use 16 MB of RAM for the page table.

It's better to use the smallest acceptable value for your application, but the default is large in order to work in most conditions.


####VM-MAX-THREADS####
`VM-MAX-THREADS=4`

Max number of VM I/O threads running at the same time.

This threads are used to read/write data from/to swap file, since they also encode and decode objects from disk to memory or the reverse, a bigger number of threads can help with big objects even if they can't help with I/O itself as the physical device may not be able to couple with many reads/writes operations at the same time.

The special value of `0` turn off threaded I/O and enables the blocking Virtual Memory implementation.


#### HASH-MAX-ZIPMAP-ENTRIES & HASH-MAX-ZIPMAP-VALUE####
`HASH-MAX-ZIPMAP-ENTRIES=512`
`HASH-MAX-ZIPMAP-VALUE=64`

Hashes are encoded in a special way (much more memory efficient) when they have at max a given numer of elements, and the biggest element does not exceed a given threshold.


####LIST-MAX-ZIPMAP-ENTRIES & LIST-MAX-ZIPMAP-VALUE####
`LIST-MAX-ZIPMAP-ENTRIES=512`
`LIST-MAX-ZIPMAP-VALUE=64`

Similarly to hashes, small lists are also encoded in a special way in order to save a lot of space.


####SET-MAX-INTSET-ENTRIES####
`SET-MAX-INTSET-ENTRIES=512`

Sets have a special encoding in just one case: when a set is composed of just strings that happens to be integers in radix 10 in the range of 64 bit signed integers. This configuration setting sets the limit in the size of the set in order to use this special memory saving encoding.


####ACTIVEREHASHING####
`ACTIVEREHASHING=yes`

Active rehashing uses 1 millisecond every 100 milliseconds of CPU time in order to help rehashing the main Redis hash table (the one mapping top-level keys to values). The hash table implementation redis uses (see dict.c) performs a lazy rehashing: the more operation you run into an hash table that is rhashing, the more rehashing "steps" are performed, so if the server is idle the rehashing is never complete and some more memory is used by the hash table.
 
The default is to use this millisecond 10 times every second in order to active rehashing the main dictionaries, freeing memory when possible.

If unsure: 

use `ACTIVEREHASHING=no` if you have hard latency requirements and it is not a good thing in your environment that Redis can reply form time to time to queries with 2 milliseconds delay.


##TODO##

Not all configuration options are available at this time.

* Snapshoting options
* Replication options
* Security options
* Limits options
* Setup Data Volume
