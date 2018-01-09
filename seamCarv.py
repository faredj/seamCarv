# -*- coding: utf-8 -*-
import numpy as np
import math
import cv2 as cv
import Tkinter
from Tkinter import *
import Image, ImageTk
import time
#lib for saving image as file
import scipy.misc

#En ce commit j'ai couriger mon id sur le client git

def rearrangColorChannel(img):
	b,g,r = cv.split(img)
	return cv.merge((r,g,b))

def energyCal(img):
	img = cv.GaussianBlur(img,(3,3),0)
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	imgX = cv.Sobel(img,cv.CV_64F,1,0,ksize=3)
	imgY = cv.Sobel(img,cv.CV_64F,0,1,ksize=3)
	img = cv.add(np.absolute(imgX), np.absolute(imgY))
	return img

def cumVerticalEnergies(energies):
	print "cumulating energies..."
	height, width = energies.shape[0:2]
	energiesCum = np.zeros((height, width), dtype=np.int)
	for j in range(0, width):
		energiesCum[0][j] = energies[0][j]

	for i in range(1, height):
		for j in range(0, width):
			minEnergy = 0
			if j-1<0:
				minEnergy = min(energiesCum[i-1][j], energiesCum[i-1][j+1])
			elif j+1>=width:
				minEnergy = min(energiesCum[i-1][j], energiesCum[i-1][j-1])
			else:
				minEnergy = min(energiesCum[i-1][j-1], energiesCum[i-1][j], energiesCum[i-1][j+1])

			energiesCum[i][j] = energies[i][j] + minEnergy
	return energiesCum

def computeCerSeam(energies):
	print "compute seam..."
	height, width = energies.shape[0:2]
	verticalSeam = []
	jIndex = np.argmin(energies[height-1])
	verticalSeam.append((height-1,jIndex))
	for i in range (height-2, -1, -1):
		if jIndex - 1 < 0:
			d = {energies[i][jIndex]:(i,jIndex),energies[i][jIndex+1]:(i,jIndex+1)}
		elif jIndex + 2 > width:
			d = {energies[i][jIndex-1]:(i,jIndex-1), energies[i][jIndex]:(i,jIndex)}
		else:
			d = {energies[i][jIndex-1]:(i,jIndex-1), energies[i][jIndex]:(i,jIndex),energies[i][jIndex+1]:(i,jIndex+1)}
		coupleIndex = d.get(min(d))
		verticalSeam.append(coupleIndex)
		jIndex = coupleIndex[1]
	return verticalSeam

def pixelsEnergies(img):
	print "energy of each pixel..."
	i=0
	height, width = img.shape[0:2]
	"""width = 8
	height = 8"""

	energies = np.zeros((height, width), dtype=np.int)
	for i in range(0, height):
		for j in range(0, width):
			topLeft = np.sum(img[i-1][j-1]) if i-1>=0 and j-1>=0 else 0
			top  = np.sum(img[i-1][j]) if i-1>=0 else 0
			topRight = np.sum(img[i-1][j+1]) if i-1>=0 and j+1<width else 0

			bottomLeft = np.sum(img[i+1][j-1]) if i+1<height and j-1>=0 else 0
			bottom = np.sum(img[i+1][j]) if i+1<height else 0
			bottomRight = np.sum(img[i+1][j+1]) if i+1<height and j+1<width else 0

			left = np.sum(img[i][j-1]) if j-1>=0 else 0
			right = np.sum(img[i][j+1]) if j+1<width else 0

			gX = topLeft + (2*top) + topRight - bottomLeft - (2*bottom) - bottomRight
			gY = topLeft + (2*left) + bottomLeft - topRight - (2*right) - bottomRight
			energies[i][j] = math.sqrt(gX**2 + gY**2)
	return energies

def removeVSeam(mat,seam):
	print "remove Vseam..."
	height, width = mat.shape[0:2]
	imgnew = np.zeros((height, (width - 1), 3), np.uint8)
	for p in seam:
		y = p[0]
		x = p[1]
		imgnew[y, 0:x] = mat[y, 0:x]
		imgnew[y, x:width-1] = mat[y, x+1:width]
	return imgnew

