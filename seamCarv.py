import numpy as np
import math
import cv2 as cv
import Tkinter
from Tkinter import *
import Image, ImageTk
import time


def rearrangColorChannel(img):
    b,g,r = cv.split(img)
    return cv.merge((r,g,b))

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

##Main()
if __name__ == '__main__':
    start_time = time.time()
    img = cv.imread('../repoDossier/pont.jpg')	#Reading Image

    energiesOfEachPix = pixelsEnergies(img)	#Calculate energy of each pixel
    print energiesOfEachPix
    cumulativeEnergies = cumVerticalEnergies(energiesOfEachPix)	#Calculate cumulative energy
    x=len(img[0])	
    for i in range (1, 100):
        seam = computeCerSeam(cumulativeEnergies)
        img = removeVSeam(img, seam)
        cumulativeEnergies = removeEnergyVSeam(cumulativeEnergies, seam)
        print "step ",i
    print "old size : ",x ,", new size : ", len(img[0])
    root = Tkinter.Tk()
    img = Image.fromarray(rearrangColorChannel(img))
    imgtk = ImageTk.PhotoImage(image=img) 
    Tkinter.Label(root, image=imgtk).pack()
    print("--- %s seconds ---" % (time.time() - start_time))
    root.mainloop()
