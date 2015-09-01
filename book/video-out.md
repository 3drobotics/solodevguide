# Custom Video Output

Video from Solo is a variable-bitrate output stream processed through a custom service `sndast`.

## Modifying Video

Replace /dev/video1 with a processed one.

## Replacing Video Streaming

If you are interested in modifying the format of the video downlink, for example adding metadata, or disabling post-processing done by `sndast`, it is possible to disable this output and provide a custom video stream using conventional streamers, e.g. gstreamer.