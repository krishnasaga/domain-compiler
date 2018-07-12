import numpy as np
import cv2 
import matplotlib as plt
import json
import math
import sys
import os, os.path


requiredJson=[]
def templatematch(snapshot,features):
    page={'page': features[0]['page']}
    featureMatches={'count':2}
    i=0
    featuresdata=[]
	
    if(os.path.isfile(snapshot)):
        img_rgb = cv2.imread(snapshot)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    else:
        print('Screenshot not found!')
        return

    for x in features:

        if os.path.isfile(x['feature-image']):
            template = cv2.imread(x['feature-image'],0)
            w, h = template.shape[::-1]
        else:
            print('Template not found!')
            return
		
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
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


features =[
	{'page': 'flightOptions', 'feature':'hub-spoke', 'feature-image':'./templates/flightOptions/hubNspoke.png'},
	{'page': 'flightOptions', 'feature':'flight-card', 'feature-image':'./templates/flightOptions/flightCard.png'},
	{'page': 'flightOptions', 'feature':'alternate-flights', 'feature-image':'./templates/flightOptions/altFlights.png'},
	{'page': 'flightOptions', 'feature':'selectyour-seats', 'feature-image':'./templates/flightOptions/selectyourSeats.png'},
	{'page': 'flightOptions', 'feature':'special-assistance', 'feature-image':'./templates/flightOptions/specialAssistance.png'}
]


def templateMapper(screenshot):
    if(os.path.isfile(screenshot)):
        print('Matching template...')
        templatematch(screenshot,features)
    else:
	    print('Screenshot not found!!')	


def main(args):
    if len(args) == 1 :
	    print('No input provided')
    else : 
        snapshotDir = args[1]
        for root, dirs, files in os.walk(snapshotDir):  
            for filename in files:
                print("Commit head : "+args[2])
                print("Build time : "+args[3])
                templateMapper(snapshotDir+'/'+filename)
    json_data = json.dumps(requiredJson)
    f = open('hyperSnapshot.txt','w+')
    f.write(json_data)
    f.close()
	 
main(sys.argv)

