import cv2
import secret as sc
import numpy as np
import math


#function restores the image
#param: pictures - the set of "shares" needed to restore a picture
#param: keys - the corresponding key to each picture
#initialize empty set
image = []
def restoreImg(pictures,keys):
	
	for i in range(len(pictures)):
		#append image to the image set	
		image.append(cv2.imread(pictures[i]))
		image[i] = np.asarray(image[i])
	
	#get dimensions of the restored image and initialize an np array with size of image
	rows = len(image[0])
	cols = len(image[0][0])
	restored_image = np.zeros((rows,cols), dtype = 'uint8')
	
	#initialize some matrices that will be used in the computation restoration
	mat = np.zeros((rows,cols,3))
	mat1 = np.full((rows,cols),1)
	mat255 = np.full((rows,cols),255)
	
	#initialize matrix multipliers
	mat[:,:,0] = mat255
	mat[:,:,1] = mat1
	mat[:,:,2] = mat1

	#initialize a set of shares
	ac_share = []

	#restore the actual values of the secret shares
	for i in range(len(pictures)):
		t_mat = np.multiply(image[i][:,:,0], mat255)
		ac_share.append(np.add(image[i][:,:,2],t_mat))

	

	for i in range(rows):
		for j in range(cols):
			#initialize a set
			shares = []
			
			for k in range(len(pictures)):
				#set up the values of the shares in (t, pub key) form
				shares.append((keys[k],ac_share[k][i][j]))
			#recover the secret value	
			restored_image[i][j] = sc.recover_secret(shares)
	#cv2.imshow("restored", restored_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	#return image restoration
	return restored_image
