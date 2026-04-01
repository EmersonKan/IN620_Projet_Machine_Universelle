#Question 1 : Structure de données pour la machine de Turing

class MT:
    def __init__(self, etats, alphabet, transitions, etat_initial, etat_final, k):
        self.etats = etats
        self.alphabet = alphabet
        self.transitions = transitions  # Dictionnaire : (etat, symbole_lu) -> (nouvel_etat, symbole_ecrit, direction)
        self.etat_initial = etat_initial
        self.etat_final = etat_final
        self.k = k

class Configuration:
    def __init__(self, etat_courant, rubans, positions):
        self.etat_courant = etat_courant
        self.rubans = rubans  # Liste de listes (chaque ruban est une liste de caractères)
        self.positions = positions  # Liste d'entiers (position de la tête de lecture pour chaque ruban)

#Question 2 : Initialisation depuis un fichier

def lire_machine(fichier):
    with open(fichier, 'r') as f:
        lignes = f.readlines()
    # Logique pour parser les lignes et créer une instance de MT
    # Exemple simplifié :
    etats = set()
    alphabet = set()
    transitions = {}
    for ligne in lignes:
        if ligne.startswith('State:'):
            etats.add(ligne.split()[1])
        elif ligne.startswith('Alphabet:'):
            alphabet.update(ligne.split()[1:])
        elif ligne.startswith('Transition:'):
            # Logique pour extraire la transition
            pass
    return MT(etats, alphabet, transitions, 'I', 'F', k=1)

def configuration_initiale(mot, machine):
    rubans = [list(mot) + ['_'] * 100]  # Exemple : un seul ruban, rempli de '_' après le mot
    positions = [0]  # Tête de lecture au début
    return Configuration(machine.etat_initial, rubans, positions)

#Question 3 : Exécution d'un pas de calcul

def pas_de_calcul(config, machine):
    if config.etat_courant == machine.etat_final:
        return config  # Arrêt si état final
    etat = config.etat_courant
    symboles_lus = [config.rubans[i][config.positions[i]] for i in range(machine.k)]
    # Chercher la transition
    cle = (etat, tuple(symboles_lus))
    if cle in machine.transitions:
        nouvel_etat, symboles_ecrits, directions = machine.transitions[cle]
        # Mettre à jour les rubans et positions
        for i in range(machine.k):
            config.rubans[i][config.positions[i]] = symboles_ecrits[i]
            if directions[i] == 'R':
                config.positions[i] += 1
            elif directions[i] == 'L':
                config.positions[i] -= 1
        config.etat_courant = nouvel_etat
    return config

#Question 4 : Simulation complète

def simuler(mot, machine):
    config = configuration_initiale(mot, machine)
    while config.etat_courant != machine.etat_final:
        config = pas_de_calcul(config, machine)
    return config

#Question 5 : Affichage des configurations

def afficher_config(config):
    print(f"État: {config.etat_courant}")
    for i, ruban in enumerate(config.rubans):
        print(f"Ruban {i}: {''.join(ruban)} (Position: {config.positions[i]})")
