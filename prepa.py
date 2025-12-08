"""
 Mon Projet en NSI
 MATCH DE FOOTBALL

"""

from match import *
import random
import time


NOMS_ALEATOIRS = ["BEVU", "CHINOIS"]
PRENOMS_ALEATOIRS = ["YFLYF", "JHGGLYGLYG"]

mon_equipe = []



## CREER DE MANIERE ALEATOIRE UN JOUEUR ##
def creer_joueur():
    
    ## FONCTION POUR DONNER DES VALEURS REALISTES ##
    def valeur_gaussienne(moy=50, sigma=7, minimum=0, maximum=100): # calcul de sigma par IA (C'est programme )
        while True:
            x = random.gauss(moy, sigma)
            if minimum <= x <= maximum:
                return int(x)

    joueur = {
        "nom": random.choice(NOMS_ALEATOIRS),   
        "prenom": random.choice(PRENOMS_ALEATOIRS),  
        "poste": random.choice(["Attaquant", "Défenseur", "Milieu", "Gardien"]),
        "stats": {
            "def": valeur_gaussienne(),
            "att": valeur_gaussienne(),
            "endurance": valeur_gaussienne()
        }
    }
     
    return joueur
    

## CREER UNE EQUIPE 
def creer_equipe():
    for _ in range(15):
        mon_equipe.append(creer_joueur())

    return mon_equipe


# def mon_equipe



def main():



    prep_av_match = True


    ## BOUCLE DE PREPARATION D'AVANT MATCH
    while prep_av_match:
        print("-----------------------")
        print(" PREPA D'AVANT MATCH")
        print("-----------------------")
        print(" ")
        print("1/ TACTIQUE")
        print("2/ COMPOSITION EQUIPE")
        action = input(" QU'EST CE QUE TU VEUX FAIRE, COACH ?  =>  ")  ####### !! A FAIRE, BOUCLE WHILE POUR ETRE SUR QUE L ACTION EST BONNE 

        if action = 1:
            pass




