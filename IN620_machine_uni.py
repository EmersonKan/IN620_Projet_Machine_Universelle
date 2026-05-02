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
    etat_init = 'q0' # valeurs par défaut 
    etat_final = 'q5'
    k = 1
    
    lignes = [l.strip() for l in contenu_fichier.split('\n') if l.strip() and not l.startswith('//')]
    
    i = 0
    while i < len(lignes):
        ligne = lignes[i]
        
        # Lecture des paramètres de la machine
        if ligne.startswith('init:'):
            etat_init = ligne.split(':')[1].strip()
            i += 1
        elif ligne.startswith('accept:'):
            etat_final = ligne.split(':')[1].strip()
            i += 1
        elif ligne.startswith('name:'):
            i += 1
        else:
            try:
                partie_g = ligne.split(',')
                etat_actuel = partie_g[0].strip()
                lus = tuple(s.strip() for s in partie_g[1:])
                k = len(lus)
                
                partie_d = lignes[i+1].split(',')
                nouvel_etat = partie_d[0].strip()
                ecrits = tuple(partie_d[1:1+k])
                # Conversion des directions : > en R, < en L, - en S
                dir = tuple(parts_d[1+k:1+2*k])
                
                transitions[(etat_actuel, lus)] = (nouvel_etat, ecrits, dir)
                i += 2 # On avance de deux lignes car une transition = 2 lignes
            except (IndexError, ValueError):
                i += 1

    return MT(transitions, k, initial=etat_init, final=etat_final)

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
        
    return "".join(config.rubans[0]).strip('_') # Retourne le contenu du ruban 1

### Tests des fonctions ###

def verifier_simulateur():
    contenu_test = """name: Test Rapide
init: start
accept: stop

start, 1
stop, 0, >
"""
    print("--- Test de lecture du nouveau format ---")
    try:
        machine = lire_machine(contenu_test)
        print(f"Machine chargée ! État initial: {machine.etat_initial}, Final: {machine.etat_final}")
        
        # Test de simulation simple
        res = simuler("1", machine, debug=True)
        print(f"Résultat pour '1': {res} (Attendu: '0')")
        
        if res == "0":
            print("✅ Succès : Le format deux lignes est bien géré.")
        else:
            print("❌ Échec : Le résultat est incorrect.")
            
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")

if __name__ == "__main__":
    verifier_simulateur()
