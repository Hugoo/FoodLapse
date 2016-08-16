from __future__ import division
import urllib
import cv
import cv2
import numpy as np
import time
import random
import os
import glob
import RPi.GPIO as GPIO
from time import strftime

import glob

count = 150

prevZone = cv2.imread("baseZone.jpg")


#titles = glob.glob("raw/*.jpg")
img = 0
ledPin = 26 

print(strftime("%Y-%m-%d %H:%M:%S")+", SCRIPT LAUNCHED")
		


#url = http://foodcam.media.mit.edu/axis-cgi/mjpg/video.cgi
#request header :
#HTTP/1.0 200 OK
#Content-Type: multipart/x-mixed-replace; boundary=--myboundary

#API : https://www.ispyconnect.com/man.aspx?n=Axis

#Get the last image :
#http://foodcam.media.mit.edu/jpg/1/image.jpg

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin,GPIO.OUT)

def downloadAndSaveImage(url,filename):
	#Download the last image :
	global img
	try:
		urllib.urlretrieve("http://foodcam.media.mit.edu/jpg/1/image.jpg", filename)
	except:
		print(strftime("%Y-%m-%d %H:%M:%S")+",error with urllib, waiting 1min")
		time.sleep(60)
		
	img = cv2.imread(filename)
	return img[185:480, 0:680]

def findAndCleanContours(imgThresh, minArcLength):
	#Find external contours and remove small ones
	contours, hierarchy = cv2.findContours(imgThresh,cv.CV_RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	return [x for x in contours if cv2.arcLength(x, True)>=minArcLength]

def printImgWithContours(title, img, contours):
	cv2.drawContours(img, contours, -1, (0,255,0), 1)
	cv2.imshow(title, img)

def isBoxInsideBox(box1,box2):
	#Return True if box1 inside box2
	#(x,y,w,h)
	#Also remove box1 if too small
	if box1[2]<35 or box1[3]<25:
		return True

	offset = 5
	return (box1[0]+offset>=box2[0] and (box1[0]+box1[2])<=(box2[0]+box2[2]) and box1[1]+offset>=box2[1] and (box1[1]+box1[3])<=(box2[1]+box2[3]))

def getBoxesFromCnt(cnt):
	#Given a list of contours, return pertinent boxes (remove small boxes and keep parent)

	boundingBoxes = [cv2.boundingRect(c) for c in cnt]
	boundingBoxes = sorted(boundingBoxes, key=lambda x: (x[0], x[1])) #Sort by x and y
	
	#Remove boxes inside one another
	finalBoxes = []

	#xxx
	for box in boundingBoxes:
		inside = False
		for lBox in finalBoxes:
			if isBoxInsideBox(box,lBox):
				inside = True
				break
		if not inside:
			finalBoxes.append(box)

	return finalBoxes


def drawBoxesOnImg(boxes, img):
	for box in boxes:
		x,y,w,h = box[0],box[1],box[2],box[3]
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

def hasMoved(newFood, newPeople):
	#Return True if thinks something happened between old and new boxes
	
	#the easiest way is to use people boxes. If something moves here, it will
	#have an impact on the food zone.

	#Used with boxes calculated by diff from previous img, so we have boxes
	#only if something move

	if len(newFood)!=0 and len(newPeople)!=0:
		return True

	return False

def generateImgName():
	#Get last img name
	try:
		lastName = max(glob.iglob('raw/*.jpg'), key=os.path.getctime)
		numero = int(lastName[7:11])+1
		longueur = len(str(numero))
		return "img"+"0"*(4-longueur)+str(numero)+".jpg"
	except ValueError:
		return "img0001.jpg"




def computeAll():
	global count
	global prevZone
	global img
	
	
	#===== GET IMAGE =====#
	im = downloadAndSaveImage("http://foodcam.media.mit.edu/jpg/1/image.jpg", "temp.jpg")

	#===== THRESHOLD =====#
	#Here, use the previous img to get the motion,
	imThresh = computeDiff(prevZone,im) #makeThreshold(foodZone, 100, cv2.THRESH_BINARY)
	prevCopy = imThresh.copy()
	prevZone = im.copy()

	#===== CONTOURS =====#
	imContours = findAndCleanContours(imThresh,90)


	#===== BOXES =====#
	imBoxes = getBoxesFromCnt(imContours)


	if len(imBoxes)!=0:
		imgName = generateImgName()
		cv.SaveImage("raw/"+imgName,cv.fromarray(img))
		print(strftime("%Y-%m-%d %H:%M:%S")+","+imgName)
		GPIO.output(ledPin,GPIO.HIGH)
	else:
		GPIO.output(ledPin,GPIO.LOW)




def computeDiff(base, img):
	#Add assert
	baseImg = cv.fromarray(base)
	baseImgGrey = cv.CreateMat(baseImg.height, baseImg.width, cv.CV_8U)
	cv.CvtColor(baseImg, baseImgGrey, cv.CV_RGB2GRAY)

	nextImg = cv.fromarray(img)
	nextImgGrey = cv.CreateMat(baseImg.height, baseImg.width, cv.CV_8U)
	cv.CvtColor(nextImg, nextImgGrey, cv.CV_RGB2GRAY)

	res = cv.CreateMat(baseImg.height, baseImg.width, cv.CV_8U)
	cv.AbsDiff(nextImgGrey, baseImgGrey, res)

	cv.Smooth(res, res, cv.CV_BLUR, 5,5)

	cv.MorphologyEx(res, res, None, None, cv.CV_MOP_OPEN)
	cv.MorphologyEx(res, res, None, None, cv.CV_MOP_CLOSE)
	cv.Threshold(res, res, 30, 255, cv.CV_THRESH_BINARY)

	return np.asarray(res[:,:])


while(1):
	computeAll()
	time.sleep(1)
	if cv2.waitKey(1) ==27:
		exit(0)
