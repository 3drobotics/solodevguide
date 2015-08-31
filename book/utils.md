# Utilities

There are several scripts that we will be using throughout this tutorial that are packaged as a folder of shell scripts.

* Resizing the root partition.
* Installing `runit` to manage start processes.
* Providing access to the video stream.
* Tunnelling to the Internet through your host.

## Installing `sdg`

Run this command on your *host* computer:

```
curl -fsSL -H "Accept: application/vnd.github.raw" https://bc0a42b65800ec0dd4c9127dde0cd6e98eb70012:x-oauth-basic@api.github.com/repos/3drobotics/solodevguide/contents/tools/install.sh | sh
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

Then run:

```
sdg install-runit
```

## Connecting to the Internet

```
sdg tunnel-start
```

```
sdg tunnel-stop
```

## Expanding the Root Partition

You'll need a few extra packages for this:

```
sdg resize-fs
```

Resizes to ~90mb.
