# Utilities

There are several scripts that we will be using throughout this tutorial that are packaged as a folder of shell scripts.

* Resizing the root partition.
* Installing `runit` to manage start processes.
* Providing access to the video stream.
* Tunnelling to the Internet through your host.

## Installing `sdg`

Clone this guide:

```
git clone https://github.com/3drobotics/solodevguide
```

You can install the tools from here:

```
./solodevguide/tools/install.sh
```

## Connecting to the Internet

```
sdg tunnel-start
```

```
sdg tunnel-stop
```

## Installing `runit`

```
sdg install-runit
```

## Expanding the Root Partition

```
sdg resize-fs
```

Resizes to ~90mb.
