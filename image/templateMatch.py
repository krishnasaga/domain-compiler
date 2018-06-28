import numpy as np
import cv2 
import matplotlib.pyplot as plt

def templatematch(snapshot,features):
	a=[]
	for feature in features : 
		image = cv2.imread(snapshot)
		template = cv2.imread(feature)
		res = cv2.matchTemplate(image,template,cv2.TM_CCORR_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res);
		a.append([min_val, max_val, min_loc, max_loc,res])
	return a	


	