def duplicateVSeam(mat,seam):
	print "duplicate Vseam..."
	height, width = mat.shape[0:2]
	imgnew = np.zeros((height, (width + 1), 3), np.uint8)
	for p in seam:
		y = p[0]
		x = p[1]
		imgnew[y, 0:x+1] = mat[y, 0:x+1]
		imgnew[y, x+1:width+1] = mat[y, x:width]
	return imgnew

def removeEnergyVSeam(mat,seam):
	print "remove Vseam..."
	height, width = mat.shape[0:2]
	imgnew = np.zeros((height, (width - 1)), np.uint8)
	for p in seam:
		y = p[0]
		x = p[1]
		imgnew[y, 0:x] = mat[y, 0:x]
		imgnew[y, x:width-1] = mat[y, x+1:width]
	return imgnew

def duplicateEnergyVSeam(mat,seam):
	print "duplicate Vseam..."
	height, width = mat.shape[0:2]
	imgnew = np.zeros((height, (width + 1)), np.uint8)
	for p in seam:
		y = p[0]
		x = p[1]
		imgnew[y, 0:x] = mat[y, 0:x]
		imgnew[y, x+1:width+1] = mat[y, x:width]
	return imgnew


	"""for i in range(0, (height/2)):
		for j in range (0, width-1):
			imgnew[i][j] = img[i][j]"""

##Main()
if __name__ == '__main__':
	start_time = time.time()
	img = cv.imread('./pont.jpg')	#Reading Image
	
	#get old width heigth
	_height, _width, _channels = img.shape
	#define horizontal steps is used for the horizontal loop
	steps = 300
	
	energiesOfEachPix = energyCal(img)	#Calculate energy of each pixel
	cumulativeEnergies = cumVerticalEnergies(energiesOfEachPix)	#Calculate cumulative energy
	
	#remove '1' or duplicate '0' 
	removeAction = 0
	
	x=len(img[0])	
	for i in range (1, steps):
		seam = computeCerSeam(cumulativeEnergies)
		if removeAction :
			img = removeVSeam(img, seam)
			cumulativeEnergies = removeEnergyVSeam(cumulativeEnergies, seam)
		else:
			img = duplicateVSeam(img, seam)
			cumulativeEnergies = duplicateEnergyVSeam(cumulativeEnergies, seam)
		print "step ",i
	#print "old size : ",x ,", new size : ", len(img[0])

	#Calculate a vertical rang
	stepsV = int(math.floor((float(steps)/_width)*_height))
	
	#Rotate the Image 90°
	img = np.rot90(img)
	
	energiesOfEachPix = energyCal(img)	 #Calculate energy of each pixel
	cumulativeEnergies = cumVerticalEnergies(energiesOfEachPix) #Calculate cumulative energy
	x=len(img[0])
	_h1, _w1, _c1 = img.shape
	print "width:",x,":",_w1,"   h:",_h1
	for i in range (1, stepsV):
		seam = computeCerSeam(cumulativeEnergies)
		if removeAction :
			img = removeVSeam(img, seam)
			cumulativeEnergies = removeEnergyVSeam(cumulativeEnergies, seam)
		else :
			img = duplicateVSeam(img, seam)
			cumulativeEnergies = duplicateEnergyVSeam(cumulativeEnergies, seam)
		print "step ",i
	
	#Rotate the Image 90° original Rotation
	img = np.rot90(img,-1)
	
	__height, __width, __channels = img.shape
	print "old size : ",_width,", ",_height," => new size : ",__width,", ",__height
	
	img = rearrangColorChannel(img);
	print("--- %s seconds ---" % (time.time() - start_time))
	#display or save
	display = 1
	if display :
		root = Tkinter.Tk()
		img = Image.fromarray(img)
		imgtk = ImageTk.PhotoImage(image=img) 
		Tkinter.Label(root, image=imgtk).pack()
		root.mainloop()
	else:
		scipy.misc.imsave('outfileNew5.jpg', img)