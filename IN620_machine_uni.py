import sys

# Question 1: Structures de données
class MT:
    def __init__(self, transitions, k=1):
        self.transitions = transitions  # (état, symboles_lus) -> (nouvel_état, symboles, directions)
        self.k = k
        self.etat_initial = 'I'
        self.etat_final = 'F'

class Configuration:
    def __init__(self, etat, rubans, positions):
        self.etat_courant = etat
        self.rubans = rubans  # Liste de listes
        self.positions = positions

# Question 2: Initialisation depuis un fichier
def lire_machine(contenu_fichier):
    transitions = {}
    k = 1
    lignes = contenu_fichier.strip().split('\n')
    
    for ligne in lignes:
        ligne = ligne.split('//')[0].strip() # supprimer les commentaires
        if not ligne: continue
        
        # Format attendu: etat_lu,symb1,symb2... -> etat_suiv,ecrit1,ecrit2...,dir1,dir2...
        try:
            gauche, droite = ligne.split('->')
            parties_g = gauche.strip().split(',')
            parties_d = droite.strip().split(',')
            
            etat_actuel = parties_g[0]
            lus = tuple(parties_g[1:])
            k = len(lus) # Détermine le nombre de rubans 
            
            nouvel_etat = parties_d[0]
            ecrits = tuple(parties_d[1:1+k])
            dirs = tuple(parties_d[1+k:])
            
            transitions[(etat_actuel, lus)] = (nouvel_etat, ecrits, dirs)
        except:
            continue
            
    return MT(transitions, k)

def configuration_initiale(mot, machine):
    # Le mot d'entrée est sur le premier ruban, les autres sont vides
    rubans = [list(mot) if len(mot) > 0 else ['_']]
    for _ in range(machine.k - 1):
        rubans.append(['_'])
    
    # On s'assure d'avoir un peu d'espace (le ruban est théoriquement infini)
    for r in rubans:
        r.extend(['_'] * 10)
        
    return Configuration(machine.etat_initial, rubans, [0] * machine.k)

# Question 3: Pas de calcul
def pas_de_calcul(config, machine):
    if config.etat_courant == machine.etat_final:
        return config
    
    # Lire les symboles sous les têtes
    symboles_lus = []
    for i in range(machine.k):
        pos = config.positions[i]
        # Extension dynamique du ruban si nécessaire
        if pos >= len(config.rubans[i]):
            config.rubans[i].append('_')
        symboles_lus.append(config.rubans[i][pos])
    
    cle = (config.etat_courant, tuple(symboles_lus))
    
    if cle in machine.transitions:
        nouvel_etat, ecrits, directions = machine.transitions[cle]
        config.etat_courant = nouvel_etat
        
        for i in range(machine.k):
            # Écriture
            config.rubans[i][config.positions[i]] = ecrits[i]
            # Mouvement
            if directions[i] == '>': config.positions[i] += 1
            elif directions[i] == '<': config.positions[i] -= 1
            # Sécurité position négative
            if config.positions[i] < 0:
                config.rubans[i].insert(0, '_')
                config.positions[i] = 0
    else:
        # Si aucune transition, on bloque (ou on considère un échec)
        config.etat_courant = machine.etat_final # Pour cet exercice, on force l'arrêt
        
    return config

# Question 5: Affichage
def afficher_config(config):
    print(f"État: {config.etat_courant}")
    for i in range(len(config.rubans)):
        # On nettoie l'affichage des '_' superflus à la fin
        ruban_str = "".join(config.rubans[i]).rstrip('_') + "_"
        pointeur = " " * config.positions[i] + "^"
        print(f"R{i}: {ruban_str}")
        print(f"    {pointeur}")
    print("-" * 20)

# Question 4: Simulation complète
def simuler(mot, machine, debug=False):
    config = configuration_initiale(mot, machine)
    if debug: afficher_config(config)
    
    while config.etat_courant != machine.etat_final:
        config = pas_de_calcul(config, machine)
        if debug: afficher_config(config)
        
    return "".join(config.rubans[0]).strip('_') # Retourne le contenu du ruban 1

### Tests des fonctions ###

# Exemple de description au format Turing Machine Simulator 
# Machine de Turing qui incrémente un nombre binaire de 1.
description_exemple = """
I,0 -> I,0,>
I,1 -> I,1,>
I,_ -> carry,_,<
carry,1 -> carry,0,<
carry,0 -> F,1,>
carry,_ -> F,1,>
"""

def test_simulateur():
    print("=== Test de la Machine de Turing (Incrémentation Binaire) ===")
    
    # 1. Chargement
    machine = lire_machine(description_exemple)
    print(f"Machine chargée avec {machine.k} ruban(s).")
    
    # 2. Test sur le mot "101"
    mot_test = "101"
    print(f"Entrée: {mot_test}")
    
    # 3. Exécution avec affichage des étapes (Question 5)
    resultat = simuler(mot_test, machine, debug=True)
    
    print(f"Résultat final sur ruban 1: {resultat}")
    assert "110" in resultat
    print("\nTest réussi !")

if __name__ == "__main__":
    test_simulateur()
