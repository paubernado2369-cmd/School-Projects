





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

import random

# ==================== DONNÉES ====================

equipe_une = [
    {'nom': 'BERNADO', 'prenom': 'PAU', 'poste': 'Milieu', 'stats': {'def': 56, 'att': 54, 'endurance': 49, 'passe': 55}},
    {'nom': 'CHINOIS', 'prenom': 'YFLYF', 'poste': 'Attaquant', 'stats': {'def': 60, 'att': 53, 'endurance': 60, 'passe': 50}},
    {'nom': 'BEVU', 'prenom': 'YFLYF', 'poste': 'Gardien', 'stats': {'def': 46, 'att': 47, 'endurance': 63, 'passe': 40}},
]

equipe_deux = [
    {'nom': 'Sainox', 'prenom': 'Saina', 'poste': 'Milieu', 'stats': {'def': 56, 'att': 54, 'endurance': 49, 'passe': 55}},
    {'nom': 'CHINOIS', 'prenom': 'Andrew', 'poste': 'Attaquant', 'stats': {'def': 60, 'att': 53, 'endurance': 60, 'passe': 50}},
    {'nom': 'Cavu', 'prenom': 'Favé', 'poste': 'Gardien', 'stats': {'def': 46, 'att': 47, 'endurance': 63, 'passe': 40}},
]

resultat = [0, 0]  # score [équipe 1, équipe 2]

# ==================== ACTIONS ====================

def tenter_passe(passeur, receveur, distance):
    """Simule une passe"""
    qualite_passe = passeur['stats']['passe'] + random.randint(-15, 15)
    reussite = qualite_passe > 50
    distance += random.randint(-5, 40)
    if reussite:
        return True, f"{passeur['prenom']} réussit une passe vers {receveur['prenom']} (distance {distance})"
    else:
        distance = 100 - distance
        return False, f"{passeur['prenom']} rate sa passe !"



def tenter_tir(tireur, distance, equipe_index):
    """Simule un tir"""
    qualite_tir = tireur['stats']['att'] + random.randint(-2 * distance, 15)
    reussite = qualite_tir > 50
    if reussite:
        resultat[equipe_index] += 1
        return True, f"{tireur['prenom']} tire et marque !"
    else:
        return False, f"{tireur['prenom']} tire mais rate..."



def simule_action(joueur_b, distance, equipe_actuelle, equipe_index):
    """Choisit une action en fonction de la distance"""
    avoir_ballon = True

    while avoir_ballon

    if distance > 30:  
        action = random.choices(["passe", "tir"], weights=[90, 10])[0]
    elif distance > 15:
        action = random.choices(["passe", "tir"], weights=[60, 40])[0]
    else:
        action = random.choices(["passe", "tir"], weights=[30, 70])[0]

    if action == "passe":
        receveur = random.choice(equipe_actuelle)
        return tenter_passe(joueur_b, receveur, distance)
    else:
        return tenter_tir(joueur_b, distance, equipe_index)

# ====================== MATCH ====================

def match():
    """Simule un match de 10 minutes (exemple)"""
    equipe_actuelle = equipe_une
    equipe_index = 0  # 0 = équipe 1, 1 = équipe 2
    
    for minute in range(1, 11):
        joueur = random.choice(equipe_actuelle)
        reussite, action = simule_action(joueur, 40, equipe_actuelle, equipe_index)
        print(f"Minute {minute}: {action}")
        
        # Si l'action échoue, la possession change
        if not reussite:
            if equipe_actuelle == equipe_une:
                equipe_actuelle = equipe_deux
                equipe_index = 1
                print(">>> L'équipe 2 récupère le ballon !")
            else:
                equipe_actuelle = equipe_une
                equipe_index = 0
                print(">>> L'équipe 1 récupère le ballon !")
    
    print("\n=== SCORE FINAL ===")
    print(f"Équipe 1 : {resultat[0]} | Équipe 2 : {resultat[1]}")

# Lancer la simulation
match()


