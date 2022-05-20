# Traceroute (+country, provider, autonomous system number)

## Usage:

1. Linux(on Windows may be troubles with ttl):
   > You should use "sudo"

```
usage: Tracer with detecting country, autonomous system and provider [-h] [-t TIMEOUT] [-m MAX_HOPS]

options:
  -h, --help            show this help message and exit
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout for ping (ms)
  -m MAX_HOPS, --max-hops MAX_HOPS
                        Max count of hops
```

   ```
   [user@user]$ sudo python trace.py -t 500 -m 25
    ip or domain:
    google.com
    tracing: 108.177.14.100
    ...
   ```

![](Screenshot_20220408_190113.png)