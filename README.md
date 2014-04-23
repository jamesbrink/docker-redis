docker-redis
============

A docker container running Redis

WIP



##Environment Variables##


* `TIMEOUT`: Close the connection after a client is idle for N seconds (0 to disable). default: `300`
* `LOGLEVEL`: Set server verbosity. default: `notice`
    * `debug` A lot of information, useful for development/testing.
    * `verbose` Many rarely useful info, but not a mess like the debug level.
    * `notice` Moderately verbose, what you want in production probably.
    * `warning` Only very important / critical messages are logged.
* `DATABASES`: Set the number of databases. The default database is DB 0, you can select a different one on a per-connection basis using SELECT <dbid> where dbid is a number between 0 and 'databases'-1. default: `16`
* `RDBCOMPRESSION`: Compress string objects using LZF when dump .rdb databases? For default that's set to 'yes' as it's almost always a win. If you want to save some CPU in the saving child set it to 'no' but the dataset will likely be bigger if you have compressible values or keys. default: `yes`
* `DBFILENAME`: default: `dump.rdb`
* `APPENDONLY`: default:`no`
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
