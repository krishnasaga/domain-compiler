##import cv2
##from matplotlib import pyplot as plt

##image = cv2.imread('./image.jpg')
##template = cv2.imread('./template.png')

##res = cv2.matchTemplate(image,template,cv2.TM_CCORR_NORMED)

##min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res);

##cv2.rectangle(image, min_loc, max_loc, 0, 2)
	
##plt.subplot(121),plt.imshow(image,cmap = 'gray')
##plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
##plt.show()



import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


fruits = ["./template.png", "./template2.png", "./template6.png"]
for x in fruits:

  img1 = cv.imread('./image.jpg',0)          # queryImage
  img2 = cv.imread(x,0) # trainImage
  # Initiate ORB detector
  orb = cv.ORB_create()
  # find the keypoints and descriptors with ORB
  kp1, des1 = orb.detectAndCompute(img1,None)
  kp2, des2 = orb.detectAndCompute(img2,None)


  # create BFMatcher object
  bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
  # Match descriptors.
  matches = bf.match(des1,des2)
  print (des2)
  # Sort them in the order of their distance.
  matches = sorted(matches, key = lambda x:x.distance)
  # Draw first 10 matches.
  img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:10], None,flags=2)
  plt.imshow(img3),plt.show()
  