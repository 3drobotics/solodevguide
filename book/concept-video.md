# Video Pipeline

In normal operation, the GoPro video device (`/dev/video0`) is acquired exclusively by Solo's video encoder (*sndast*). This topic explains how you can split the video device and use it as needed. It also shows how to view the live video from Solo on your computer.

Video pipeline:

```
GoPro -> HDMI cable -> HDMI encoder -> i.MX6 (h.264 encode/gstreamer) -> WiFi (UDP) -> Controller (h.264 decode/hdmi output/UDP relay to phone) -> WiFi (UDP) -> App
```


## Viewing Live Video

You can use VLC on your computer to view live video as it is being recorded by Solo.

First, we need to create a connection to Solo to enable video output. Either ensure the Solo App is open on your phone, or create a TCP connection from your command line as follows:

```
nc 10.1.1.1 5502
```

You can leave this open (there is no need to type into this prompt). Then, you can open [sololink.sdp](https://github.com/3drobotics/solodevguide/blob/master/tools/video/sololink.sdp) using VLC. This describes the RTP stream configuration that enables VLC to interpret Solo's video stream.

<aside class="todo">
Show a screenshot of this working in VLC.
</aside>

## Configuring Solo's Video Output

Because *sndast* has exclusive access to Solo's video input, we need to reconfigure it by splitting the video device via an intermediary. As a result of this configuration, *sndast* will have exclusive access to `/dev/video1`, and the video will be available for scripts to connect to on `/dev/video2`.

[After having installed the `solo-utils` tool](starting-utils.html), connect Solo to the internet using `solo-utils tunnel-start`. Then, install these packages:

```sh
smart update
smart install gst-plugins-good-video4linux2 v4l2loopback v4l-utils
```

Next, we can start our custom video pipeline. You will need to run this each time your Solo is reset and you want scripts to be able to access video:

```sh
solo-utils video-start
```

Solo's default video output through *sndast* should continue as normal. If you want to revert this video access, run:

```sh
solo-utils video-stop
```

Video is now available on `/dev/video2` for script use. For an example of this in action, see [Using OpenCV](example-opencv.html). <!--For a more complex example of modifying the video pipeline, see [how to write a dynamic video overlay](video-overlay.html).-->

## Video Pipeline Internals

The video pipeline uses several kernel modules loaded at runtime to interpret video. The most important of these:

```
modprobe mxc_v4l2_capture
```

This initiates the capture of the HDMI device (the GoPro camera) as a v4l2 (Video4Linux2) device loaded at `/dev/video0`. All scripts which parse video manually require this.

Internally, the *sndast* video driver uses *GStreamer* to begin a video pipeline using `tvsrc`:

```
gst-launch tvsrc device=/dev/video0 ! mfw_ipucsc ! ... <h246 encoder>
```

The `mfw_ipucsc` pipeline uses iMX6 drivers to transform the video into a planer (YUV) colorspace, making it suitable for encoding as h264 or further processing.


The package `gst-plugins-good-video4linux2` allows us to use the `v4l2sink` pipeline in *GStreamer*.  The second package is a kernel module called `v4l2loopback`, wihch allows us to emulate a video device. Creating multiple video processing endpoints requires the kernel-level driver `v4l2loopback`, which creates video devices that echo their video input as video output. To activate this driver:

```
modprobe v4l2loopback exclusive_caps=0,0 video_nr=1,2
```

This creates loopback devices `/dev/video1` and `/dev/video2` devices (as specified by `video_nr`). To split our video feed across these two devices, we create a *GStreamer* pipeline that sources from HDMI and outputs using `v4l2sink`:

```
gst-launch tvsrc ! mfw_ipucsc ! tee name=vid \
vid. ! queue ! v4l2sink device=/dev/video1 \
vid. ! queue ! v4l2sink device=/dev/video2
```

The *solo-utils* command to start the custom video pipeline starts a service that splits `/dev/video0` into two outputs, `/dev/video1` and `/dev/video2`. *sndast* will continue to pipe video from `/dev/video1` as normal, but `/dev/video2` is now available for scripts to take as input, e.g. OpenCV, saving video to disk, taking still shots, etc.

<!--
## Further Reading

* [How to write a dynamic video overlay](example-vidoverlay.html)
* [Custom video output](example-vidoutput.html)
-->
