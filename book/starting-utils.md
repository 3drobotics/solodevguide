# "solo" Command Line Tool

The *Solo CLI* tool performs several tasks that are essential for development on Solo. These include:

* Enabling simultaneous WiFi access to Solo and the Internet
* Resizing the root partition
* Installing `runit`, `pip`, and `smart` packages
* Providing access to the video stream
* Updating the firmware on Solo and the Controller
* Downloading logs


## Installing *Solo CLI*

*Solo CLI* is a command line application you install to your PC. This application can control Solo and the Controller when connected to their WiFi network. You will need *Python* and *pip* installed in order to run this utility.

First connect to a WiFi network with Internet access. Run this command on your PC:

<div class="host-code"></div>

```sh
pip install -UI git+https://github.com/3drobotics/solo-cli
```

<aside class="note">
On OS X and Linux, you may need to run the command as root, i.e. `sudo -H pip install -UI git+https://github.com/3drobotics/solo-cli`.
</aside>

Once installed, you should be able to run `solo` from your command line to see the list of available options. For example:

<div class="host-code"></div>

```sh
$ solo
Usage:
  solo info
  solo wifi --name=<n> --password=<p>
  solo update (solo|controller|both) (latest|<version>)
  solo revert (solo|controller|both) (latest|current|factory|<version>)
  solo provision
  solo resize
  solo logs (download)
  solo install-pip
  solo install-smart
  solo install-runit
  solo video (acquire|restore)
```

Specific information about what these commands do is given in the following sections and on the [*Solo CLI* README](https://github.com/3drobotics/solo-cli).


## Connecting Solo to the Internet

The `solo wifi` command connects your Controller to a local WiFi network. Solo uses this connection (via the Controller network) to access the Internet during development and to [download and install packages](starting-installing.html#installing-packages).

<aside class="tip">The development PC still connects to Solo and the Controller by their dedicated IP addresses on the Controller Network (`10.1.1.1` and `10.1.1.10`) rather than the IP of the Controller on your local WiFi network.

The Controller provides Internet access to the connected PC. This is useful if the PC WiFi connection is normally used to access the local network.</aside>

The steps for using the command are:

* [Connect your PC to the Controller's WiFi network](starting-network.html).
* Run the following command from your PC's command line:
  <div class="host-code"></div>

  ```sh
  solo wifi --name=<ssid> --password=<password>
  ```
  The SSID and password should be those of a local WiFi network, i.e. that of your home or your office.
* You may need to disconnect and reconnect your PC to Solo's WiFi network in order enable Internet access (you can verify the PC connection by opening up a web browser and accessing any web page).

<aside class="tip">
You will (for now) need to run this command each time the Controller is reset. It is safe to run this command multiple times in one session.
</aside>




## Installation

This section demonstrates how to install various development tools using *Solo CLI*. You must first connect to the Internet, as shown in the previous section.

### Install *smart* repositories

*smart* is the Solo package manager (see the [Installing Packages section](starting-installing.html#installing-packages) for more information). To install the list of repositories needed by *smart*, run:

<div class="host-code"></div>

```
solo install-smart
``` 

### Install runit

To add the *runit* script daemon (used to create new services):

<div class="host-code"></div>

```
solo install-runit
```

### Install pip

To install `pip` directly on Solo:

<div class="host-code"></div>

```
solo install-pip
```


## Expanding the Root Partition

Solo splits its available space between a "root" partition for code and a "logs" partition. In production, the root partition on Solo is fairly small in order to maximize the space available for logs. When installing many packages or code samples, you can quickly reach the limits of space on this partition.

You can use the `solo resize` option to expand the root partition from its default of 90Mb to ~600Mb.

<aside class="tip">
Resizing the partition will delete and recreate your `/log` directory. Ensure you have any important data backed up first! 
</aside>

To expand the root partition run:

<div class="host-code"></div>

```
solo resize
```

You may have to physically reboot (power cycle) your drone after the script is complete.

<aside class="warning">
Resizing the partition may occasionally fail ([bug #5](https://github.com/3drobotics/solo-cli/issues/5)). You can see this by running `df -h` on Solo and seeing if the root partition is resized, or if there is no longer a `/log` partition. The solution is simply to re-run `solo resize`. 
</aside>

