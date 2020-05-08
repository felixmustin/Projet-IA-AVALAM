# PROJET IA AVALAM 
# FÉLIX MUSTIN 18075

## BIBLIOTHÈQUES

Différentes bibliothèques sont utilisées dans les codes:
json, sys, copy, cherrypy, socket

## STRATÉGIE

L'IA repose sur un algorithme minmax, avec un état donné initial il prévoit jusqu'à 2 coups plus loin dans le jeu pour tous des coups possible.
Ensuite pour ces états modifiés du jeu on calcule le score du plateau : ` 
`+1` si le pion le plus haut d'une case est à nous, `+2` si la pile de pions est de 5 (car la tour n'est plus modifiable, donc coup à privilégier)
`-1` si il est à l'adversaire, `-2` si la pile de pions est de 5

## INFORMATIONS

Les programmes nécéssitent python 3.X

Pour s'inscrire au serveur il faut d'abord lancer le fichier `subscribe.py` avec la commande suivate : 

```
python3 subscribe.py 3001 'nom' 'matricule'
```

On peut ensuite lancer le fichier `matche.py` avec la commande :

```
python3 matche.py 8080
```

