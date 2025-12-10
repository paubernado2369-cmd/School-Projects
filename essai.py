"""
Simulateur de Match de Football - Sans Classes
Architecture du projet avec dictionnaires et fonctions
"""

# ==================== CRÉATION DES DONNÉES ====================

def creer_joueur(nom, poste, vitesse=50, tir=50, passe=50, dribble=50, defense=50, physique=50):
    """Crée un dictionnaire représentant un joueur"""
    return {
        'nom': nom,
        'poste': poste,  # 'GK', 'DEF', 'MIL', 'ATT'
        'stats': {
            'vitesse': vitesse,
            'tir': tir,
            'passe': passe,
            'dribble': dribble,
            'defense': defense,
            'physique': physique
        },
        'cartons_jaunes': 0,
        'carton_rouge': False,
        'blesse': False,
        'energie': 100,
        'buts': 0,
        'passes_decisives': 0
    }


def creer_equipe(nom, formation="4-4-2"):
    """Crée un dictionnaire représentant une équipe"""
    return {
        'nom': nom,
        'formation': formation,
        'joueurs_terrain': [],  # Liste de 11 joueurs max
        'remplacants': [],
        'score': 0,
        'statistiques': {
            'tirs': 0,
            'tirs_cadres': 0,
            'possession': 0,
            'passes_reussies': 0,
            'fautes': 0
        }
    }


def creer_match(equipe_domicile, equipe_exterieur):
    """Crée un dictionnaire représentant un match"""
    return {
        'equipe_domicile': equipe_domicile,
        'equipe_exterieur': equipe_exterieur,
        'minute': 0,
        'evenements': [],
        'termine': False
    }


# ==================== GESTION DES JOUEURS ====================

def diminuer_energie(joueur, montant):
    """Réduit l'énergie d'un joueur"""
    joueur['energie'] = max(0, joueur['energie'] - montant)


def donner_carton(joueur, couleur):
    """Donne un carton à un joueur"""
    if couleur == "jaune":
        joueur['cartons_jaunes'] += 1
        if joueur['cartons_jaunes'] >= 2:
            joueur['carton_rouge'] = True
            return f"{joueur['nom']} reçoit un second carton jaune et est expulsé!"
        return f"Carton jaune pour {joueur['nom']}"
    elif couleur == "rouge":
        joueur['carton_rouge'] = True
        return f"Carton rouge direct pour {joueur['nom']}! Il est expulsé!"


def blesser_joueur(joueur):
    """Marque un joueur comme blessé"""
    joueur['blesse'] = True
    return f"{joueur['nom']} est blessé et doit sortir!"


def peut_jouer(joueur):
    """Vérifie si un joueur peut continuer à jouer"""
    return not joueur['carton_rouge'] and not joueur['blesse']


# ==================== GESTION DE L'ÉQUIPE ====================

def ajouter_joueur_terrain(equipe, joueur):
    """Ajoute un joueur sur le terrain (max 11)"""
    if len(equipe['joueurs_terrain']) < 11:
        equipe['joueurs_terrain'].append(joueur)
        return True
    return False


def ajouter_remplacant(equipe, joueur):
    """Ajoute un joueur sur le banc"""
    equipe['remplacants'].append(joueur)


def effectuer_remplacement(equipe, joueur_sortant, joueur_entrant):
    """Effectue un remplacement"""
    if joueur_sortant in equipe['joueurs_terrain'] and joueur_entrant in equipe['remplacants']:
        equipe['joueurs_terrain'].remove(joueur_sortant)
        equipe['remplacants'].remove(joueur_entrant)
        equipe['joueurs_terrain'].append(joueur_entrant)
        return f"Remplacement: {joueur_sortant['nom']} sort, {joueur_entrant['nom']} entre"
    return "Remplacement impossible"


def obtenir_joueurs_actifs(equipe):
    """Retourne la liste des joueurs pouvant jouer"""
    return [j for j in equipe['joueurs_terrain'] if peut_jouer(j)]


def calculer_force_equipe(equipe):
    """Calcule la force globale de l'équipe"""
    joueurs_actifs = obtenir_joueurs_actifs(equipe)
    if not joueurs_actifs:
        return 0
    
    total = 0
    for joueur in joueurs_actifs:
        stats = joueur['stats']
        moyenne = sum(stats.values()) / len(stats)
        # Bonus d'énergie
        moyenne *= (joueur['energie'] / 100)
        total += moyenne
    
    return total / len(joueurs_actifs)


# ==================== SIMULATION DES ACTIONS ====================

import random


