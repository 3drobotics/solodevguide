# Solo and Video

The Gopro video device (/dev/video0) is used by Sculpture, so we can't actually get access to the video device without disabling sculpture.  To disable sculpture, comment out `VID:4:respawn:video_send.sh` in `inittab`.  In order to get access to a video device without interrupting sculpture, things get complicated.  Read on.

Theory: We will attach a gstreamer pipeline to `/dev/video0`.  Then we will pipe that info into the virtual devices `/dev/video1` and `/dev/video2`.  We will redirect sculpture to latch onto `/dev/video1`.  Now we have the device `/dev/video2` to use as we please.

There are two pieces of software that are needed in order for this to work.  The first is `gst-plugins-good-video4linux2`.  This allows us to use `v4l2sink` with gstreamer.  The other part of that is install a kernel module called v4l2loopback.  This allows us to emulate a video device.  After placing the kernel module in `/lib/modules/$(uname -r)/extra/`, run `depmod -a`.

modify `/usr/bin/video_send.sh`  line 88 from `-g 0` to `-g 1`.  This will tell sculpture to use `/dev/video1`

reboot.

`modprobe v4l2loopback video_nr=1,2` will load the kernel module that we need and will start the fake video devices.

Now just run this gstreamer pipeline:
```
gst-launch tvsrc ! tee name=vid \
vid. ! queue ! v4l2sink device=/dev/video1 \
vid. ! queue ! v4l2sink device=/dev/video2
```

Voila!  Now use `/dev/video2`