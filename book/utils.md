# Utilities

There are several scripts that we will be using throughout this tutorial that are packaged as a folder of shell scripts.

* Resizing the root partition.
* Installing `runit` to manage start processes.
* Providing access to the video stream.
* Tunnelling to the Internet through your host.

## Installing `solo-utils`

Run this command on your *host* computer:

```sh
curl -fsSL -H "Accept: application/vnd.github.raw" https://bc0a42b65800ec0dd4c9127dde0cd6e98eb70012:x-oauth-basic@api.github.com/repos/3drobotics/solodevguide/contents/tools/install-solo-utils.sh | sh
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

### Optional Installs

To add the init script daemon:

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

## Expanding the Root Partition

To expand the root partition from 90Mb to 250Mb, you will delete and recreate your `/log` directory. Ensure you have any important data backed up. Then run:

```
solo-utils resize-fs
```

You will have to physically reboot (power cycle) your drone after the script is complete.