def tenter_tir(joueur, gardien):
    """Simule une tentative de tir"""
    qualite_tir = joueur['stats']['tir'] + random.randint(-20, 20)
    qualite_arret = gardien['stats']['defense'] + random.randint(-20, 20)
    
    cadre = qualite_tir > 30
    but = cadre and qualite_tir > qualite_arret
    
    return {
        'cadre': cadre,
        'but': but,
        'tireur': joueur['nom'],
        'gardien': gardien['nom']
    }


def tenter_passe(passeur, receveur):
    """Simule une passe"""
    qualite_passe = passeur['stats']['passe'] + random.randint(-15, 15)
    reussite = qualite_passe > 50
    return reussite


def verifier_blessure(joueur):
    """Vérifie si un joueur se blesse (basé sur physique et énergie)"""
    chance_blessure = (100 - joueur['stats']['physique']) + (100 - joueur['energie'])
    return random.randint(0, 1000) < chance_blessure


def verifier_carton(joueur, type_action):
    """Vérifie si une action mérite un carton"""
    # type_action: 'faute', 'faute_grave', 'simulation'
    agressivite = 100 - joueur['stats']['defense']  # Plus la défense est faible, plus agressif
    
    if type_action == 'faute':
        chance = agressivite / 10
        rand = random.randint(0, 100)
        if rand < chance:
            return 'jaune'
    elif type_action == 'faute_grave':
        return 'rouge' if random.randint(0, 100) < 30 else 'jaune'
    
    return None


# ==================== SIMULATION DU MATCH ====================

def simuler_minute(match):
    """Simule une minute de jeu"""
    match['minute'] += 1
    equipes = [match['equipe_domicile'], match['equipe_exterieur']]
    
    # Possession aléatoire
    equipe_attaque = random.choice(equipes)
    equipe_defense = match['equipe_exterieur'] if equipe_attaque == match['equipe_domicile'] else match['equipe_domicile']
    
    joueurs_attaque = obtenir_joueurs_actifs(equipe_attaque)
    joueurs_defense = obtenir_joueurs_actifs(equipe_defense)
    
    if not joueurs_attaque or not joueurs_defense:
        return
    
    # Événements possibles
    if random.randint(0, 100) < 10:  # 10% de chance d'action
        evenement = simuler_action(match, equipe_attaque, equipe_defense, joueurs_attaque, joueurs_defense)
        if evenement:
            match['evenements'].append(evenement)
    
    # Diminuer l'énergie
    for joueur in joueurs_attaque + joueurs_defense:
        diminuer_energie(joueur, random.uniform(0.5, 1.5))


def simuler_action(match, equipe_attaque, equipe_defense, joueurs_attaque, joueurs_defense):
    """Simule une action de jeu"""
    attaquant = random.choice([j for j in joueurs_attaque if j['poste'] in ['ATT', 'MIL']])
    gardien = next((j for j in joueurs_defense if j['poste'] == 'GK'), joueurs_defense[0])
    defenseur = random.choice([j for j in joueurs_defense if j['poste'] in ['DEF', 'MIL']])
    
    action_type = random.choice(['tir', 'faute', 'blessure'])
    
    if action_type == 'tir':
        resultat = tenter_tir(attaquant, gardien)
        equipe_attaque['statistiques']['tirs'] += 1
        
        if resultat['cadre']:
            equipe_attaque['statistiques']['tirs_cadres'] += 1
        
        if resultat['but']:
            equipe_attaque['score'] += 1
            attaquant['buts'] += 1
            return {
                'minute': match['minute'],
                'type': 'but',
                'description': f"⚽ BUT! {attaquant['nom']} marque pour {equipe_attaque['nom']}!",
                'score': f"{match['equipe_domicile']['score']}-{match['equipe_exterieur']['score']}"
            }
        else:
            return {
                'minute': match['minute'],
                'type': 'tir',
                'description': f"Tir de {attaquant['nom']} {'arrêté' if resultat['cadre'] else 'à côté'}!"
            }
    
    elif action_type == 'faute':
        equipe_defense['statistiques']['fautes'] += 1
        carton = verifier_carton(defenseur, 'faute')
        if carton:
            message = donner_carton(defenseur, carton)
            return {
                'minute': match['minute'],
                'type': f'carton_{carton}',
                'description': f"🟨 {message}" if carton == 'jaune' else f"🟥 {message}"
            }
    
    elif action_type == 'blessure':
        if verifier_blessure(attaquant):
            message = blesser_joueur(attaquant)
            return {
                'minute': match['minute'],
                'type': 'blessure',
                'description': f"🚑 {message}"
            }
    
    return None


def simuler_match_complet(match, duree=90):
    """Simule un match complet"""
    for _ in range(duree):
        simuler_minute(match)
    
    match['termine'] = True
    return generer_rapport_match(match)


