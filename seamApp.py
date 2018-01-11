import numpy as np
from Tkinter import *
from PIL import ImageTk, Image
import cv2 as cv
import tkFileDialog
import seamCarv as sc

#lancement du processus
def LunchProcess():
    print "process started..."
    btnStart.config(state=DISABLED)
    radio1.config(state=DISABLED)
    radio2.config(state=DISABLED)
    imgTmp = imgArray
    fct = fChoice.get()
    newHeight = vHeight.get()
    newWidth =  vWidth.get()
    
    if(newWidth < img.width):#suppression de seam Verticaux
        nbIteration = img.width - newWidth
        for i in range (1, nbIteration):
            if(fct == 1):
                energiesOfEachPix = sc.pixelsEnergies1(imgTmp)
            elif (fct == 2):
                energiesOfEachPix = sc.pixelsEnergies2(imgTmp)
            cumulativeEnergies = sc.cumVerticalEnergies(energiesOfEachPix)
            seamVertival = sc.computeVericalSeam(cumulativeEnergies)
            imgTmp = sc.removeVSeam(imgTmp, seamVertival)
    elif (newWidth > img.width):#duplication de seam Verticaux
        nbIteration = newWidth - img.width
        calculatedSeam = []
        for i in range (1, nbIteration):
            if(fct == 1):
                energiesOfEachPix = sc.pixelsEnergies1(imgTmp)
            elif (fct == 2):
                energiesOfEachPix = sc.pixelsEnergies2(imgTmp)
            cumulativeEnergies = sc.cumVerticalEnergies(energiesOfEachPix)
            seamVertival = sc.computeVericalSeamForDup(cumulativeEnergies,calculatedSeam)
            calculatedSeam.append(seamVertival)
        for s in calculatedSeam:
            imgTmp = sc.duplicateVSeam(imgTmp, s)
    else:
        pass
    
    if(newHeight < img.height):#suppression de seam Horizontaux
        nbIteration = img.height - newHeight
        for i in range (1, nbIteration):
            if(fct == 1):
                energiesOfEachPix = sc.pixelsEnergies1(imgTmp)
            elif (fct == 2):
                energiesOfEachPix = sc.pixelsEnergies2(imgTmp)
            cumulativeEnergies = sc.cumHorizontalEnergies(energiesOfEachPix)
            seamHorizontal = sc.computeHorizontalSeam(cumulativeEnergies)
            imgTmp = sc.removeHSeam(imgTmp, seamHorizontal)
    elif (newHeight > img.height):#duplication de seam Horizontaux
        nbIteration = newHeight - img.height
        for i in range (1, nbIteration):
            if(fct == 1):
                energiesOfEachPix = sc.pixelsEnergies1(imgTmp)
            elif (fct == 2):
                energiesOfEachPix = sc.pixelsEnergies2(imgTmp)
            cumulativeEnergies = sc.cumHorizontalEnergies(energiesOfEachPix)
            seamHorizontal = sc.computeHorizontalSeam(cumulativeEnergies)
            imgTmp = sc.duplicateHSeam(imgTmp, seamHorizontal)
    else:
        pass

    cv.imwrite(pTofldr+"/imgRezized.jpg", imgTmp)
    img2 = Image.fromarray(sc.rearrangColorChannel(imgTmp))
    imgTk2 = ImageTk.PhotoImage(image = img2)
    window.geometry(str(imgTk2.width())+"x"+str(imgTk2.height()))
    panel.configure(image=imgTk2)
    panel.image = imgTk2
    

#Initialiser la fenetre et la frame 
window = Tk()
window.title("Seam Carving")
frame = Frame(window)
frame.pack()

#Charger l'image
window.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
pathToFoldr = window.filename.split("/")
pTofldr=""
for i in range (1, len(pathToFoldr)-1):
    pTofldr+="/"+pathToFoldr[i]
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

btnStart = Button(window, text="Lancer", command=LunchProcess)
btnStart.pack(padx=5,side = TOP)

labelText2 = StringVar()
messageSize = Label(window, textvariable=labelText2).pack(padx=10,side = TOP)

#Bare de menu
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

#Affichage de l'image la premiere fois
path = window.filename
imgArray = cv.imread(path)
img = Image.fromarray(sc.rearrangColorChannel(imgArray))
imgTk = ImageTk.PhotoImage(image = img)
panel = Label(window, image = imgTk)
panel.pack()

labelText2.set("L : "+str(img.width)+"    H : "+str(img.height))

window.geometry(str(imgTk.width())+"x"+str(imgTk.height()))
window.config(menu=menubar)
window.mainloop()