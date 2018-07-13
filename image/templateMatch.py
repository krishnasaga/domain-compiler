import numpy as np
import cv2 
import matplotlib as plt
import json
import math
import sys
import os, os.path
dir_path = os.path.dirname(os.path.realpath(__file__))

requiredJson=[]
def templatematch(snapshot,features):
    page={'page': features[0]['page']}
    featureMatches={'count':2}
    i=0
    featuresdata=[]
    img_rgb=0
	
    if(os.path.isfile(snapshot)):
        img_rgb = cv2.imread(snapshot)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    else:
        print('Screenshot not found!')
        return

    for x in features:
        if os.path.isfile(dir_path + "/" + x['feature-image']):
            template = cv2.imread(dir_path + "/" + x['feature-image'],0)
            w, h = template.shape[::-1]
        else:
            print('Template not found!')
            return

        if (img_rgb.shape[0] < template.shape[0] and img_rgb.shape[1] < template.shape[1]):
            print('Screenshot is smaller than template')
            return

        try:
            res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        except IOError:
            print('\tIO error----')
        else:
            print ("\tCompared feature---")
            
        if not os.path.exists('results'):
              os.makedirs('results')
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        threshold = 0.8
        loc = np.where( res >= threshold)

        if max_val >= threshold:
            data = {}
            data['name'] = x['feature']
            data['match'] = max_val
            featuresdata.append(data)
        print(snapshot.split('/')[1])
        print('\t'+x['page']+' : '+x['feature'])
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            cv2.putText(img_rgb, data['name'] ,(pt[0] + int(round(w/2)) - 200 ,pt[1] - 20 ) , cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0))
            
            cv2.imwrite('results/'+snapshot.split('/')[-1]+'.png',img_rgb)
           
    featureMatches['features']=featuresdata
    featureMatches['count']=len(featuresdata)
    page['featureMatches']=featureMatches
    requiredJson.append(page)


features =[
	{'page': 'flightOptions', 'feature':'hub-spoke', 'feature-image':'templates/flightOptions/hubNspoke.png'},
	{'page': 'flightOptions', 'feature':'selected-flight', 'feature-image':'templates/flightOptions/flightCard.png'},
	{'page': 'flightOptions', 'feature':'alternate-flights', 'feature-image':'templates/flightOptions/altFlights.png'},
	{'page': 'flightOptions', 'feature':'selectyour-seats', 'feature-image':'templates/flightOptions/luggage.png'},
	{'page': 'flightOptions', 'feature':'special-assistance', 'feature-image':'templates/flightOptions/specialAssistance.png'},
	{'page': 'flightOptions', 'feature':'selected', 'feature-image':'templates/flightOptions/selected.png'},
	{'page': 'flightOptions', 'feature':'gallery', 'feature-image':'templates/flightOptions/imageGallery.png'},
	{'page': 'flightOptions', 'feature':'select-button', 'feature-image':'templates/flightOptions/button.png'},
	{'page': 'flightOptions', 'feature':'date-selection', 'feature-image':'templates/flightOptions/dateSelection.png'}
]


def templateMapper(screenshot):
    if(os.path.isfile(screenshot)):
        print('\nMatching template...')
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
                templateMapper(snapshotDir+'/'+filename)
    json_data = json.dumps(requiredJson)
    f = open('hyperSnapshot.txt','w+')
    f.write(json_data)
    f.close()
	 
main(sys.argv)

