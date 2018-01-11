import numpy as np
import math
import cv2 as cv
import Image, ImageTk

def rearrangColorChannel(img):
    b,g,r = cv.split(img)
    return cv.merge((r,g,b))


def cumVerticalEnergies(energies):
    print "cumulating energies V..."
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

def cumHorizontalEnergies(energies):
    print "cumulating energies H..."
    height, width = energies.shape[0:2]
    energiesCum = np.zeros((height, width), dtype=np.int)
    for i in range(0, height):
        energiesCum[i][0] = energies[i][0]

    for j in range(1, width):
        for i in range(0, height):
            minEnergy = 0
            if i-1<0:
                minEnergy = min(energiesCum[i][j-1], energiesCum[i+1][j-1])
            elif i+1>=height:
                minEnergy = min(energiesCum[i][j-1], energiesCum[i-1][j-1])
            else:
                minEnergy = min(energiesCum[i-1][j-1], energiesCum[i][j-1], energiesCum[i+1][j-1])

            energiesCum[i][j] = energies[i][j] + minEnergy
    return energiesCum

def computeVericalSeam(energies):
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

def computeVericalSeamForDup(energies,seams):
    height, width = energies.shape[0:2]
    verticalSeam = []
    startJIndex = []
    for e in seams:
        startJIndex.append(e[0][1])
    
    firstRow = (energies[height-1]).tolist()
    minFounded = False
    jIndex = firstRow.index(min(firstRow))
    while (not minFounded):
        if(jIndex in startJIndex):
            firstRow[jIndex] = max(firstRow)
            jIndex = firstRow.index(min(firstRow))
        else:
            minFounded = True

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

def computeHorizontalSeam(energies):
    height, width = energies.shape[0:2]
    horizontalSeam = []
    iIndex = np.argmin(energies[:,width-1])
    horizontalSeam.append((iIndex,width-1))
    for j in range (width-2, -1, -1):
        if iIndex - 1 < 0:
            d = {energies[iIndex][j]:(iIndex,j),energies[iIndex+1][j]:(iIndex+1,j)}
        elif iIndex + 2 > height:
            d = {energies[iIndex-1][j]:(iIndex-1,j), energies[iIndex][j]:(iIndex,j)}
        else:
            d = {energies[iIndex-1][j]:(iIndex-1,j), energies[iIndex][j]:(iIndex,j),energies[iIndex+1][j]:(iIndex+1,j)}
        coupleIndex = d.get(min(d))
        horizontalSeam.append(coupleIndex)
        iIndex = coupleIndex[0]
    return horizontalSeam

def computeHorizontalSeamForDup(energies,seams):
    height, width = energies.shape[0:2]
    horizontalSeam = []
    startJIndex = []
    for e in seams:
        startJIndex.append(e[0][0])
    
    firstRow = (energies[:,width-1]).tolist()
    minFounded = False
    iIndex = firstRow.index(min(firstRow))
    while (not minFounded):
        if(iIndex in startJIndex):
            firstRow[iIndex] = max(firstRow)
            iIndex = firstRow.index(min(firstRow))
        else:
            minFounded = True

    horizontalSeam.append((iIndex,width-1))
    for j in range (width-2, -1, -1):
        if iIndex - 1 < 0:
            d = {energies[iIndex][j]:(iIndex,j),energies[iIndex+1][j]:(iIndex+1,j)}
        elif iIndex + 2 > height:
            d = {energies[iIndex-1][j]:(iIndex-1,j), energies[iIndex][j]:(iIndex,j)}
        else:
            d = {energies[iIndex-1][j]:(iIndex-1,j), energies[iIndex][j]:(iIndex,j),energies[iIndex+1][j]:(iIndex+1,j)}
        coupleIndex = d.get(min(d))
        horizontalSeam.append(coupleIndex)
        iIndex = coupleIndex[0]
    return horizontalSeam

def pixelsEnergies1(img):
    print "energy of each pixel..."
    i=0
    height, width = img.shape[0:2]
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

def pixelsEnergies2(img):
	img = cv.GaussianBlur(img,(3,3),0)
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	imgX = cv.Sobel(img,cv.CV_64F,1,0,ksize=3)
	imgY = cv.Sobel(img,cv.CV_64F,0,1,ksize=3)
	img = cv.add(np.absolute(imgX), np.absolute(imgY))
	return img

def removeVSeam(mat,seam):
    print "remove vert seam..."
    height, width = mat.shape[0:2]
    imgnew = np.zeros((height, (width - 1), 3), np.uint8)
    for p in seam:
        i = p[0]
        j = p[1]
        imgnew[i] = np.delete(mat[i],(j),axis=0)
    return imgnew

def removeHSeam(mat,seam):
    print "remove hor seam..."
    height, width = mat.shape[0:2]
    imgnew = np.zeros(((height-1), width, 3), np.uint8)
    for p in seam:
        i = p[0]
        j = p[1]
        imgnew[:, j] = np.delete(mat[:, j], (i), axis=0)
    return imgnew

def duplicateVSeam(mat,seam):
    print "duplicate vert seam..."
    height, width = mat.shape[0:2]
    imgnew = np.zeros((height, (width + 1), 3), np.uint8)
    for p in seam:
        i = p[0]
        j = p[1]
        imgnew[i, 0:j+1] = mat[i, 0:j+1]
        imgnew[i, j+1:width+1] = mat[i, j:width]
    return imgnew

def duplicateHSeam(mat,seam):
    print "duplicate hor seam..."
    height, width = mat.shape[0:2]
    imgnew = np.zeros(((height+1), width, 3), np.uint8)
    for p in seam:
        i = p[0]
        j = p[1]
        imgnew[0:i+1, j] = mat[0:i+1, j]
        imgnew[i+1:height+1, j] = mat[i:height, j]
    return imgnew