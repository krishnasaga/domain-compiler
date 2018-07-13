import numpy as np
import cv2
import json
import math
import sys
import os

commitHead = sys.argv[2]
builldTime = sys.argv[3]


requiredJson=[]
def templatematch(snapshot,features):
	page={'page': snapshot.split('/')[-1].split('.')[-1]}
	featureMatches={'count':2}
	i=0
	featuresdata=[]
	
	img_rgb = cv2.imread(snapshot)
	for x in features:
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
			data['match'] = max_val
			featuresdata.append(data)
		
		for pt in zip(*loc[::-1]):
			cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
			cv2.imwrite('results/'+x['page']+'.png',img_rgb)
			
	featureMatches['features']=featuresdata
	featureMatches['count']=len(featuresdata)
	page['featureMatches']=featureMatches
	requiredJson.append(page)


features1 =[
	{'page': 'flightOptions', 'feature':'hub-spoke', 'feature-image':'./templates/flightOptions/hubNspoke.png'},
	{'page': 'flightOptions', 'feature':'flight-card', 'feature-image':'./templates/flightOptions/flightCard.png'},
	{'page': 'flightOptions', 'feature':'alternate-flights', 'feature-image':'./templates/flightOptions/altFlights.png'},
	{'page': 'flightOptions', 'feature':'standard-seats', 'feature-image':'./templates/flightOptions/standardSeats.png'},
	{'page': 'flightOptions', 'feature':'selectyour-seats', 'feature-image':'./templates/flightOptions/selectyourSeats.png'},
	{'page': 'flightOptions', 'feature':'extraLeg-seats', 'feature-image':'./templates/flightOptions/extraLegSeats.png'},
	{'page': 'flightOptions', 'feature':'luggage', 'feature-image':'./templates/flightOptions/luggage.png'},
	{'page': 'flightOptions', 'feature':'special-assistance', 'feature-image':'./templates/flightOptions/specialAssistance.png'}
]

features2 =[
    {'page':'extraOptions', 'feature':'hub-spoke', 'feature-image':'./templates/extraOptions/hubNspoke.png'},
    {'page':'extraOptions', 'feature':'tfc', 'feature-image':'./templates/extraOptions/tuiCareFoundation.png'},
    {'page':'extraOptions', 'feature':'airport-parking', 'feature-image':'./templates/extraOptions/airportParking.png'},
    {'page':'extraOptions', 'feature':'airportHotel-parking', 'feature-image':'./templates/extraOptions/airportHotelParking.png'}]

snapshotDir = sys.argv[1];



for root, dirs, files in os.walk(snapshotDir):  
    for filename in files:
     print(snapshotDir + "/" + filename)


