# Visual Cryptography of Biometric Data



## Description


## Installation
This program runs on python 3 and requires the installation of the following libraries:

OpenCV and OpenCV-Contrib </br>
Numpy </br>
PyFingerprint (for part 3)</br>
pyserial3 (for part 3)</br>



## Usage

### To run the program
****
From the SRC folder, type the following:

python project.py

****************************************

#### There are three parts to the project:
1. Image Encryption technique
2. Fingerprint encryption/decryption from dataset
3. Fingerpret reader, encryptor and decryptor

#### For part 1:
_________________________________________________________
##### Encryption:
You will be prompted to enter a filename for an image.  These images should be placed in the DATA/pictures folder.
Once you've directed the program to a valid image file, the program will prompt you to enter values for t and n.
As it stands, the program currently works best when t=3.  When t=4, it sometimes works but not always.
Anything greater than 4 will result in the program terminating. </br>

The program will then display the image in grayscale and prompt you to press enter.
The program will encrypt the images and save them in the DATA/pictures folder.

##### Decryption:

You will then be prompted to enter the exact filename of one of the shares and then its corresponding share value.  The shar value will
be the share value will correspond to the naming scheme, i.e. if the file was saved as "cat1.png", the share value will be 1.  
Enter these until you have entered at least t shares.
Press 'r' and the picture will be restored (in grayscale).

#### For part 2:
_____________________________________________________________
Part 2 will choose an image from the dataset at random and display it's feature points.  This dataset can be found in /DATA/DB1_B.
The program will create a text file of the locations of the keypoints (titled "answerkey.txt") and .tsv files that contain the share values of the keypoints.
By pressing enter (after the first 3 images appear), the program will randomly decrypt 3 "shares" files and create a text file of the decrypted shares.  You can then compare the decrypted text file with the answerkey to confirm the points were successfully restored.

#### For part 3:
______________________________________________________________
Part 3 only runs on Linux.  You will need a fingerprint sensor compatible with pyfingerprint and you need to install the pyfingerprint library (which also requires the pyserial3 library).  The user is prompted to place their thumb on the sensor and an image of the user's thumbprint is saved.  This portion of the application essentially does the same thing as part 2 except the processed image is the one collected by the sensor.  I used the FlashTree Green Light Optical Fingerprint Sensor connected to a USB to TTL serial converter.  