# Accessing Solo

Solo can be accessed via WiFi. When Solo and its Controller are booted, the Controller creates a private network between the two devices. Any computer or smartphone can connect to this network and access these devices via their IP addresses.

The network assigns particular addresses to the Controller and to Solo. All other devices are assigned within a particular range:

* `10.1.1.1` &mdash; Controller
* `10.1.1.10` &mdash; Solo
* `10.1.1.100`&ndash;`10.1.1.255` &mdash; Computers, phones, or other devices on the network

## Using SSH

SSH is a mechanism to access the shell of another device securely. SSH is the primary mechanism by which you can access Solo's internals. You can SSH into either Solo or the Controller.

<aside class="note">
We do not recommend modifying the Controller. All examples in this guide will be focused exclusively on modifying Solo.
</aside>

To SSH into Solo, you will need an SSH client.

* On Windows, we recommend [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/) or [Cygwin with OpenSSH](http://ftp.perforce.com/perforce/tools/benchmarks/browse/doc/cygwin.html).
* On Linux or OS X, you likely already have OpenSSH installed. Try using the `ssh` tool from your command line.

First, connect to Solo's WiFi network (similar to how you would connect your phone to it via the app). Next, open a terminal and type:

<div class="host-code"></div>

```
ssh root@10.1.1.10
```

This will prompt you for Solo's root password. The default SSH root password on Solo is:

> TjSDBkAu

Your SSH client will then have direct terminal access to Solo.

<aside class="note">
If you receive a 'Host Idenfiication' error, you may have previously SSH'd into a different Solo from the same computer you are currently using. You can delete your leftover SSH keys using the following commands:

```
ssh-keygen -R 10.1.1.10
ssh-keygen -R 10.1.1.1
```
</aside>



### Security

Solo's root SSH password is the same for all devices. We recommend not modifying the SSH password. Instead, improve security on your device by [changing the WiFi SSID and password](https://3drobotics.com/kb/setting-wifi-password/) via the app.
