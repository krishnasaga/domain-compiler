import numpy as np
import cv2 
import matplotlib as plt
import json
import math
import sys
import os.path


requiredJson=[]
def templatematch(snapshot,features):
	page={'page': features[0]['page']}
	featureMatches={'count':2}
	i=0
	featuresdata=[]
	
	for x in features:
		if(os.path.isfile(snapshot)):
		  img_rgb = cv2.imread(snapshot)
		  img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
		else:
		  print('\033[91m' + 'Screenshot not found!' + '\x1b[0m')
		  return
		  
		if os.path.isfile(x['feature-image']):
			template = cv2.imread(x['feature-image'],0)
			w, h = template.shape[::-1]
		else:
			print('\033[91m' + 'Template not found!' + '\x1b[0m')
			return
		
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
    {'page':'extraOptions', 'feature':'airportHotel-parking', 'feature-image':'./templates/extraOptions/airportHotelParking.png'}
]


def main(argv):
  if len(argv) == 1 :
    print('No input provided')
  else : 
    for arg in argv[1:]:
        pageName = arg.split('=')[0]
        screenshot = arg.split('=')[1]
        if pageName == 'flightOption':
            print(pageName+' - Matching template...')
            templatematch(screenshot,features1)
        if pageName == 'extraOptions':
            print(pageName+' - Matching template...')
            templatematch(screenshot,features2)
    json_data = json.dumps(requiredJson)
    f = open('hyperSnapshot.txt','w+')
    f.write(json_data)
    f.close()

		
main(sys.argv)