# Using Video Onboard

In normal operation, the GoPro video device (`/dev/video0`) is acquired exclusively by Solo's video encoder (referred to as _Sculpture_). To gain access to the video device, we need to reconfigure Sculpture.

Theory: We will attach an intermediary gstreamer pipeline to `/dev/video0`.  Then we will pipe that info into two virtual devices, `/dev/video1` and `/dev/video2`.  We will instruct Sculpture to attach to `/dev/video1`, leaving device `/dev/video2` to use as we please.

There are two pieces of software that are needed in order for this to work.  The first is `gst-plugins-good-video4linux2`.  This allows us to use `v4l2sink` with gstreamer.  The other part of that is install a kernel module called `v4l2loopback`.  This allows us to emulate a video device.  After placing the kernel module in `/lib/modules/$(uname -r)/extra/`, run `depmod -a`.

## Steps to Enable Multiple Video Outputs

Modify `/usr/bin/video_send.sh` line 88 from `-g 0` to `-g 1`.  This will tell sculpture to use `/dev/video1`. Reboot.

`modprobe v4l2loopback video_nr=1,2` will load the kernel module that we need and will start the fake video devices.

Now just run this gstreamer pipeline:

```
gst-launch tvsrc ! tee name=vid \
vid. ! queue ! v4l2sink device=/dev/video1 \
vid. ! queue ! v4l2sink device=/dev/video2
```

Voila! Sculpture will resume transmitting video, and `/dev/video2` is available for scripts.
