import random


minute = 0
joueur_ballon = None
equipe_ballon = []

#def blesser_joueur(joueur):
#    """Marque un joueur comme blessé"""
#    joueur['blesse'] = True
#    return f"{joueur['nom']} est blessé et doit sortir!"
#
#def donner_carton(joueur, couleur):
#    """Donne un carton à un joueur"""
#    if couleur == "jaune":
#        joueur['cartons_jaunes'] += 1
#        if joueur['cartons_jaunes'] >= 2:
#            joueur['carton_rouge'] = True
#            return f"{joueur['nom']} reçoit un second carton jaune et est expulsé!"
#        return f"Carton jaune pour {joueur['nom']}"
#    elif couleur == "rouge":
#        joueur['carton_rouge'] = True
#        return f"Carton rouge direct pour {joueur['nom']}! Il est expulsé!"


# ==================== SIMULATION DES ACTIONS ====================


def simule_action(joueur_b, distance):
    action = random.randint(1,5)
    
    if action == 1 : 
        reussite, receveur, distance = tenter_passe(joueur_b, random.choice(equipe_ballon), distance)
        return reussite, receveur, distance
    
    if action == 2 : 
        reussite, receveur, distance = tenter_passe(joueur_b, random.choice(equipe_ballon), distance)
        return reussite, receveur, distance


def tenter_passe(passeur, receveur, distance):
    """Simule une passe"""
    qualite_passe = passeur['stats']['passe'] + random.randint(-15, 15)
    reussite = qualite_passe > 50
    distance += random.randint(-5, 40)
    return reussite, receveur ,distance

def tenter_tir(tireur, distance):
    qualite_tir = tireur['stats']['tir'] + random.randint(2 * distance * -1, 15)  
    reussite = qualite_tir > 50
    return

#def verifier_blessure(joueur):
    """Vérifie si un joueur se blesse (basé sur physique et énergie)"""
    chance_blessure = (100 - joueur['stats']['physique']) + (100 - joueur['energie'])
    return random.randint(0, 1000) < chance_blessure


def simuler_minute(minute, joueur, distance):
    print(minute)

    simule_action(joueur, distance)



