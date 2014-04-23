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

If you have latency problems turn this to `yes`. Otherwise leave it as `no` that is the safest pick from the point of view of durability.


**`VM-ENABLED` : `no`**

Virtual Memory allows Redis to work with datasets bigger than the actual amount of RAM needed to hold the whole dataset in memory. In order to do so very used keys are taken in memory while the other keys are swapped into a swap file, similarly to what operating systems do with memory pages.

To enable VM just set 'vm-enabled' to yes, and set the following three VM parameters accordingly to your needs.


**`VM-MAX-MEMORY` : `0`**

vm-max-memory configures the VM to use at max the specified amount of RAM. Everything that deos not fit will be swapped on disk *if* possible, that is, if there is still enough contiguous space in the swap file.

With vm-max-memory 0 the system will swap everything it can. Not a good default, just specify the max amount of RAM you can in bytes, but it's better to leave some margin. For instance specify an amount of RAM that's more or less between 60 and 80% of your free RAM.


**`VM-PAGE-SIZE` : `32`**

Redis swap files is split into pages. An object can be saved using multiple contiguous pages, but pages can't be shared between different objects. So if your page is too big, small objects swapped out on disk will waste a lot of space. If you page is too small, there is less space in the swap file (assuming you configured the same number of total swap file pages).

If you use a lot of small objects, use a page size of 64 or 32 bytes. If you use a lot of big objects, use a bigger page size. If unsure, use the default :)


**`VM-PAGES` : `134217728`**

Number of total memory pages in the swap file.

Given that the page table (a bitmap of free/used pages) is taken in memory, every 8 pages on disk will consume 1 byte of RAM.

The total swap size is vm-page-size * vm-pages

With the default of 32-bytes memory pages and 134217728 pages Redis will use a 4 GB swap file, that will use 16 MB of RAM for the page table.

It's better to use the smallest acceptable value for your application, but the default is large in order to work in most conditions.


**`VM-MAX-THREADS` : `4`**

Max number of VM I/O threads running at the same time.

This threads are used to read/write data from/to swap file, since they also encode and decode objects from disk to memory or the reverse, a bigger number of threads can help with big objects even if they can't help with I/O itself as the physical device may not be able to couple with many reads/writes operations at the same time.

The special value of `0` turn off threaded I/O and enables the blocking Virtual Memory implementation.


**`HASH-MAX-ZIPMAP-ENTRIES` : `512`**
**`HASH-MAX-ZIPMAP-VALUE` : `64`**

Hashes are encoded in a special way (much more memory efficient) when they have at max a given numer of elements, and the biggest element does not exceed a given threshold.

**`LIST-MAX-ZIPMAP-ENTRIES` : `512`**
** `LIST-MAX-ZIPMAP-VALUE` : `64`**

Similarly to hashes, small lists are also encoded in a special way in order to save a lot of space.


**`SET-MAX-INTSET-ENTRIES` : `512`**

Sets have a special encoding in just one case: when a set is composed of just strings that happens to be integers in radix 10 in the range of 64 bit signed integers. This configuration setting sets the limit in the size of the set in order to use this special memory saving encoding.

**`ACTIVEREHASHING` : `yes`**

Active rehashing uses 1 millisecond every 100 milliseconds of CPU time in order to help rehashing the main Redis hash table (the one mapping top-level keys to values). The hash table implementation redis uses (see dict.c) performs a lazy rehashing: the more operation you run into an hash table that is rhashing, the more rehashing "steps" are performed, so if the server is idle the rehashing is never complete and some more memory is used by the hash table.
 
The default is to use this millisecond 10 times every second in order to active rehashing the main dictionaries, freeing memory when possible.

If unsure: 

use "activerehashing no" if you have hard latency requirements and it is not a good thing in your environment that Redis can reply form time to time to queries with 2 milliseconds delay.

