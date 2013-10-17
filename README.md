ganglia-redis-llen
==================

Plugin for ganglia to monitor Redis list sizes

This plugins allows you to monitor the size of a group os lists optionaly on multiple databases

## How to Install

Place `redis-gmond-llen.py` and `redis-gmond-llen.py.pyconf` in the appropriate directories and restart `gmond`:

* copy `conf.d/redis-gmond-llen.pyconf` to `/etc/ganglia/conf.d`
* copy `conf.d/redis-gmond-llen.pyconf` to `/usr/lib/ganglia/python_modules` (32bis) or `/usr/lib64/ganglia/python_modules` (64bits)

## How to configure

To configure the plugin edit the file and change the values of the paramether described bellow:

```
modules {
  module {
    name = "redis-gmond-llen"
    language = "python"
    param host { value = "127.0.0.1" }
    param port { value = 6379 }
    param databases { value = "0, 1" }
    param lists { value = "listA, listB, listC" }
  }
}
```

### ```param``` meaning and default values:


* __host__: the host where the redis server is running (default: 127.0.0.1)
* __port__: The port where the redis server is running (default: 6379)
* __database__: The database that will be queried for the lists (default: 0)
* __lists__: the lists that we want to monitor

## AUTHOR

Ricardo Melo <rjsmelo@gmail.com>
