#Optimisation

## Premier Modèle

Nous avons commencé par une résolution qui nous semblait la plus intuitive : les variables correspondaient aux segments et les domaines aux mots du dictionnaire. 

Une ligne était représentée par les coordonnées de son début, sa fin, et le fait qu’elle soit horizontale ou verticale. 
Une intersection entre deux lignes était représentée par ses coordonnées et un tuple représentant l’indice de la ligne et l’indice de la colonne qui forment cette intersection (la première intersection est contenue dans la 1ère ligne et 0ème colonne).

Les contraintes étaient donc :
-	Un mot doit faire la longueur du segment qui le contient.
-	 A l’endroit de l’intersection, le mot de la ligne et celui de la colonne doivent avoir la même lettre.
-	Les mots doivent être deux à deux différents.

Le modèle fonctionnait avec une petite grille mais pouvait tourner très longtemps voire ne pas arriver à bout lorsque la grille était plus grande. Ceci était du au fait que les deux dernières contraintes citées nécessitaient chacune à n^2 instructions avec n nombre de mots. Nous avons essayé de réduire le temps de calcul du programme en réduisant les champs de recherche aux mots qui avaient la bonne taille, en les ayant au préalable classé par taille. Cela a permis d’aller plus vite mais le temps de calcul était toujours beaucoup trop grand pour que la tâche soit réalisable.

## Deuxième Modèle

Dans le deuxième modèle, nous avons pris comme variables les segments et les cases, et comme domaines les mots et les lettres respectivement.

Le domaine d’une variable case est maintenant réduit à seulement 26 possibilités.

- La contrainte sur la longueur des mots dans les segments reste inchangée.

- Un mot est composé des lettres qui sont contenues dans les cases qui constituent le segment.

Nous n'avons pas eu à rajouter une contrainte sur les intersections car celle-ci était implicitement donnée dans la contrainte précedente. 
La contrainte qui empêche un mot d'apparaitre deux fois dans la grille a été supprimée car elle rallongeait considérablement le calcul. 

Avec ce modèle, nous sommes arrivés au résultat ci-dessous avec un temps de calcul de 0:05:18.228956

"""
# # # # # # # # # # # # # # #
# # # k e n s i n g t o n # #
# s # n # e # o # u # r # # #
# t h e r e i n # a l i b i #
# r # e # d # i # r # e # n #
# e n d s # p a n d a n u s #
# n # # # g # n # i # t # i #
# g u n m e n # j a n s e n #
# t # i # n # v # n # # # u #
# h a l l i n a n # d a n a #
# e # s # u # c # o # n # t #
# n e s t s # a b s e n c e #
# # # o # e # n # l # o # s #
# # a n i s o t r o p y # # #
# # # # # # # # # # # # # # #
"""

Remarque: nous remarquons que le modèle n'est pas déterministe. En effet, à chaque fois qu'on exécute le programme, il nous renvoie une solution différente.