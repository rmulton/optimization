# Problème du musée
L'énoncé est disponible en suivant ce lien : https://www-desir.lip6.fr/~durrc/Iut/optim/dm2-couverture

## Utilisation
La résolution du problème est donnée dans le notebook python ```museum.ipynb```. Pour l'exécuter, entrer ```jupyter notebook museum.ipynb```. PySCIPOpt et Jupyter doivent être installés.

## Modèle
### Variables
Les caméras sont ici supposés être positionnés à des coordonnées entières afin de simplifier le problème. Le musée est ainsi représenté par une grille. Chaque point de la grille peut prendre la valeur 0 ou 1 pour chaque type de caméra. La valeur 1 est donnée s'il y a une caméra du type en question en ce point.
### Fonction objectif
L'objectif étant de diminuer les coûts, la fonction objectif choisie est la somme des coûts pour chaque caméra, i.e. le prix de chaque caméra multiplié par le nombre de caméra de ce type. La formule suivante donne cette fonction : ```math \sum_{i} \sum_{j} (c_{ij}^{1}*p^{1} + c_{ij}^{2}*p^{2})```
### Contraintes
La contrainte choisie est d'imposer la présence d'une caméra de type 1 dans le rayon d'une caméra de type 1 autour de chaque oeuvre d'art, ou bien la présence d'une caméra de type 2 dans le rayon d'une caméra de type 2 autour de cette oeuvre. La formule suivante donne la contrainte pour une oeuvre d'art : \sum_{oeuvre} ( \sum_{c_{ij}^{1}/d_{oeuvre}(i,j)\leqslant d^{2}} + \sum_{c_{ij}^{2}/d_{oeuvre}(i,j)\leqslant d^{2}} )