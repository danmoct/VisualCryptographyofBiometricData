#import numpy
import cv2

from pyfingerprint import PyFingerprint as pf

#function reads a fingerprint image from fingerprint sensor
def finger_pic():
	try:
	    #initialize sensor
	    f = pf('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

	    if ( f.verifyPassword() == False ):
	        raise ValueError('The given fingerprint sensor password is wrong!')
	#throw exception
	except Exception as e:
	    print('The fingerprint sensor could not be initialized!')
	    print('Exception message: ' + str(e))
	    exit(1)

	#read fingerprint image from sensor
	try:
		print("Waiting for finger...")

		while (f.readImage() == False):
			pass
		#save image to DATA folder
		print("Saving image..")
		f.downloadImage("../DATA/Fprint/finger.png")

		
	#throw exception	
	except Exception as e:
		print("Error occurred")
		print("Exception message: " + str(e))
		exit(1)