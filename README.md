# SeamCarving 

## C'est quoi Seam Carving ?


Le **seam carving** ou recadrage intelligent, est un algorithme de réduction d'image, dont l'objectif est de garder les proportions de l'objet tout en supprimant des informations peu utiles de l'image. Cet algorithme redimensionne, non pas par une mise à l'échelle ou un recadrage classique, mais par une suppression de chemins de pixels dits de moindre importance (seams).


## Notre Méthode de calcul

 Une image est une matrice de triplets (r, g, b), chacun représentant un pixel. L’idée va être de se donner une **fonction d’énergie** qui pour chaque pixel mesure sa ressemblance avec ses voisins. On va ensuite chercher dans la matrice un chemin de **moindre énergie**, et le supprimer.

* Calcul d’énergie de chaque pixel : L’énergie de chaque pixel est calculée à l'aide de deux fonctions, une se basant sur l'ntensité des pixels voisins et l'autre sur les filtre Gaussian blur pour réduire l'intensité des détails et Sobel pour calculer le gradient de l'intensité de chaque pixel selon la direction X ou Y.
* 	Calcul d’énergie cumulative : Après avoir calculé l'énergie de l'image,on calcule  l’énergie cumulée, qui est la somme des énergies du pixel plus les pixels qui le précédent  (via l'approche de programmation dynamique)
* 	Calcul des seams : Calculer le chemin en suivant les pixels voisins où l'énergie est la plus minimale.


## Ce Projet


Est une implémentation de l'algorithme **SeamCarving** avec le langage de programmation `python`.




## Bibliothéques utilisées
Pour que l'application fonctionne sur votre environnement les bibliothèques suivantes sont requises :


####  -   NumPy
[NumPy](http://www.numpy.org/) est une bibliothèque numérique , destinée à manipuler des matrices ou tableaux multidimensionnels ainsi que des fonctions mathématiques opérant sur ces tableaux.

 #### - OpenCV 
[OpenCV](https://opencv.org/) c'est  une bibliothèque de traitement d'image.

#### - Tkinter 
[Tkinter](http://www.tkdocs.com/) : permet de créer des interfaces graphiques

#### - Math
permet d’avoir accès aux fonctions mathématiques

#### - PIL
Est une bibliothèque pour la manipulation des images.

## Améliorations
* Augmenter la taille de l’image en rajoutant des seams : En duplicant les seams on arrive à augmenter la taille de l’image, avant la duplication on calcul d'abord l'ensemble des seams puis on parcours les seams calculés et on les dupliquants.

* Fonction de calcul d’énergie en utilisant les filtres : la fonction consiste à utiliser les filtre Gausian Blur et Sobel principalement pour faire apparaitre les contours ce qui permet d'avoir des energies différentes.

## Lancement de projet
Lancer avec la commande :  *python seamApp.py*


## Exemple d'exécution
### - Réduction d'images
Exemple 1 :<br/>
Originale<br/>
![Fleurs](/uploads/09a9f8053e94e0f7de9bcfbff041abf6/fleurs.jpg "Fleurs")<br/>
Aprés réduction<br/>
![Fleurs](/uploads/851f2a31e7b21955754f252524e9e400/fleursResized.jpg "Fleurs")<br/>

Exemple 2 :<br/>
Originale<br/>
![Couche de soleil](/uploads/db5c5b4a50aa044b4541676ff78c4534/coucheSoleil.jpg "Couche de soleil")<br/>
Aprés réduction<br/>
![Couche de soleil](/uploads/7fe4754ebc46fe6751c3257423ec47d9/coucheSoleilResized.jpg "Couche de soleil")<br/>

### - Agrandissement d'images
Exemple 3 :<br/>
Originale<br/>
![Maison](/uploads/6857f66e69f1749ea61c617e6b4e62bb/maison.jpg "Maison")<br/>
Aprés réduction<br/>
![Maison](/uploads/ad4a8f433ee0c658c0cdc50b351d0235/maisonResized.jpg "Maison")<br/>

## Sources
[https://en.wikipedia.org/wiki/Seam_carving](https://en.wikipedia.org/wiki/Seam_carving)<br/>
[http://cs.brown.edu/courses/cs129/results/proj3/rkuppig/](http://cs.brown.edu/courses/cs129/results/proj3/rkuppig/)<br/>
[http://www.faculty.idc.ac.il/arik/SCWeb/imret/index.html](http://www.faculty.idc.ac.il/arik/SCWeb/imret/index.html)<br/>
[https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_image_display/py_image_display.html](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_image_display/py_image_display.html)<br/>
[https://www.pyimagesearch.com/2017/01/23/seam-carving-with-opencv-python-and-scikit-image/](https://www.pyimagesearch.com/2017/01/23/seam-carving-with-opencv-python-and-scikit-image/)
## Auteurs
HAMMACHE Faredj  
IDIR Sonia