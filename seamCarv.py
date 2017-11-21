import numpy as np
import math
import cv2 as cv
import Tkinter
from Tkinter import *
import Image, ImageTk

def energyCal(img):
    img = cv.GaussianBlur(img,(3,3),0)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgX = cv.Sobel(img,cv.CV_64F,1,0,ksize=3)
    imgY = cv.Sobel(img,cv.CV_64F,0,1,ksize=3)
    img = cv.add(np.absolute(imgX), np.absolute(imgY))
    return img

def energyCal_1(img):
    i=0
    height, width = img.shape[0:2]
    for i in range(0, height):
        for j in range(0, width):
            topLeft = img[i-1][j-1] if i-1>=0 and j-1>=0 else 0
            top  = img[i-1][j] if i-1>=0 else 0
            topRight = img[i-1][j+1] if i-1>=0 and j+1<width else 0

            bottomLeft = img[i+1][j-1] if i+1<height and j-1>=0 else 0
            bottom = img[i+1][j] if i+1<height else 0
            bottomRight = img[i+1][j+1] if i+1<height and j+1<width else 0

            left = img[i][j-1] if j-1>=0 else 0
            right = img[i][j+1] if j+1<width else 0

            gX = topLeft + (2*top) + topRight - bottomLeft - (2*bottom) - bottomRight
            gY = topLeft + (2*left) + bottomLeft - topRight - (2*right) - bottomRight
            img[i][j] = math.sqrt(gX**2 + gY**2)

            if i==0 and j==0:
                print math.sqrt(gX**2 + gY**2)

    return img

if __name__ == '__main__':
    img = cv.imread('ski-min.jpg', 0)
    print energyCal_1(img)
"""
    root = Tkinter.Tk()
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img) 
    Tkinter.Label(root, image=imgtk).pack() 
    root.mainloop()"""