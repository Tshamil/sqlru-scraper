try:
	import Image
except ImportError:
	from PIL import Image

import cv2
import numpy as np
import pytesseract
import argparse

from classes.parser import Parser
from pprint import pprint
import sys
import os

parser = argparse.ArgumentParser(description='Short sample app')
parser.add_argument('-f', action='store', dest='file', help='Source file with email image')
parser.add_argument('-m', action='store', dest='memberId', help='Member Id')
results = parser.parse_args()

if results.memberId:
	parser = Parser(results.memberId)
	try:
		imgIO = parser.request().parsePage().requestEmailImg()
		im = Image.open(imgIO).convert('RGB')
	except ValueError as err:
		print(err)
		raise SystemExit
		
elif results.file:
	im = Image.open(results.file).convert('RGB')
else:
	raise SystemExit

cvImg = np.array(im) 
cvImg = cvImg[:, :, ::-1].copy()

img = cv2.cvtColor(cvImg, cv2.COLOR_BGR2GRAY)
height, width = img.shape[:2]
img = cv2.resize(img, (20 * width, 20 * height), interpolation = cv2.INTER_CUBIC)

cv2.imwrite('temp.png', img)

#print(pytesseract.image_to_string(Image.open('test_2.png'), lang="eng", config='--tessdata-dir "traning/tessdata"'))

print(pytesseract.image_to_string(Image.open('temp.png')))

os.remove('temp.png')
