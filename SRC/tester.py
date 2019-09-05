import secret as sc
import cv2
import numpy as np
import math
import random


#this module does the main encryption of the images


#image test converts a color picture into a grayscale image and creates n images that can restore
#a grayscale of the original image by combining the information of t images
#param: fname - the filename of the original image
#param: t  - an integer that must be less than or equal to n. It denotes the number of minimum shares
#param: n  - an integer that denotes the number of images/shares to be created
def image_test(fname,t,n):
	#initialize to empty sets
	secret = []
	shares = []

	#read the image and convert it to gray scale
	img = cv2.imread(fname)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#convert to numpy array
	test1 = np.asarray(gray)
	#display original image
	cv2.imshow(fname,test1)
	#prompt user to press a key
	print("Press a key to begin encryption.")
	cv2.waitKey(0)

	print("Encrypting images. Please wait; this may take a few minutes. ")
	#get the dimensions of the image
	rows, cols = test1.shape
	#initialize an n * height * width * 3 matrix of zeros
	all_shares = np.zeros((n,rows,cols,3), dtype='uint8')
	
	#iterate through each pixel
	for i in range(rows):
		for j in range(cols):
		    #for each pixel create shares
		    secreti, sharesi = sc.make_random_shares( minimum = t, shares =n, pixel = test1[i][j])
		    #convert the large numbers from the resulting shares into values <255	
		    for shares in sharesi:
		    	#setting this value of k ensures we start at 0 
		    	k = shares[0]-1
		    	#ac_share is the value held by one of the shares
		    	#this value will be spread across the BGR channels of a color image
		    	#the number of the secret share can be reconstructed by the information in the
		    	#[0] and [2] values of the all_shares matrix...these represent
		    	#the Blue and Red channels of the image.  The green channel value is chosen at random
		    	ac_share = shares[1]
		    	all_shares[k][i][j][0] = int(ac_share/255)
		    	all_shares[k][i][j][1] = random.randrange(0,255)
		    	all_shares[k][i][j][2] = ac_share % 255
		    	

	#create a naming scheme for each share
	#and save each share image 
	for i in range(len(all_shares)):
		window = "Randomized Image " + str(i)
		nfname = fname[:-4] + str(i+1) + ".png"
		print(nfname)
		#show and save the image
		cv2.imshow(window, all_shares[i])
		cv2.imwrite(nfname, all_shares[i])
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return
	