#!/usr/bin/python3

import requests
import time
import shutil
import logging
import sys
import json
import pathlib

import iplapsconf as conf

print("Logging to "+conf.logFileName)

logging.basicConfig(filename=conf.logFileName, format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

logging.info("==================================================")
logging.info("ipCameraServerAddress: "+conf.ipCameraServerUrl)

logging.info("Command arguments: {}".format(' '.join(map(str, sys.argv[1:]))))
startDelay = float(sys.argv[2]) / 1000.0 # should be seconds, but effectively ms are passed in
imageFilePath = sys.argv[4]
fullImageFilePath = sys.argv[6]
logging.info("Writing file to " + imageFilePath)
logging.info("Full image file path " + fullImageFilePath)
logging.info("Start delay " + str(startDelay))

path = pathlib.Path(imageFilePath)
path.mkdir(parents=True, exist_ok=True)

time.sleep(startDelay)
response1 = requests.get(conf.ipCameraServerUrl + '/getsnapshot')
time.sleep(1) # get ip camera a chance to store the image
response2 = requests.get(conf.ipCameraServerUrl + '/get/' + response1.text, stream=True)
with open(fullImageFilePath, 'wb') as out_file:
	response2.raw.decode_content = True
	shutil.copyfileobj(response2.raw, out_file)


