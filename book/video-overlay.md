# Dynamic Video Overlay

<aside class="note">
This example requires you to install the packages `python-gst`
</aside>

We're going to overlay text onto Solo's video output. This will be visible in Solo's mobile app and any other video clients.

```py
import gst

# Create the pipeline for our elements.
pipeline = gst.Pipeline('pipeline')

hdmi_source = gst.element_factory_make('tvsrc', 'hdmi_source')
hdmi_source.set_property('device', '/dev/video0')
pipeline.add(hdmi_source)

colorspace = gst.element_factory_make('mfw_ipucsc', 'colorspace')
pipeline.add(colorspace)
video_source.link(colorspace)

#capsfilter = gst.element_factory_make('capsfilter')
#capsfilter.set_property('caps', gst.caps_from_string('video/x-raw-yuv, width=320, height=240'))

textoverlay = gst.element_factory_make('textoverlay', 'textoverlay')
textoverlay.set_property('text', '1')
pipeline.add(textoverlay)
colorspace.link(textoverlay)

video1 = gst.element_factory_make('v4l2sink', 'video1')
video1.set_property('device', '/dev/video1')
pipeline.add(video1)
textoverlay.link(video1)

#video2 = gst.element_factory_make('v4l2sink', 'video2')
#video2.set_property('device', '/dev/video2')
#pipeline.add(video2)
#colorspace.link(video2)

# Set our pipelines state to Playing.
pipeline.set_state(gst.STATE_PLAYING)

# Wait until error or EOS.
bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE,
    gst.MESSAGE_ERROR | gst.MESSAGE_EOS)
print msg

# Free resources.
pipeline.set_state(gst.STATE_NULL)
```

## References

* <https://markwingerd.wordpress.com/2014/11/19/using-gstreamer-with-python/>
* <http://www.jonobacon.org/2006/11/03/gstreamer-dynamic-pads-explained/>
