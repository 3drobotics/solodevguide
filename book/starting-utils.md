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
pip install git+https://github.com/3drobotics/solo-cli
```

<aside class="note">
On OS X and Linux, you may need to run the command as root:
<div class="host-code"></div>

```sh
sudo -H pip install git+https://github.com/3drobotics/solo-cli
```
To upgrade to the latest version, append ``--upgrade`` or ``-U`` to the above command:

<div class="host-code"></div>

```sh
sudo -H pip install -U git+https://github.com/3drobotics/solo-cli
```

</aside>

Once installed, you should be able to run `solo` from your command line to see the list of available options. For example:

<div class="host-code"></div>

```sh
$ solo
Usage:
  solo info
  solo wifi --name=<n> [--password=<p>]
  solo flash (drone|controller|both) (latest|current|factory|<version>) [--clean]
  solo flash --list
  solo flash pixhawk <filename>
  solo provision
  solo resize
  solo logs (download)
  solo install-pip
  solo install-smart
  solo install-runit
  solo video (acquire|restore)
  solo script [<arg>...]
```

Specific information about what these commands do is given in the following sections and on the [*Solo CLI* README](https://github.com/3drobotics/solo-cli).


## Connecting Solo to the Internet

The `solo wifi` command connects your Controller to your home WiFi network. Solo uses this connection (via the Controller network) to access the Internet during development and to [download and install packages](starting-installing.html#installing-packages).

<aside class="tip">The development PC still needs to connect to the Controller's WiFi network and access Solo and the Controller using their dedicated IP addresses (`10.1.1.1` and `10.1.1.10`).

The Controller provides Internet access to the connected PC. This is useful if the PC normally uses Wifi to connect to your home network.
</aside>

The steps for using the command are:

* [Connect your PC to the Controller's WiFi network](starting-network.html).
* Run the following command from your PC's command line:
  <div class="host-code"></div>

  ```sh
  solo wifi --name=<ssid> --password=<password>
  ```
  The SSID and password should be those of a local WiFi network, i.e. that of your home or your office.
  <aside class="tip">
  You will (for now) need to run this command each time the Controller is reset. It is safe to run this command multiple times in one session.
  </aside>
* You may need to disconnect and reconnect your PC to Solo's WiFi network in order enable Internet access (you can verify the PC connection by opening up a web browser and accessing any web page).


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

## Deploying/running DroneKit scripts on Solo

Use the ``solo script pack`` command to package a folder containing DroneKit-Python scripts
and any dependencies into an archive for deployment to Solo.
The host computer must be connected to the Internet, and the folder must contain a
**requirements.txt** file listing
the (PyPi) dependencies:

<div class="host-code"></div>

```
solo script pack
```

If successful, the command will create an archive in the `solo-script.tar.gz` in the current directory.

Deploy this archive to Solo and run a specified script using the ``solo script run <scripname>`` command.
The host computer must be connected to the Solo wifi network, and Solo must also be connected to the
Internet.

For example, to deploy and run the [helloworld example](example-helloworld.html):

<div class="host-code"></div>

```
solo script run helloworld.py
```


## Downloading Logs

To download logs to your host computer:

<div class="host-code"></div>

```
solo logs download
```

Logs are downloaded from both solo and the controller, and copied into subdirectories **./drone** and **./controller** (respectively).


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

