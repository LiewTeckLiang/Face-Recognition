from __future__ import print_function
from Util import Util
from imutils.video import VideoStream
import argparse
import time


def new_register():

	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--picamera", type=int, default=-1,
		help="whether or not the Raspberry Pi camera should be used")
	args = vars(ap.parse_args())
  
	print("Starting camera...")
	vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
	time.sleep(2.0)
	
	pba = Util(vs)
	pba.root.mainloop()

