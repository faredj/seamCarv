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

### - #### - Math
Est une bibliothèque pour la manipulation des images.

## Améliorations
* Augmenter la taille de l’image en rajoutant des seams : En duplicant les seams on arrive à augmenter la taille de l’image (duplicateVSeam)
* Fonction de calcul d’énergie en utilisant les filtres

## Lancement de projet
Lancer avec la commande :  python seamApp.py


## Résultats
![Origine](http://www.levif.be/medias/5774/2956429.jpg "Origine")  
**♣ Image Origine**


![Origine](http://www.levif.be/medias/5774/2956429.jpg "Origine")  
**♣ Image Effet 1**
> Un mot !!

![Origine](http://www.levif.be/medias/5774/2956429.jpg "Origine")  

## Source

## Auteurs
Hammache Faredj  
Idir Sonia  
```