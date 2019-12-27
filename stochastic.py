#! /usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
from turtle import *
from random import *

""" TO DO LIST

"""

""" PROBLEMS
PB : ecriture() fait plus de 30 lignes
Ans : Resolu, j'ai divisé en une fonction ecriture et une fonction
affichage ce qui permet d'ouvrir le fichier de sortie meme pendant
que le l-systeme se trace.

PB : Il faut stocker les angles
Ans : Résolu, fallait définir les listes positions et angles séparemment
on obtient maintenant la bonne figure pour l'arbre (il correspond à l'image).
"""

""" NOTES
On pourrait mettre toutes les écritures fichiers dans une meme fonction DONE
faire une fonction d'erreurs DONE

j'ai modifié le fonctionnement de check(): à tester (ça fonctionne).
"""

""" EXTRAS
2 chararcteres en plus pour le grosseur du traits
full spectrum color

"""

""" CHARACTERES
a : avance en ecrivant
b : avance sans ecrire
+ : tourne a droite
- : tourne a gauche
* : fait demi tour
[ : stock une position et un angle
] : se rend a la position stockee et meme angle
& : diminue l epaisseur du trait
à : augmente l'epaisseur du trait
"""


####################################################
### FONCTIONS ###
####################################################

""" Permet de lancer le programme depuis la console avec les fichiers d'entree et sortie
verifie la syntaxe et renvoie le nom des fichiers d'entree et de sortie
"""
def unix():
    Arguments = sys.argv # Liste des arguments
    if len(Arguments) > 5:
        print("trop d'arguments (il faut ecrire : \nbase.py -i fichierEntree.txt -o fichierSortie.py)\n")
        exit()
    elif len(Arguments) < 5:
        print("arguments manquants (il faut ecrire : \nbase.py -i fichierEntree.txt -o fichierSortie.py)\n")
        exit()

    for i in range(len(Arguments)):
        if Arguments[1] != "-i":
            print("argument n°2 faux, ce devrait etre : -i\n")
            exit()
        if Arguments[3] != "-o":
            print("argument n°4 faux, ce devrait etre : -o\n")
            exit()
        nom_entree = Arguments[2]
        nom_sortie = Arguments[4]
    return(nom_entree, nom_sortie)


### LECTURE DU FICHIER ### -------------------------

""" Prend en parametre le fichier d'entree
Retourne les valeurs de chaque parametres en str
Et celle des regles sous forme de liste comprenant toutes les regles.
"""
def read(fichier) :
    for ligne in fichier :

        if "axiome" in ligne :
            axiome = clean(ligne, True)
        elif "taille" in ligne :
            taille = clean(ligne, True)
        elif "angle" in ligne :
            angle = clean(ligne, True)
        elif "niveau" in ligne :
            niveau = clean(ligne, True)

        elif "regle" in ligne :
            regle = []
            # Pour chaque ligne de regle on créé une liste avec deux elements
            # Un pour l'objet, et un pour la regle a lui appliquer
            for ligne in fichier :
                if "  " in ligne and not ("axiome" in ligne or "taille" in ligne or "angle" in ligne or "niveau" in ligne or "regle" in ligne):
                    regle.append(clean(ligne, False).split("="))

    return(axiome, regle, taille, angle, niveau)

""" Retourne la valeur apres le "="
Prend une ligne du fichier d entree en parametre.
le parametre "mode" vaut False si c'est pour les regles, True pour le reste
"""
def clean(ligne,mode):
    for character in ligne:
        if character in '\\" n':
            ligne = ligne.replace(character, "")
    ligne = ligne.replace("\n", "")
    contenu = ligne
    if mode:
        for i in range(len(ligne)):
            if ligne[i] == "=":
                contenu = ligne[i+1:]
    return(contenu)


### VERIFICATION ET AFFICHAGE DES ERREURS ###-------


# Fonctions de verifications du fichier d'entree.
""" Affiche une erreur si un parametre est faux.
"""
def affichageErreurs(angle, taille, niveau, axiome, regle):
    if not check(angle) :
        print("Erreur : angle incorrect.")
        exit()
    elif not check(taille) :
        print("Erreur : taille incorrect.")
        exit()
    elif not checkNiveau(niveau) :
        print("Erreur : niveau incorrect.")
        exit()
    elif not checkCode(axiome) :
        print("Erreur : axiome incorrect.")
        exit()
    elif not checkRegle(regle) :
        print("Erreur : regle incorrecte.")
        exit()


""" Retourne vrai seulemeunt si l'objet entré ne contient que
des chiffres et un seul point.
"""
def check(objet): # pour l'angle et la taille.
    point = 0

    for i in objet :
        if not i in "0123456789.":
            return(False)

        if i == ".":
            point += 1
            if point > 1:
                return(False)

    return(True)

def checkNiveau(objet):
    for i in objet :
        if not i in "0123456789":
            return(False)
    return(True)

