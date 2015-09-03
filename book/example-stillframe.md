# Stillframe Photo API

<aside class="note">
To run this example, run `solo-utils video-splice` first to get camera access.
</aside>

<aside class="note">
This example requires you to [install the packages](uploading.html#installing-packages) `gst-plugins-good-jpeg gst-plugins-base-tcp`.
</aside>

This example provides a RESTful API on port `8080` that can be accessed from Solo.When the HTTP endpoint is hit, it uses `gstreamer` to grab a frame from the video feed and provide it as a response. We also include an example app that allows you to grab a frame in your web browser.

Our API definition is simple: every request to the `/jpeg` endpoint fetches a new frame from the video feed.

This API is implemented as three processes/threads launched from `server.py`:

* *gstreamer* is spawned to take video input from `/dev/video1` and create a MJPEG server on port `5000`.
* A background thread is launched that connects to the MJPEG server and caches only the latest JPEG.
* A server thread is launched to serve static assets (like HTML and JavaScript), and also implement the above API call. Every time the `/jpeg` endpoint is hit, the most recent JPEG is streamed back to the user.

The server is implemented using _[flask](http://flask.pocoo.org/)_, and should be very straightforward to modify.

## Installing _stillframe_

<aside class="note">
See [Bundling Python](advanced-python.html) for an explanation of the following steps.
</aside>

Clone the [solodevguide](https://github.com/3drobotics/solodevguide) repository and cd into the [examples/stillframe](https://github.com/3drobotics/solodevguide/tree/master/examples/stillframe) directory.

In this folder, run:

```sh
virtualenv env
source ./env/bin/activate
echo 'import sys; import distutils.core; s = distutils.core.setup; distutils.core.setup = (lambda s: (lambda **kwargs: (kwargs.__setitem__("ext_modules", []), s(**kwargs))))(s)' > env/lib/python2.7/site-packages/distutils.pth
pip install -r requirements.txt
```

Package the required modules for Solo:

```sh
pip wheel -r ./requirements.txt --build-option="--plat-name=py27"
```

Next, and every time we make changes to Python, we can sync our code to Solo using *rsync*:

```sh
rsync -avz --exclude="*.pyc" --exclude="env" ./ solo:/opt/stillframe
```

Now SSH into Solo and run the following commands:

```sh
virtualenv env
source ./env/bin/activate
pip install --no-index ./wheelhouse/* -UI
python server.py
```

Every time you change code, you can use Ctrl+C to kill the server, use _rsync_ to synchronize changes from your host computer, and run `python server.py` again to relaunch it.