def generer_rapport_match(match):
    """Génère un rapport du match"""
    rapport = []
    rapport.append(f"\n{'='*50}")
    rapport.append(f"MATCH TERMINÉ")
    rapport.append(f"{match['equipe_domicile']['nom']} {match['equipe_domicile']['score']} - {match['equipe_exterieur']['score']} {match['equipe_exterieur']['nom']}")
    rapport.append(f"{'='*50}\n")
    
    rapport.append("ÉVÉNEMENTS DU MATCH:")
    for evt in match['evenements']:
        rapport.append(f"[{evt['minute']}''] {evt['description']}")
    
    rapport.append(f"\n{'='*50}")
    rapport.append("STATISTIQUES:")
    for equipe in [match['equipe_domicile'], match['equipe_exterieur']]:
        rapport.append(f"\n{equipe['nom']}:")
        rapport.append(f"  Tirs: {equipe['statistiques']['tirs']} (dont {equipe['statistiques']['tirs_cadres']} cadrés)")
        rapport.append(f"  Fautes: {equipe['statistiques']['fautes']}")
    
    return "\n".join(rapport)


# ==================== EXEMPLE D'UTILISATION ====================

if __name__ == "__main__":
    # Créer les joueurs de l'équipe 1
    equipe1 = creer_equipe("FC Python", "4-3-3")
    
    # Gardien
    ajouter_joueur_terrain(equipe1, creer_joueur("Dubois", "GK", vitesse=60, defense=85, physique=80))
    
    # Défenseurs
    ajouter_joueur_terrain(equipe1, creer_joueur("Martin", "DEF", vitesse=70, defense=80, physique=75))
    ajouter_joueur_terrain(equipe1, creer_joueur("Bernard", "DEF", vitesse=65, defense=82, physique=78))
    ajouter_joueur_terrain(equipe1, creer_joueur("Petit", "DEF", vitesse=68, defense=79, physique=76))
    ajouter_joueur_terrain(equipe1, creer_joueur("Durand", "DEF", vitesse=72, defense=77, physique=74))
    
    # Milieux
    ajouter_joueur_terrain(equipe1, creer_joueur("Lefebvre", "MIL", passe=80, dribble=75, vitesse=73))
    ajouter_joueur_terrain(equipe1, creer_joueur("Moreau", "MIL", passe=78, dribble=72, vitesse=70))
    ajouter_joueur_terrain(equipe1, creer_joueur("Simon", "MIL", passe=76, dribble=70, vitesse=75))
    
    # Attaquants
    ajouter_joueur_terrain(equipe1, creer_joueur("Laurent", "ATT", tir=85, vitesse=88, dribble=82))
    ajouter_joueur_terrain(equipe1, creer_joueur("Michel", "ATT", tir=83, vitesse=86, dribble=80))
    ajouter_joueur_terrain(equipe1, creer_joueur("Garcia", "ATT", tir=82, vitesse=85, dribble=81))
    
    # Créer l'équipe 2
    equipe2 = creer_equipe("JS Code", "4-4-2")
    
    ajouter_joueur_terrain(equipe2, creer_joueur("Lopez", "GK", vitesse=58, defense=83, physique=79))
    ajouter_joueur_terrain(equipe2, creer_joueur("Rodriguez", "DEF", vitesse=69, defense=81, physique=77))
    ajouter_joueur_terrain(equipe2, creer_joueur("Martinez", "DEF", vitesse=67, defense=80, physique=75))
    ajouter_joueur_terrain(equipe2, creer_joueur("Sanchez", "DEF", vitesse=70, defense=78, physique=76))
    ajouter_joueur_terrain(equipe2, creer_joueur("Perez", "DEF", vitesse=71, defense=79, physique=73))
    
    ajouter_joueur_terrain(equipe2, creer_joueur("Gonzalez", "MIL", passe=77, dribble=73, vitesse=72))
    ajouter_joueur_terrain(equipe2, creer_joueur("Fernandez", "MIL", passe=79, dribble=74, vitesse=71))
    ajouter_joueur_terrain(equipe2, creer_joueur("Ruiz", "MIL", passe=75, dribble=71, vitesse=74))
    ajouter_joueur_terrain(equipe2, creer_joueur("Diaz", "MIL", passe=76, dribble=72, vitesse=73))
    
    ajouter_joueur_terrain(equipe2, creer_joueur("Torres", "ATT", tir=84, vitesse=87, dribble=81))
    ajouter_joueur_terrain(equipe2, creer_joueur("Ramirez", "ATT", tir=81, vitesse=84, dribble=79))
    
    # Créer et simuler le match
    match = creer_match(equipe1, equipe2)
    rapport = simuler_match_complet(match, duree=90)
    print(rapport)




