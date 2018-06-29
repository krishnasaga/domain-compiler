import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import templateMatch

def bruteForeMatch(snapshot,features):
	for x in features:
		img1 = cv.imread('./image.jpg',0)          # queryImage
		img2 = cv.imread(x['feature-image'],0) # trainImage
	
		# Initiate ORB detector
		orb = cv.ORB_create()
		# find the keypoints and descriptors with ORB
		kp1, des1 = orb.detectAndCompute(img1,None)
		kp2, des2 = orb.detectAndCompute(img2,None)


		# create BFMatcher object
		bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
		# Match descriptors.
		matches = bf.match(des1,des2)
		# Sort them in the order of their distance.
		matches = sorted(matches, key = lambda x:x.distance)
		
		# Initialize lists
		list_kp1 = []
		list_kp2 = []

		# For each match...
		for mat in matches:

			# Get the matching keypoints for each of the images
			img1_idx = mat.queryIdx
			img2_idx = mat.trainIdx

			# x - columns
			# y - rows
			# Get the coordinates
			(x1,y1) = kp1[img1_idx].pt
			(x2,y2) = kp2[img2_idx].pt 
			
			print(kp1[img1_idx])
			print(kp2[img2_idx]) 
			
			
			
						# Append to each list
			list_kp1.append((x1, y1))
			list_kp2.append((x2, y2))
			
		print( list_kp1)
		print( list_kp2)
	return matches

features = [{'feature':'price-panel', 'feature-image':"./template.png"},
			{'feature':'summary-panel','feature-image':"./template2.png"},
            {'feature': 'gallery' , 'feature-image': "./template6.png"}]

bruteForeMatch('./template', features)


