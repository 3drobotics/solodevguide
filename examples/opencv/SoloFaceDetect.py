import cv2
import sys
import time
import threading
from SoloCamera import SoloCamera

#open HDMI-In as a video capture device
#BE SURE YOU HAVE RUN `SOLO VIDEO ACQUIRE`
video_capture = SoloCamera()

#HDMI-In uses a ring buffer that stops grabbing new frames once full
#so this allows us to remove excess frames that we aren't using
CLEAR_EXTRA_FRAMES = True
kill_thread = False

def clear_frames():
    while kill_thread is False:
        video_capture.clear()
#start a background thread to clear frames
if CLEAR_EXTRA_FRAMES:
    thr = threading.Thread(target=clear_frames)
    thr.start()

#open a face tracking classifier
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

try:
    while True:
        start = time.time()
        # Capture a grayscale image
        ret, frame = video_capture.read()

        #resize image to decrease processing time
        frame = cv2.resize(frame,(0,0), fx = 0.5,fy = 0.5)

        #detect faces
        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.3, #larger number equals less false positives but more false negative. Decrease for more false postives
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        #calculte time is took to process
        fps = round(1/(time.time()-start),2)

        #print the results
        print "Found {0} faces at {1} fps:".format(len(faces),fps)
        for (x, y, w, h) in faces:
            cent_x = x + w/2
            cent_y = y + h/2
            print "---Center(x:{0}, y:{1}), Size(w:{2}, h:{3})".format(cent_x,cent_y,w,h)
except KeyboardInterrupt:
    kill_thread = True
