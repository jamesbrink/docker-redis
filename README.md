docker-redis
============

A docker container running Redis

WIP



##Environment Variables##
Below are the avaiable variables that can be set. Each section lists **`VARIABLE_NAME : DEFAULT_VALUE`**. These settings can be set at runtime, and are optional.

**`TIMEOUT` : `300`**

Close the connection after a client is idle for N seconds (0 to disable).

**`LOGLEVEL` : `notice`**

Set server verbosity.
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


* `APPENDFSYNC`: default:`everysec`
* `NO-APPEND-FSYNC-ON-REWRITE`: default:`no`
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
