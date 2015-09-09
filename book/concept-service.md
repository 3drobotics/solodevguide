# System Services

After Linux is instantiated, Solo launches a group of services that fulfil various roles. These include communication proxying, RSSI testing, video encoding, and the state manager for running Smart Shots and communicating with the Solo app. These services are considered "always on" during normal operation of Solo, and are restarted if they happen to crash or shut down.

You want to create a service if you want to talk to Solo's autopilot, log information while flying, set up a server for routing data, creating a new video output, etc. We'll first describe how services are implemented, then how to add your own to run on boot.

## Disabling Services

Disabling services is ideal when reconfiguring the system or installing packages, when you don't want Solo to arm or communicate aside from over SSH.

Linux has a concept of "run levels" to express states like "shutting down" (runlevel 6). It leaves run levels 2-5 defined for normal operation. Solo by default boots into runlevel 4, which enables multi-user login and launches all of the services mentioned above. At any time, you can change into runlevel 2, which runs the Linux environment but disables these services. To switch into runlevel 2, type in your shell:

```
init 2
```

Typing this, you should hear Solo make a "disconnected" sound and its lights start flashing red. This means that communication to Controller via services are disabled, but note that you can still use SSH and all other functions continue to work. To re-enable services:

```
init 4
```

Solo should immediately reconnect, as though you had just turned on the Controller.

## Installing `runit`

To add a service, we first want to configure a more flexible way of launching services. For this, we'll use `runit` as our launch system.

[After having installed the `solo-utils` tool](starting-utils.html), from your Solo's shell, run:

```
solo-utils install-runit
```

## Adding a new Service

We're going to add a web server to Solo.

```
mkdir -p /etc/solo-services/webserver/static
cat <<'EOF' | tee /etc/solo-services/webserver/run
#!/bin/bash
cd static && exec python -m SimpleHTTPServer 80
EOF
chmod +x /etc/solo-services/run
echo '<h1>Hello world!</h1>' > /etc/solo-services/webserver/static/index.html
```

After ~5 seconds, `runit` will pick up this service and launch it. Go to <http://10.1.1.10/> and see your service running.

Add more files to `/etc/solo-services/webserver/static` to see them update live. You can replace `python` in the previous example with any script of your choosing.

To see that the service is working, you can even forcibly kill your process:

```
kill -9 $(ps | grep "[S]impleHTTPServer" | awk "{print \$1 }")
```

Refresh your web browser and you will see the service still running.

You can run `sv [start|stop|restart] /etc/solo-services/webserver` to change the state of the service independently of all other services, for example after you make a change to the `run` file.

Why do we use `exec python`? Because the supervisor tracks only the PID of the `run` script when it is launched, if you were to instead run `python`, and the process were stopped, only the bash script would stop. The webserver would keep going! `exec` replaces your current process (the bash script) with the specified process so that it can be killed by a script knowing its PID.

