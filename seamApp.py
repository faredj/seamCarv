import numpy as np
from Tkinter import *
from PIL import ImageTk, Image
import cv2 as cv
import Tkinter, Tkconstants, tkFileDialog
import tkMessageBox
import seamCarv as sc


def saveImage():
    print "save image..."

def LunchProcess():
    print "process started..."
    btnStart.config(state=DISABLED)
    radio1.config(state=DISABLED)
    radio2.config(state=DISABLED)
    #print imgArray
    imgTmp = imgArray
    fct = fChoice.get()
    newHeight = vHeight.get()
    newWidth =  vWidth.get()
    
    if(newWidth < img.width):#suppression de seam Horizontaux
        nbIteration = img.width - newWidth
        for i in range (1, nbIteration):
            energiesOfEachPix = sc.pixelsEnergies2(imgTmp)
            cumulativeEnergies = sc.cumVerticalEnergies(energiesOfEachPix)
            seamVertival = sc.computeVericalSeam(cumulativeEnergies)
            imgTmp = sc.removeVSeam(imgTmp, seamVertival)
    elif (newWidth > img.width):#duplication de seam Horizontaux
        nbIteration = newWidth - img.width
        print "duplication"
    else:
        pass
    
    if(newHeight < img.height):#suppression de seam Verticaux
        nbIteration = img.height - newHeight
        for i in range (1, nbIteration):
            energiesOfEachPix = sc.pixelsEnergies2(imgTmp)
            cumulativeEnergies = sc.cumHorizontalEnergies(energiesOfEachPix)
            seamVertival = sc.computeHorizontalSeam(cumulativeEnergies)
            imgTmp = sc.removeHSeam(imgTmp, seamVertival)
    elif (newHeight > img.height):#duplication de seam Verticaux
        nbIteration = newHeight - img.height

    
    img2 = Image.fromarray(imgTmp)
    imgTk2 = ImageTk.PhotoImage(image = img2)
    panel.configure(image=imgTk2)
    panel.image = imgTk2
    

#Initialiser la fenetre et la frame 
window = Tk()
window.title("Seam Carving")
frame = Frame(window)
frame.pack()

#Charger l'image
#window.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

#Choisir la fonction de calcul d'energie
fChoice = IntVar()
fChoice.set(1)
radio1 = Radiobutton(frame, text="Fct d'energie 1", variable=fChoice, value=1)
radio1.pack(side = LEFT)

radio2 = Radiobutton(frame, text="Fct d'energie 2", variable=fChoice, value=2)
radio2.pack(padx=5,side = LEFT)

vWidth = IntVar()
eWidth = Entry(frame, width = 6, textvariable=vWidth)
eWidth.insert(0, 'width')
eWidth.pack(padx=5,side = LEFT)

vHeight = IntVar()
eHeight = Entry(frame, width = 6, textvariable=vHeight)
eHeight.insert(0, 'height')
eHeight.pack(padx=5,side = LEFT)

btnStart = Button(frame, text="Lancer", command=LunchProcess)
btnStart.pack(padx=5,side = LEFT)

labelText2 = StringVar()
messageSize = Label(window, textvariable=labelText2).pack(padx=10,side = TOP)

#Bare de menu
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=saveImage)
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

#Affichage de l'image la premiere fois
path = "/home/faredj/Bureau/pyth/repoDossier/loutres.jpg"
imgArray = cv.imread(path)
img = Image.fromarray(imgArray)
imgTk = ImageTk.PhotoImage(image = img)
panel = Label(window, image = imgTk)
panel.pack()

labelText2.set("L : "+str(img.width)+"    H : "+str(img.height))

window.geometry(str(imgTk.width())+"x"+str(imgTk.height()))
window.config(menu=menubar)
window.mainloop()