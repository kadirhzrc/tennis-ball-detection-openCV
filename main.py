from collections import deque
from imutils.video import VideoStream
import numpy
import argparse
import time
import cv2
import imutils

# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--video")
ap.add_argument("--buffer", type=int, default=32)

args = vars(ap.parse_args())

# define boundaries of the ball color green in HSV color model, then initialize the list of tracked points
greenLowerBound = (25, 86, 6)
greenUpperBound = (67, 255, 255)

pts = deque(maxlen=args["buffer"])

# if there is no video file supplied, take reference to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
# if not, get the video file
else:
	vs = cv2.VideoCapture(args["video"])

# let it sleep for processing purposes
time.sleep(2.0)

# loop until the program is interrupted or the supplied video file ends
while True:
	# get current frame
	frame = vs.read()
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame
	# if processing video and there exists no more frame, then video ended
	if frame is None:
		break

	# resize the frame, blur it, and convert it to the HSV color model
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform a series of dilations and erosions to remove small blobs
	mask = cv2.inRange(hsv, greenLowerBound, greenUpperBound)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current (x,y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None

	# only proceed if at least one contour is found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame, then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
	# update the points queue
	pts.appendleft(center)

	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		# otherwise, compute the thickness of the line and draw the connecting lines
		thickness = int(numpy.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
# otherwise, release the camera
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()