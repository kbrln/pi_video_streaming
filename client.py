# USAGE
# python client.py --server-ip 192.168.1.103

# import the necessary packages
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True,
	help="ip address of the server to which the client will connect")
args = vars(ap.parse_args())

print("initialising imagesender")
# initialize the ImageSender object with the socket address of the server
sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(args["server_ip"]))
print("initalised, getting clienthostname")

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
rpiName = socket.gethostname()
print(f"name = {rpiName}")

# vs = VideoStream(usePiCamera=True).start()
vs = VideoStream(-1).start()	# use webcam instead of picamera
time.sleep(2.0)
 
print("start loop")
while True:
	# read the frame from the camera and send it to the server
	frame = vs.read()
	print("frame", frame)
	sender.send_image(rpiName, frame)
vs.release()