""" Utilisé pour l'axiome et les regles
Retourne vrai seulemeunt si l'objet entré ne contient que
les caracteres autorisés
"""
def checkCode(objet) :
    for i in objet :
        if not i in "ab+-*[]&à" :
            return(False)
    return(True)

def checkRegle(objet) :
    pos = 0
    for i in objet :
        if len(i) != 3 :
            return(False)
        for j in i :
            if j=="" and pos == 0 :
                return(False)
            for k in j :
                if not k in "0123456789" and pos == 0 :
                    return(False)
                elif not k in "ab+-*[]&à" and pos > 0 :
                    return(False)
            pos += 1
        pos = 0
    return(True)


""" Retourne True s'il trouve autant de "[" que de "]"
"""
def checkCrochet(figure):
    count_o, count_f = 0, 0
    for i in figure:
        if i in "[":
            count_o += 1
        if i in "]":
            count_f += 1
    if count_o == count_f:
        return(True)
    else:
        return(False)



### TRADUCTION EN L-SYSTEME ###---------------------

""" Genere le L-systeme
Prend en argument le niveau, l'axiome et les regles
"""
def generator(axiome, regle, niveau) :
    figure = axiome
    if int(niveau) > 0 :
        for h in range(int(niveau)) :
            for i in regle :
                if 0<randint(0,100)<=int(i[0]) :
                    if i[1] in figure :
                        figure = figure.replace(i[1], i[2])
    return(figure)


### ECRITURE DU FICHIER ###-------------------------

""" Prend le L-systeme, la taille et l'angle en parametres
Ecrit dans le fichier de destination toutes les actions à effectuer et les parametres
Gere les crochets (retiennent la position et l'angle)
"""
def ecriture(figure, taille, angle, sortie) :
    grosseur, R, G, B = 1, 1.00, 0.00, 0.00
    sortie.write("from turtle import * \npositions, angles = [], [] \n")
    sortie.write("bgcolor(0.1,0.1,0.1); speed(0); register_shape('cat.gif'); shape('cat.gif'); pensize(" + str(grosseur) + ")\n")
    if int(input("voulez vous masquer la tortue? Oui:1 Non:0 : ")) == 1 : sortie.write("ht();\n")
    if not checkCrochet(figure): return(False) # Verifie les crochets
    for i in figure :
        R, G, B = newColour(R, G, B)
        sortie.write("color(" + str(R) + "," + str(G) + "," + str(B) + ");\n")
        if i == "a" : sortie.write("pd();fd(" + str(taille) + ");\n")
        elif i == "b" : sortie.write("pu();fd(" + str(taille) + ");\n")
        elif i == "+" : sortie.write("right(" + str(angle) + ");\n")
        elif i == "-" : sortie.write("left(" + str(angle) + ");\n")
        elif i == "*" : sortie.write("right(180);\n")
        elif i == "[" :
            sortie.write("positions.append(pos())\n")
            sortie.write("angles.append(heading())\n")
        elif i == "]" :
            sortie.write("pu(); setpos(positions[-1]); setheading(angles[-1]); pd();\n")
            sortie.write("positions.pop(-1)\n")
            sortie.write("angles.pop(-1)\n")
        elif i == "&" :
            grosseur += 1
            sortie.write("pensize(" + str(grosseur)+ ");\n")
        elif i == "à" and grosseur > 1 :
            grosseur -= 1
            sortie.write("pensize(" + str(grosseur)+ ");\n")
    sortie.write("exitonclick();")
    sortie.close()
    return(True)

def newColour(R,G,B): # rend le tracé multicolor !!!
    if R<1 and G <= 0:
        R += 0.05
    elif G<1 and B <= 0:
        G += 0.05
    elif R > 0 and G >= 1:
        R -= 0.05
    elif B<1 and R <= 0:
        B += 0.05
    elif G > 0 and B >= 1:
        G -= 0.05
    elif B > 0 and R >= 1:
        B -= 0.05
    return(R, G, B)



####################################################
### /// FONCTIONS ###
####################################################


# Fichiers entree et sortie
nom_entree, nom_sortie = unix()
entree = open(nom_entree,"r")
sortie = open(nom_sortie,"w")


# Liste des lignes du fichier d'entree
contenu_entree = entree.readlines()
entree.close()

# Assigne les valeurs du fichiers aux variables
axiome, regle, taille, angle, niveau = read(contenu_entree)

# Affiche les erreurs s'il y en a
affichageErreurs(angle, taille, niveau, axiome, regle)

# Genere le L-Systeme
figure = generator(axiome, regle, niveau)

# Ecrit le fichier de sortie
if not ecriture(figure, taille, angle, sortie):
    print("Erreur : il n'y a pas de position sauvegardee")
    exit()

# Lance le fichier de sortie créé pour afficher la figure
os.system("python3 "+str(nom_sortie))
