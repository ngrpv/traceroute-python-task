# Traceroute (+country, provider, autonomous system number)

## CLI Usage:

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

## Web interface usage:

### Install dependencies: `pip install flask pytest`
### Run it as root in project directory: `FLASK_APP=app flask run`
Actually, you can run it as you want as flask allows to, but let's suppose you would be satisfied with flask test server.
Also it's not neccessary to run it as root - you just need to grant ICMP usage rights to user server runs by

In this case, a web interface would be available at http://localhost:5000/

It has quite poor visual, but easy to undestand and has AJAX "fat" web interace logic.

Type desired host and scan limitations and there you go.

If server cannot resolve host, you'll be notified with corresponding alert.

Otherwise, a scan view will appear and you'll see routers the packet reaches.
This list is built dynamically at server side and client retrieves it dynamically too until server finish current scanning job.

At any moment of scanning process you may return to new scan task view by pressing corresponding button right under the view header.

## Tests coverage

* app.py 100% coverage
* trace.py 80% coverage
