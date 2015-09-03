# Installing "solo-utils"

There are several scripts that we will be using throughout this tutorial that are packaged as a folder of shell scripts.

* Enables direct Internet access from Solo through the host (required to install packages on Solo).
* Resizing the root partition.
* Installing `runit` to manage start processes.
* Providing access to the video stream.


All of these can be performed using the `solo-utils` command. To install, run this command on your *host* computer (you must be running OS X or Linux):

```sh
curl -fsSL -H "Accept: application/vnd.github.raw" https://bc0a42b65800ec0dd4c9127dde0cd6e98eb70012:x-oauth-basic@api.github.com/repos/3drobotics/solodevguide/contents/tools/install-solo-utils.sh | sh
```

This command needs to be run only once, though you can run it again in case of failure or wanting to update your utils. A successful install will resemble the following output:

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

<!--
Clone this guide:

```
git clone https://github.com/3drobotics/solodevguide
```

You can install the tools from here:

```
./solodevguide/tools/install.sh
```
-->

## Configure Tools

To add the *runit* script daemon (used to create new services):

```
solo-utils install-runit
```

To install `pip` directly on Solo:

```
solo-utils install-pip
```

## Connecting to the Internet

Follow the prompts on first initialization to create a reverse SSH tunnel to your host computer, enabling direct Internet access from Solo:

```
solo-utils tunnel-start
```

You can disable this tunnel by restarting Solo or running:

```
solo-utils tunnel-stop
```

<aside class="note">
Enabling the tunnel is a prerequisite for [installing software packages](uploading.html#installing-packages) on Solo using *smart*.
</aside>



## Expanding the Root Partition

To expand the root partition from 90Mb to 250Mb, you will delete and recreate your `/log` directory. Ensure you have any important data backed up. Then run:

```
solo-utils resize-fs
```

You will have to physically reboot (power cycle) your drone after the script is complete.
