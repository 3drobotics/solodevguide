# Creating a Service

After Linux is instantiated, Solo launches a group of services that fulfill various roles. These include communication proxying, RSSI testing, video encoding, and the state manager for running Smart Shots and communicating with the Solo app. These services are considered "always on" during normal operation of Solo, and are restarted if they happen to crash or shut down.

You want to create a service if you want to talk to Solo's autopilot, log information while flying, set up a server for routing data, creating a new video output, etc. We'll first describe how services are implemented, then how to add your own to run on boot.

## Disabling Services

Disabling services is ideal when reconfiguring the system or installing packages, when you don't want Solo to arm or communicate aside from over SSH.

Linux has a concept of "run levels" to express states like "shutting down" (runlevel 6). It leaves run levels 2-5 defined for normal operation. Solo by default boots into runlevel 4, which enables multi-user login and launches all of the services mentioned above. At any time, you can change into runlevel 3, which runs the Linux environment but disables these services. To switch into runlevel 3, type in your shell:

```
init 3
```

Typing this, you should hear Solo make a "disconnected" sound and its lights start flashing red. This means that communication to Controller via services are disabled, but note that you can still use SSH and all other functions continue to work. To re-enable services:

```
init 4
```

Solo should immediately reconnect, as though you had just turned on the Controller.

## Adding a new Service

To add a service, we first want to configure a more flexible way of packaging your code. (**NOTE:** In the future, we may ship this configuration by default.)

### Installing runit

We are going to use `runit` as our launch system. Save this file as `/sbin/solo-services-start`:

```
#!/bin/sh

PATH=/usr/local/bin:/usr/local/sbin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/X11R6/bin

exec env - PATH=$PATH \
runsvdir -P /etc/solo-services "log: $(printf '.%.0s' {1..395})"
```

Then run:

```
chmod +x /sbin/solo-services-start
mkdir -p /etc/solo-services
```

Add this line to your inittab:

```
SSS:4:respawn:/sbin/solo-services-start
```

Then type:

```
init q
```

### Adding a new service

We're going to add a web server to Solo.

```
mkdir -p /etc/solo-services/webserver/static
echo $'#!/bin/bash\npython -m SimpleHTTPServer -p 8000\n' > /etc/solo-services/webserver/run
chmod +x /etc/solo-services/run
echo $'<h1>Hello world!</h1>' < /etc/solo-services/webserver/static/index.html
```

After ~5 seconds, `runit` will pick up this service and launch it. Go to <http://10.1.1.10:8000/> and see your service running.

(TODO: Kill the service, see it restart)
