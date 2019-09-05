import cv2
import numpy as np
import secret as sc
import random

'''
This module deals with fingerprint reading functionalities
'''



#Prepare the data by creating a binary thresholded image of it and skeletonize

def prep_data(img):
	img = cv2.bilateralFilter(img,4,8,2)
	ret2,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)		
	skel = cv2.ximgproc.thinning(img,img,cv2.ximgproc.THINNING_ZHANGSUEN)

	return skel


#Feature detect finds ROIs/corners through Harris corner detection
#param: skel- a skeletonized version of the image
#name: the original image

def feature_detect(skel, name):
	#filename of image
	filen = name

	#create an np array
	corner = np.float32(skel)	

	#find harris corners
	harris_corners = np.zeros(corner.size, dtype = "float32")
	harris_corners = cv2.cornerHarris(corner,2,5,0.04)
	
	
	img_hc = np.zeros(harris_corners.size, dtype = "float32")

	img_hc = cv2.normalize(harris_corners,img_hc,0,255,cv2.NORM_MINMAX, dtype = cv2.CV_32FC1)
	
	

	#threshold to eliminate excessive points and create a set of keypoints
	threshold = 170.0
	keypoints = []

	rescaled = np.zeros(corner.size, dtype = "uint8")
	rescaled = cv2.convertScaleAbs(img_hc)

	dimx , dimy = rescaled.shape
	
	#draw circles around all keypoints
	count = 0
	for i in range(dimx):
		for j in range(dimy):
			if int(img_hc[i][j]) > threshold:
				#eliminate any corners that may be caused by incomplete fingerprint
				if (i > 10 and  i < (dimx-10) ) and (j > 10 and j < (dimy-10)):
					
					
					cv2.circle(corner, (j,i), 5, (255,0,0),1 )
					cv2.circle(rescaled,(j,i),5,(255,0,0),1)
					keypoints.append(cv2.KeyPoint(j,i,1))


	#confirm and show detected keypoints

	cv2.imshow(filen, corner)
	
	
	#return and set of corners keypoints
	return corner,keypoints

#this module possibly used in future functionality for verification of fingerprints
def orb_image(img,keypts,img2,keypts2):
	orb = cv2.ORB_create()
	#compute descriptors for first image
	keys, des = orb.compute(img,keypts)
	#compute descriptors for second image
	keys2, des2 = orb.compute(img2,keypts2)
	imgt= np.zeros(img.size, dtype = "uint8")
	#need brute force matcher for orb
	bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck =True)
	matches = bf.match(des,des2)
	matches = sorted(matches, key = lambda match:match.distance)
	
	img3 = cv2.drawMatches(img,keypts, img2,keypts2,matches[:5], flags=2, outImg=None)
	cv2.imshow("testing orb", img3)
	cv2.waitKey(0)


	
#this function encrypts all of the keypoints and writes them to a file
#params: keypoints - they set of keypoints taken from a fingerprint image
def encrypt_prints(keypoints):
	#created encrypted point array
	enc_points = np.zeros((6,2,len(keypoints)), dtype='uint32')
	#for all points, encrypt each value by creating random shares
	j = 0
	for i in keypoints:
		secretx, sharesx = sc.make_random_shares( minimum = 3, shares =6, pixel = i.pt[0])
		secrety, sharesy = sc.make_random_shares(minimum =3, shares =6, pixel = i.pt[1])

		for sharex in sharesx:
			k = sharex[0] -1
			enc_points[k][0][j]= sharex[1]
		for sharey in sharesy:
			k = sharey[0] -1
			enc_points[k][1][j]= sharey[1]
		j +=1
	j=0
			

	print("Writing to file.")

	#write to file and same as tab spaced value file
	for i in range(0,6):
		#create a file
		filen = "../DATA/keypt" + str(i) + ".tsv"
		filex = open(filen, "w")
		
		#write the encrypted points one line at a time
		for m in range(len(keypoints)):
			#write the points to a line
			share = i+1
			line = str(share) + " " + str(enc_points[share-1][0][m]) + " " + str(enc_points[share-1][1][m]) + "\n"
			filex.write(line)

	#write/create an answer key to compare against
		filen = "../DATA/answerkey.txt"
		filex = open(filen,"w")
	for i in keypoints:
		line = str(i.pt[0]) + " " + str(i.pt[1]) + "\n"
		filex.write(line)

#this function restores the points from the shares.  The shares are chosen at random
#param: files - the set of files that will be used to recover
#param: pts - the set of pts (this parameter is now obsolete)

def restore_points(files,pts):
	#load the text from each file
	filen = "../DATA/decrypted.txt"
	filex = open(filen, "w")
	ds1 = np.loadtxt("../DATA/keypt0.tsv", delimiter = " ")
	ds2 = np.loadtxt("../DATA/keypt1.tsv", delimiter = " ")
	ds3 = np.loadtxt("../DATA/keypt2.tsv", delimiter = " ")
	ds4 = np.loadtxt("../DATA/keypt3.tsv", delimiter = " ")
	ds5 = np.loadtxt("../DATA/keypt4.tsv", delimiter = " ")
	ds6 = np.loadtxt("../DATA/keypt5.tsv", delimiter = " ")
	
	#initialize sets to restore the points	
	restored_points = []

	for i in range(0,pts):
		txshares = []
		tyshares = []
		shares = set()
		#generate a random set of shares
		while len(shares)<3:
			r= random.randint(1,6)
			#print(r)
			shares.add(r)
		for share in shares:
			#create the set of shares that are required to decrypt			
			if share ==1:
				txshares.append((1,int(ds1[i][1])))
				tyshares.append((1,int(ds1[i][2])))
			if share ==2:
				txshares.append((2,int(ds2[i][1])))
				tyshares.append((2,int(ds2[i][2])))
			if share ==3:
				txshares.append((3,int(ds3[i][1])))
				tyshares.append((3,int(ds3[i][2])))
			if share ==4:
				txshares.append((4,int(ds4[i][1])))
				tyshares.append((4,int(ds4[i][2])))
			if share ==5:
				txshares.append((5,int(ds5[i][1])))
				tyshares.append((5,int(ds5[i][2])))
			if share ==6:
				txshares.append((6,int(ds6[i][1])))
				tyshares.append((6,int(ds6[i][2])))
		
		#recover x and y points and append to file		
		rx = sc.recover_secret(txshares)		
		ry = sc.recover_secret(tyshares)
		
		#create line string
		line = str(rx) + " " + str(ry) + "\n"
		#write the line to file
		filex.write(line)
		#append the set of points to restored_points set
		restored_points.append((rx,ry))
		
		
	#return the set of restored points	
	return restored_points



	
		 
#a tester main function for keypoint detection

if __name__ == "__main__":
	img = cv2.imread("../DATA/DB1_B/102_1.tif",0)
	img2 = cv2.imread("../DATA/DB1_B/102_2.tif",0)
	#test that it is reading correctly
	cv2.imshow("Image",img)
	cv2.imshow("Image2",img2)
	cv2.waitKey(0)
	skel = prep_data(img)
	skel2 = prep_data(img2)
	cv2.imshow('Thinned', skel)
	cv2.imshow('Thinned2', skel2)
	cv2.waitKey(0)
	#find cornerness points
	corners, keypoints = feature_detect(skel, "pic1")
	corners2, keypoints2 = feature_detect(skel2, "pic2")
	cv2.waitKey(0)
	cv2.destroyAllWindows()