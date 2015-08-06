# solodevguide

<!--TOC-->
Table of Contents:

1. [Overview](#overview)
1. [Getting Started](#getting-started)
1. [Solo's Network](#solo-s-network)
1. [Factory Reset](#factory-reset)
1. [(Advanced) Linux Distribution](#advanced-linux-distribution)
1. [License](#license)

<!--/TOC-->

## Overview

Solo is a Linux system (iMX.6 running Yocto Linux) connected to a Pixhawk autopilot.

The Pixhawk controls flight modes, stabilization, and recovery in the case of an RTL event (return-to-launch). Pixhawk comminicates over the MAVLink telemetry protocol to both the onboard Linux computer and downstream devices like the Controller and mobile phone Solo apps.

The Linux system controls high-level operation of the copter: smart shots, camera and gimbal control, mobile app communication, and accessory interaction are all implemented on this layer.

## Getting Started

Development for Solo encompasses both externally interfacing to Solo (for a mobile app, ground control station, or API) and controlling the onboard computer. To begin, let's look at gaining control of Solo's shell console over SSH..

**NOTE:** We advise that you connect your computer to the Internet via ethernet while developing for Solo. When paired with Solo's WiFi network, you will not be able to access any webpages over your WiFi connection.

Power your Controller and your Solo. Connect your computer to Solo's Wifi network using the password for your given network.

## Solo's Network

**TODO:** Here we describe how Solo's internal network looks like.

| Host | IP |
|------|----|
| Solo | 10.1.1.10 |
| Controller | 10.1.1.1 |

### Default Wi-Fi password:

sololink

### SSH

**Solo:**

```
ssh root@10.1.1.10
```

**Controller:**

```
ssh root@10.1.1.1
```

### Default root password

TjSDBkAu

### Password-less access

We recomend you copy your public key to Solo and Controller for a better SSH experience

```bash
ssh-copy-id -i ~/.ssh/id_rsa root@10.1.1.10
````

You can optimize this process by adding the following to your .ssh/config file

```
Host solo 10.1.1.10
    Hostname 10.1.1.10
    Port 22
    User root
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
    IdentityFile ~/.ssh/id_rsa
```

**Note:** OS X doesn't ship with `ssh-copy-id`, you can easily get it with [Homebrew](http://brew.sh/)

```bash
brew install ssh-copy-id
```

## Factory Reset

To factory reset your Solo to "Gold Master", follow the [Factory Reset Procedure](http://3drobotics.com/kb/factory-reset/).

**NOTE:** We are working on a programmatic way to [reflash Solo and the Controller](https://github.com/3drobotics/solodevguide/issues/5).


## (Advanced) Linux Distribution

The linux distribution used is 3DR Poky (based on Yocto Project Reference Distro)
Documentation: http://www.yoctoproject.org/docs/1.8/mega-manual/mega-manual.html

```
# uname -a
Linux 3dr_solo 3.10.17-rt12-1.0.0_ga+g3f15a11 #3 SMP PREEMPT Thu Jun 4 04:07:49 UTC 2015 armv7l GNU/Linux
```

```
# cat /etc/issue
3DR Poky (based on Yocto Project Reference Distro) 1.5.1 \n \l
```

Yocto has a package manager "smart" that can be used to download packages if Solo is connected to the Internet.

## License

This document is Copyright &copy; 2015 3DRobotics.
