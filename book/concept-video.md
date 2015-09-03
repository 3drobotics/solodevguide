# Video Pipeline

```
GoPro -> HDMI cable -> HDMI encoder -> i.MX6 (h.264 encode/gstreamer) -> WiFi (UDP) -> Controller (h.264 decode/hdmi output/UDP relay to phone) -> WiFi (UDP) -> App
```

In normal operation, the GoPro video device (`/dev/video0`) is acquired exclusively by Solo's video encoder (referred to as *sndast*). 

## Viewing Live Video

To view live video as it is being recorded by Solo, you can use VLC on your computer.

First, we need to create a connection to Solo to enable video output. Either ensure the Solo App is open on your phone, or create a TCP connection from your command line as follows:

```
nc 10.1.1.1 5502
```

You can leave this open (there is no need to type into this prompt). Then, you can open `[sololink.sdp](https://github.com/3drobotics/solodevguide/blob/master/tools/video/sololink.sdp)` using VLC. This describes the RTP stream configuration that enables VLC to interpret Solo's video stream.

<aside class="todo">
Show a screenshot of this working in VLC.
</aside>

## Configuring Solo's Video Output

Because *sndast* has exclusive access to Solo's video input, we need to reconfigure it by splitting the video device via an intermediary.

Overview: We will attach an intermediary GStreamer pipeline to `/dev/video0`.  Then we will pipe that info into two virtual devices, `/dev/video1` and `/dev/video2`.  We will instruct *sndast* to attach to `/dev/video1`, leaving device `/dev/video2` for use as we please.

There are two pieces of software that are needed in order for this to work.  The first is `gst-plugins-good-video4linux2`, which allows us to use the `v4l2sink` pipeline in GStreamer.  The second is a kernel module called `v4l2loopback`, wihch allows us to emulate a video device. 

[After having installed the `solo-utils` tool](utils.html), connect Solo to the internet using `solo-utils tunnel-start`. Then, install these packages:

```
smart update
smart install gst-plugins-good-video4linux2 v4l2loopback v4l-utils gst-plugins-base-videotestsrc
```

After installing, run `depmod -a` or reboot to refresh your kernel modules.

Next, modify `/usr/bin/video_send.sh` line 88 from `-g 0` to `-g 1`.  This will tell sculpture to use `/dev/video1`. To trigger a reload of `video_send.sh` while Solo is running, run `killall video_send.sh`. The script will automatically restart.

From your Solo's shell, run:

```
solo-utils video-start
```

This command creates a service that splits `/dev/video0` into two outputs, `/dev/video1` and `/dev/video2`. *sndast* will continue to pipe video from `/dev/video1` as normal, but `/dev/video2` is now available for scripts to take as input, e.g. OpenCV, saving video to disk, taking still shots, etc.

If you are interested in modifying the video before it reaches *sndast*, you can modify the video pipeline. The file `/opt/solo-utils/video-service/output-pipeline` contains the default pipeline, which is just to queue data:

```
queue
```

You can modify this file to use alternative GStreamer plugins:

```
textoverlay text="Hello world!"
```

For a more complex example of modifying the video pipeline, see [how to write a dynamic video overlay](video-overlay.html).

## Video Pipeline Internals

The video pipeline uses several kernel modules loaded at runtime to interpret video. The most important of these:

```
modprobe mxc_v4l2_capture
```

This initiates the capture of the HDMI device (the GoPro camera) as a v4l2 (Video4Linux2) device loaded at `/dev/video0`. All scripts which parse video manually require this.

Internally, the *sndast* video driver uses GStreamer to begin a video pipeline using `tvsrc`:

```
gst-launch tvsrc device=/dev/video0 ! mfw_ipucsc ! ... <h246 encoder>
```

The `mfw_ipucsc` pipeline uses iMX6 drivers to transform the video into a planer (YUV) colorspace, making it suitable for encoding as h264 or further processing.

Creating multiple video processing endpoints requires the kernel-level driver `v4l2loopback`, which creates video devices that echo their video input as video output. To activate this driver:

```
modprobe v4l2loopback exclusive_caps=0,0 video_nr=1,2
```

This creates loopback devices `/dev/video1` and `/dev/video2` devices (as specified by `video_nr`). To split our video feed across these two devices, we create a GStreamer pipeline that sources from HDMI and outputs using `v4l2sink`:

```
gst-launch tvsrc ! mfw_ipucsc ! tee name=vid \
vid. ! queue ! v4l2sink device=/dev/video1 \
vid. ! queue ! v4l2sink device=/dev/video2
```

We can then source any of these v4l2 devices to capture video, e.g.:

```
gst-launch v4l2src device=/dev/video1 ! x264enc ! filesink filename=saved_video.mp4
```

This will save an h264-encoded video from the HDMI video source to `saved_video.mp4`.

## Further Reading

* [How to write a dynamic video overlay](video-overlay.html)
* [Custom video output](video-out.html)
