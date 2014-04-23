docker-redis
============

A docker container running Redis

WIP



##Environment Variables##
Below are the avaiable variables that can be set. Each section lists **`VARIABLE_NAME : DEFAULT_VALUE`**. These settings can be set at runtime, and are optional.

**`TIMEOUT` : `300`**

Close the connection after a client is idle for N seconds (0 to disable).

**`LOGLEVEL` : `notice`**

Set server verbosity. The following options are available:

* `debug` A lot of information, useful for development/testing.
* `verbose` Many rarely useful info, but not a mess like the debug level.
* `notice` Moderately verbose, what you want in production probably.
* `warning` Only very important / critical messages are logged.
    
**`DATABASES` : `16`**

Set the number of databases. The default database is DB 0, you can select a different one on a per-connection basis using SELECT <dbid> where dbid is a number between 0 and 'databases'-1.


**`RDBCOMPRESSION` : `yes`**

Compress string objects using LZF when dump .rdb databases? For default that's set to 'yes' as it's almost always a win. If you want to save some CPU in the saving child set it to 'no' but the dataset will likely be bigger if you have compressible values or keys.


**`DBFILENAME` : `dump.rdb`**

The filename where to dump the DB


**`APPENDONLY` : `no`**

By default Redis asynchronously dumps the dataset on disk. If you can live with the idea that the latest records will be lost if something like a crash happens this is the preferred way to run Redis. If instead you care a lot about your data and don't want to that a single record can get lost you should enable the append only mode: when this mode is enabled Redis will append every write operation received in the file appendonly.aof. This file will be read on startup in order to rebuild the full dataset in memory. Note that you can have both the async dumps and the append only file if you like (you have to comment the "save" statements above to disable the dumps). Still if append only mode is enabled Redis will load the data from the log file at startup ignoring the dump.rdb file.


**IMPORTANT:** Check the BGREWRITEAOF to check how to rewrite the append log file in background when it gets too big.


**`APPENDFSYNC` : `everysec`**

The fsync() call tells the Operating System to actually write data on disk instead to wait for more data in the output buffer. Some OS will really flush data on disk, some other OS will just try to do it ASAP.

Redis supports three different modes:


* `no` Don't fsync, just let the OS flush the data when it wants. Faster.
* `always` Fsync after every write to the append only log . Slow, Safest.
* `everysec` Fsync only if one second passed since the last fsync. Compromise.


The default is "everysec" that's usually the right compromise between speed and data safety. It's up to you to understand if you can relax this to "no" that will will let the operating system flush the output buffer when it wants, for better performances (but if you can live with the idea of some data loss consider the default persistence mode that's snapshotting), or on the contrary, use "always" that's very slow but a bit safer than everysec.


If unsure, use "everysec".


**`NO-APPEND-FSYNC-ON-REWRITE` : `no`**

When the AOF fsync policy is set to always or everysec, and a background saving process (a background save or AOF log background rewriting) is performing a lot of I/O against the disk, in some Linux configurations Redis may block too long on the fsync() call. Note that there is no fix for this currently, as even performing fsync in a different thread will block our synchronous write(2) call.

In order to mitigate this problem it's possible to use the following option that will prevent fsync() from being called in the main process while a BGSAVE or BGREWRITEAOF is in progress.

This means that while another child is saving the durability of Redis is the same as "appendfsync none", that in pratical terms means that it is possible to lost up to 30 seconds of log in the worst scenario (with the default Linux settings).

If you have latency problems turn this to "yes". Otherwise leave it as "no" that is the safest pick from the point of view of durability.


* `VM-ENABLED`: default:`no`
* `VM-MAX-MEMORY`: default:`0`
* `VM-PAGE-SIZE`: default:`32`
* `VM-PAGES`: default:`134217728`
* `VM-MAX-THREADS`: default:`4`
* `HASH-MAX-ZIPMAP-ENTRIES`: default:`512`
* `HASH-MAX-ZIPMAP-VALUE`: default:`64`
* `LIST-MAX-ZIPMAP-ENTRIES`: default:`512`
* `LIST-MAX-ZIPMAP-VALUE`: default: `64`
* `SET-MAX-INTSET-ENTRIES`: default:`512`
* `ACTIVEREHASHING`: default:`yes`
