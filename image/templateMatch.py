import numpy as np
import cv2 
import matplotlib.pyplot as plt
import json
import math

def templatematch(snapshot,features):
	requiredJson=[]
	page={'page':'flight_options'}
	featureMatches={'count':2}
	featuresdata=[]
	for x in features:
		img_rgb = cv2.imread(snapshot)
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
		template = cv2.imread(x['feature-image'],0)
		w, h = template.shape[::-1]

		res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res);
		threshold = 0.8
		loc = np.where( res >= threshold)
		if max_val >= threshold:
			data = {}
			data['name'] = x['feature']
			
			data['match']=max_val
			featuresdata.append(data)
			
		
		for pt in zip(*loc[::-1]):
			cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
			cv2.imwrite('res.png',img_rgb)
			
			
	featureMatches['features']=featuresdata
	page['featureMatches']=featureMatches
	requiredJson.append(page)
	json_data = json.dumps(requiredJson)
	f = open('./file.txt','w')
	f.write(json_data)
	f.close()


features1 = [{'feature':'price-panel', 'feature-image':"./f1.jpg"},
			{'feature':'summary-panel','feature-image':"./f2.jpg"},
            {'feature': 'gallery' , 'feature-image': "./template6.png"}]
templatematch('desk.jpg',features1)	