"""
import random
import time

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
    nouvelle_distance = distance + random.randint(-5, 40)
    
    if reussite:
        return True, nouvelle_distance, f"{passeur['prenom']} réussit une passe vers {receveur['prenom']} (distance: {nouvelle_distance}m)"
    else:
        return False, 100, f"{passeur['prenom']} rate sa passe !"


def tenter_tir(tireur, distance, equipe_index):
    """Simule un tir"""
    qualite_tir = tireur['stats']['att'] + random.randint(-2 * distance, 15)
    reussite = qualite_tir > 50
    
    if reussite:
        resultat[equipe_index] += 1
        return True, 100, f"⚽ BUT ! {tireur['prenom']} tire et marque !"
    else:
        return False, 100, f"{tireur['prenom']} tire mais rate..."

def simule_action(joueur_b, distance, equipe_actuelle, equipe_index):
    """Choisit une action en fonction de la distance"""
    avoir_ballon = True
    actions_effectuees = []
    max_passes = 5  # Limite le nombre de passes pour éviter une boucle infinie
    nombre_passes = 0

    while avoir_ballon and nombre_passes < max_passes:
        if distance > 30:  
            action = random.choices(["passe", "tir"], weights=[90, 10])[0]
        elif distance > 15:
            action = random.choices(["passe", "tir"], weights=[60, 40])[0]
        else:
            action = random.choices(["passe", "tir"], weights=[30, 70])[0]

        if action == "passe":
            receveur = random.choice(equipe_actuelle)
            reussite, nouvelle_distance, message = tenter_passe(joueur_b, receveur, distance)
            actions_effectuees.append(message)
            
            if reussite:
                distance = nouvelle_distance
                joueur_b = receveur  # Le receveur a maintenant le ballon
                nombre_passes += 1
            else:
                avoir_ballon = False
                
        else:  # tir
            reussite, nouvelle_distance, message = tenter_tir(joueur_b, distance, equipe_index)
            actions_effectuees.append(message)
            avoir_ballon = False  # Après un tir, on perd toujours le ballon

    return avoir_ballon, actions_effectuees


# ====================== MATCH ====================

def match():
    """Simule un match de 90 minutes"""
    equipe_actuelle = equipe_une
    equipe_index = 0  # 0 = équipe 1, 1 = équipe 2
    
    print("=" * 60)
    print("🏆 DÉBUT DU MATCH 🏆")
    print("=" * 60)
    print()
    
    for minute in range(1, 91):
        joueur = random.choice(equipe_actuelle)
        distance_initiale = random.randint(30, 80)  # Distance au but
        
        garde_ballon, actions = simule_action(joueur, distance_initiale, equipe_actuelle, equipe_index)
        
        # Affichage des actions importantes (environ 1 action sur 10)
        if random.random() < 0.15 or resultat[0] + resultat[1] > 0:  # Affiche plus souvent s'il y a des buts
            print(f"⏱️  Minute {minute} {'─' * 40}")
            for action in actions:
                print(f"   {action}")
        
        # Si l'action échoue, la possession change
        if not garde_ballon:
            if equipe_actuelle == equipe_une:
                equipe_actuelle = equipe_deux
                equipe_index = 1
                if random.random() < 0.05:  # Affiche parfois le changement
                    print("   🔄 L'équipe 2 récupère le ballon !")
            else:
                equipe_actuelle = equipe_une
                equipe_index = 0
                if random.random() < 0.05:
                    print("   🔄 L'équipe 1 récupère le ballon !")
        
        # Affiche le score à certains moments clés
        if minute in [15, 30, 45, 60, 75, 90]:
            print(f"\n📊 Score à la {minute}ème minute : Équipe 1 [{resultat[0]}] - [{resultat[1]}] Équipe 2")
            print()
    
    print("\n" + "=" * 60)
    print("🏁 FIN DU MATCH 🏁")
    print("=" * 60)
    print(f"SCORE FINAL : Équipe 1 [{resultat[0]}] - [{resultat[1]}] Équipe 2")
    print("=" * 60)
    
    # Annonce le vainqueur
    if resultat[0] > resultat[1]:
        print("🏆 VICTOIRE DE L'ÉQUIPE 1 ! 🏆")
    elif resultat[1] > resultat[0]:
        print("🏆 VICTOIRE DE L'ÉQUIPE 2 ! 🏆")
    else:
        print("🤝 MATCH NUL ! 🤝")

# Lancer la simulation
match()


"""
