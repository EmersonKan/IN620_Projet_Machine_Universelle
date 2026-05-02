import sys

# Question 1: Structures de données
class MT:
    def __init__(self, transitions, k=1, initial='q0', final='q5'):
        self.transitions = transitions  # (état, symboles_lus) -> (nouvel_état, symboles, directions)
        self.k = k
        self.etat_initial = initial
        self.etat_final = final

 
class Configuration:
    def __init__(self, etat, rubans, positions):
        self.etat_courant = etat
        self.rubans = rubans  # Liste de listes
        self.positions = positions

# Question 2: Initialisation depuis un fichier
def lire_machine(contenu_fichier):
    transitions = {}
    etat_init = 'q0' 
    etat_final = 'q5'
    k_max = 1 
    
    # On nettoie les lignes (supprime les lignes vides et les commentaires)
    lignes = [l.strip() for l in contenu_fichier.split('\n') if l.strip() and not l.startswith('//')]
    
    i = 0
    while i < len(lignes):
        ligne = lignes[i]
        
        if ligne.startswith('init:'):
            etat_init = ligne.split(':')[1].strip()
        elif ligne.startswith('accept:'):
            etat_final = ligne.split(':')[1].strip()
        elif ligne.startswith('name:'):
            pass # On ignore simplement
        else:
            # On est sur une ligne de lecture (Ligne 1 d'un bloc)
            try:
                # Analyse ligne 1
                partie_g = [s.strip() for s in ligne.split(',')]
                if len(partie_g) > 1: # On vérifie que c'est bien une transition
                    etat_actuel = partie_g[0]
                    lus = tuple(partie_g[1:])
                    
                    k_actuel = len(lus)
                    if k_actuel > k_max: k_max = k_actuel
                    
                    # Analyse ligne 2 (l'action)
                    i += 1 # On passe à la ligne suivante
                    partie_d = [s.strip() for s in lignes[i].split(',')]
                    nouvel_etat = partie_d[0]
                    
                    # On découpe selon k_actuel
                    ecrits = tuple(partie_d[1 : 1 + k_actuel])
                    directions = tuple(partie_d[1 + k_actuel : 1 + 2 * k_actuel])
                    
                    transitions[(etat_actuel, lus)] = (nouvel_etat, ecrits, directions)
            except Exception as e:
                # En cas d'erreur de format, on passe
                pass
        
        i += 1 # On avance à la ligne suivante (ou à la ligne après le bloc de 2)

    return MT(transitions, k_max, initial=etat_init, final=etat_final)

def configuration_initiale(mot, machine):
    # Le mot d'entrée est sur le premier ruban, les autres sont vides
    rubans = [list(mot) if len(mot) > 0 else ['_']]
    for _ in range(machine.k - 1):
        rubans.append(['_'])
    
    # espace initial (ruban théoriquement infini)
    for r in rubans:
        r.extend(['_'] * 10)
        
    return Configuration(machine.etat_initial, rubans, [0] * machine.k)

# Question 3: Pas de calcul
def pas_de_calcul(config, machine):
    if config.etat_courant == machine.etat_final:
        return config
    
    # Lecture des têtes
    symboles_lus = []
    for i in range(machine.k):
        pos = config.positions[i]
        if pos >= len(config.rubans[i]): config.rubans[i].append('_')
        symboles_lus.append(config.rubans[i][pos])
    
    cle = (config.etat_courant, tuple(symboles_lus))
    
    if cle in machine.transitions:
        nouvel_etat, ecrits, directions = machine.transitions[cle]
        config.etat_courant = nouvel_etat
        
        for i in range(machine.k):
            config.rubans[i][config.positions[i]] = ecrits[i]
            # Mouvements : > (droite), < (gauche), - (immobile)
            if directions[i] == '>': config.positions[i] += 1
            elif directions[i] == '<': config.positions[i] -= 1
            elif directions[i] == '-':
                pass
                
            if config.positions[i] < 0:
                config.rubans[i].insert(0, '_')
                config.positions[i] = 0
    else:
        pass
        
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
        
    return "".join(config.rubans[0]).replace('_', '').strip() # Retourne le contenu du ruban 1

### Tests des fonctions ###

def verifier_simulateur():
    contenu_test = """name: Test Rapide
init: start
accept: stop

start, 1
stop, 0, >
"""
    print("--- Test ---")
    try:
        machine = lire_machine(contenu_test)
        res = simuler("1", machine, debug=True)
        
        # Nettoyage du résultat pour la comparaison
        res_propre = res.strip() 
        attendu = "0"
        
        print(f"Résultat obtenu: '{res_propre}'")
        print(f"Résultat attendu: '{attendu}'")
        
        # On compare les chaînes nettoyées
        if res_propre == attendu:
            print(" Succès : Le résultat est correct !")
        else:
            print(" Échec : Les chaînes ne correspondent pas exactement.")
            # Debug : affiche les codes ASCII pour voir les caractères invisibles
            print(f"Codes ASCII obtenus: {[ord(c) for c in res_propre]}")
            
    except Exception as e:
        print(f" Erreur système : {e}")
if __name__ == "__main__":
    verifier_simulateur()

def simuler_fichier(nom_fichier, entree):
    try:
        with open(nom_fichier, "r", encoding="utf-8") as f:
            contenu = f.read()
        ma_machine = lire_machine(contenu)
        print(f"--- Test de la machine : {nom_fichier} ---")
        print(f"Entrée : {entree}")
        resultat = simuler(entree, ma_machine, debug=True)  
        print(f"Résultat final : {resultat}")
        return resultat

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' est introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

simuler_fichier("question6_2.txt","111#1#101#1#111#11" )
