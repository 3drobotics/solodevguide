# Development Tools ("solo-utils")

The `solo-utils` tools perform several tasks that are essential for development on Solo. These include:

* Enabling direct Internet access from Solo through the host (required to install packages on Solo).
* Resizing the root partition.
* Installing `runit` (which manages automatic process execution).
* Providing access to the video stream.


## Installing solo-utils

To install `solo-utils` onto Solo, your host PC must be running OS X or Linux and be connected to both Solo and the Internet. 
<aside class="note">
* The installation need only be performed once, though you can repeat the process in case of failure or if you wish to update your utils.
* Connect the host computer to the Internet using an Ethernet cable or other spare network adapter (your wifi adapter will be attached to the Solo network!) 
</aside>

Run this command on your *host* computer:

<div class="host-code"></div>

```sh
curl -fsSL -H "Accept: application/vnd.github.raw" https://api.github.com/repos/3drobotics/solodevguide/contents/tools/install-solo-utils.sh | sh
```

A successful install will resemble the following output:

<div class="host-code"></div>

```
checking for sshuttle....
checking for solo-utils...
checking rpms...
checking for sv...
checking for parted...
checking for resize2fs...
checking for resize2fs...
checking for resize2fs...
checking for mkfs.ext3...
checking for lsof...
done. solo-utils is installed and up to date.
```

## Running solo-utils

The `solo-utils` are run from the Solo terminal. Instructions on how to set up an SSH session with Solo are provided in [Accessing Solo](starting-network.html).

<aside class="note">
You should [connect to the Internet](#connecting-to-the-internet) and call `smart update` before [configuring other tools](#configure-tools) and [resizing the partition](#expanding-the-root-partition).
</aside>

Specific examples of how the utils are called are given in the following sections.


## Connecting to the Internet

<aside class="note">
* If you are on OS X, you must first [enable remote sharing](https://support.apple.com/kb/PH13759?locale=en_US). If you are on Windows, you will need to install an SSH server.
* Connect the host computer to the Internet using an Ethernet cable or other spare network adapter (your wifi adapter will be attached to the Solo network!) 
</aside>


Follow the prompts on first initialization to create a reverse SSH tunnel to your host computer, enabling direct Internet access from Solo:

```
solo-utils tunnel-start
smart update
```

You can disable this tunnel by restarting Solo or running:

```
solo-utils tunnel-stop
```

<aside class="tip">
Enabling the tunnel is a prerequisite for [installing software packages](starting-installing.html#installing-packages) on Solo using *smart*.
</aside>



## Configure Tools

This section shows how to call the `solo-utils` to install other important development tools.  You must first connect to the Internet, as demonstrated in the previous section.


### Install runit

To add the *runit* script daemon (used to create new services):

```
solo-utils install-runit
```

### Install pip

To install `pip` directly on Solo:

```
solo-utils install-pip
```



## Expanding the Root Partition

Solo minimizes the root partition size in order to maximize the space available for logs. In order to install more packages you will need to use the `resize-fs` option to expand the root partition from 90Mb to 250Mb.

<aside class="tip">
Resizing the partition will delete and recreate your `/log` directory. Ensure you have any important data backed up first! 
</aside>

To expand the root partition run:

```
solo-utils resize-fs
```

You will have to physically reboot (power cycle) your drone after the script is complete.

<aside class="warning">
Resizing the partition may occasionally fail. The solution is simply to re-run `solo-utils resize-fs`. 
</aside>

