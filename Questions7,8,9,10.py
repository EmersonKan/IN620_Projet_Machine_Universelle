import os


#Q7

def codage(chemin):
    #Vérification de l'existence du fichier
    if not os.path.exists(chemin):
        raise FileNotFoundError(f"Le fichier {chemin} n'existe pas.")

    #Ouverture en lecture du fichier et filtrage
    lignes_filtrees = []
    with open(chemin, 'r', encoding='utf-8-sig') as f:
        for ligne in f:
            ligne = ligne.strip()
            # Ignorer les lignes vides ou commençant par //, name, init, accept
            if (not ligne
                or ligne.startswith("//")
                or ligne.startswith("name")
                or ligne.startswith("init")
                or ligne.startswith("accept")):
                continue
            lignes_filtrees.append(ligne + '\n')

    #Ouverture en écriture du fichier pour écrre les lignes filtrées
    with open(chemin, 'w', encoding='utf-8') as f:
        f.writelines(lignes_filtrees)

    transitions = []
    etats = {}
    compteur = 0
    
    i = 0
    while i < len(lignes_filtrees):
        ligne1=lignes_filtrees[i].strip().split(',') #Strip pour enlever le retour à la ligne et split pour séparer les éléments
        ligne2= lignes_filtrees[i+1].strip().split(',')
        nb_symboles_lus = ligne1[1:] if len(ligne1) > 1 else ""
        n_rubans = len(nb_symboles_lus) #On déduit le nombre de rubans à partir du nombre de symboles lus (première ligne)
        
        #On définit ce que réprésente chaque partie de chaque ligne
        etat1=ligne1[0]
        lus = ligne1[1:n_rubans+1]
        etat2=ligne2[0]
        ecrits = ligne2[1:n_rubans+1]
        directions = ligne2[1+n_rubans:2*n_rubans+1]

        #On remplace les '_' par des '□' pour les symboles vides
        for l in range(len(lus)):
            if lus[l] == '_':
                lus[l] = '□'
            else:
                lus[l] = lus[l]

        for e in range(len(ecrits)):
            if ecrits[e] == '_':
                ecrits[e] = '□'
            else:
                ecrits[e] = ecrits[e]

        for etat in [etat1, etat2]:
            if etat not in etats:
                etats[etat] = str(compteur) #On associe à chaque état un numéro unique
                compteur += 1
        
        #On ajoute la transition correspondante à la liste des transitions, * pour ajouter les éléments de chaque liste individuellement
        transitions.extend([
            etats[etat1],
            *lus,
            *ecrits,
            *directions,
            etats[etat2]
        ])
        i += 2 #On lit les lignes deux par deux

    codage = "|".join(transitions)

    return codage, n_rubans


#Q8

def table_de_codage(dico):
    liste_elements = []
    table_codage = {}

    #Création d'une liste avec toutes les valeurs du dictionnaire
    for elements in dico.values():
        liste_elements+=elements

    n_elements = len(liste_elements)
    if n_elements == 0:
        table_codage = {}
    nb_bits = (n_elements - 1).bit_length() if n_elements > 0 else 0 #Calcul du nombre de bits nécessaires pour coder tous les éléments de la liste

    for i, element in enumerate(liste_elements):
        code_binaire = format(i, f'0{nb_bits}b') #Formatage de l'index en binaire puis ajout de 0 à gauche pour atteindre le nombre de bits nécessaire
        table_codage[element] = code_binaire

    return table_codage


def codage_binaire(chemin):
    code_str, n_rubans = codage(chemin)
    dico_elements={"etats": [], "symboles": [], "mouvements": [], "separateur": []}
    formatage = ["etats","separateur"]+(2*n_rubans)*["symboles","separateur"]+n_rubans*["mouvements","separateur"]+["etats","separateur"] #Formatage spécifique en fonction du nombre de rubans
    code_liste=list(code_str)
    print(code_str)
    print(n_rubans)
    n_elements = len(code_str)

    #On parcourt le codage et on ajoute chaque élément à sa catégorie dans le dictionnaire en fonction du formatage
    for i in range(6*n_rubans+4):
        for j in range(i, n_elements, 6*n_rubans+4):
            element = code_str[j]
            if element not in dico_elements[formatage[i]]:
                dico_elements[formatage[i]] += element
    dico_elements['etats'] = [f"q{etat}" for etat in dico_elements['etats']] #On ajoute "q" devant le numéro des états pour les différencier des symboles

    table_codage=table_de_codage(dico_elements)
    print(table_codage)
    #On parcourt le codage et on remplace chaque élément par son code binaire correspondant dans la table de codage
    for i in range(6*n_rubans+4):
        for j in range(i, n_elements, 6*n_rubans+4):
            if formatage[i] == "etats" and "q"+code_liste[j] in table_codage:
                code_liste[j]=table_codage["q"+ code_liste[j]]
            elif code_liste[j] in table_codage:
                code_liste[j]=table_codage[code_liste[j]]

    return "".join(code_liste)



#Q9

def decodage_binaire(code, table_codage):
    transitions = []
    n_bits = len(table_codage[list(table_codage.keys())[0]])
    table_decodage = {v: k for k, v in table_codage.items()}
    coupe = [code[i:i+n_bits] for i in range(0, len(code), n_bits)]

    for i in coupe:
        if table_decodage[i][0] == 'q': 
            transitions.append(table_decodage[i][1:])
        else:
            transitions.append(table_decodage[i])
    
    transitions_str="".join(transitions)

    return transitions_str


def lire_transitions(code_str, n_rubans):
    elements = code_str.split("|")
    #print(elements)
    taille = 2 + 3*n_rubans  # etat1 + lus + ecrits + directions + etat2

    transitions = []

    i = 0
    while i < len(elements):
        etat1 = elements[i]
        lus = elements[i+1:i+1+n_rubans]
        ecrits = elements[i+1+n_rubans:i+1+2*n_rubans]
        directions = elements[i+1+2*n_rubans:i+1+3*n_rubans]
        etat2 = elements[i+1+3*n_rubans]

        transitions.append((etat1, *lus, *ecrits, *directions, etat2))
        i += taille

    return transitions

#print(lire_transitions("0|0|1|>|0|0|1|0|>|0|0|□|□|-|1", 1))


def machine_universelle(code_M,x, n_rubans, table_codage, initial, accepte):

    ruban1=code_M+"#"+x
    ruban3=initial

    part1, part2 = ruban1.split("#")
    ruban1=list(part1)
    ruban2=list(part2)+['□'] # On ajoute des cases vides à la fin du ruban pour éviter les problèmes d'index

    decodage=decodage_binaire(code_M, table_codage)
    transitions = lire_transitions(decodage, n_rubans)

    tete=0
    i = 0

    while i < len(transitions):

        if ruban3 == transitions[i][0] and 0 <= tete < len(ruban2) and ruban2[tete] == transitions[i][1]:

            ruban3 = transitions[i][-1]
            ruban2[tete] = transitions[i][1 + n_rubans]

            if transitions[i][1+2*n_rubans] == '>':
                if tete < 0:
                    ruban2.insert(0, '□')
                    tete = 0
                elif tete >= len(ruban2):
                    ruban2.append('□')
                else:
                    tete += 1
            elif transitions[i][1+2*n_rubans] == '<':
                tete -= 1

            i = 0
            continue
        i += 1
    
    if ruban3 == accepte:
        print("La machine accepte l'entrée.")
    else:
        print("La machine rejette l'entrée.")

    return



#Q10

def machine_universelle_limitee(code_M, x, n_etapes, n_rubans,table_codage, initial, accepte):

    ruban1 = code_M + "#" + x + "#" + str(n_etapes)
    ruban3 = initial

    part1, part2, part3 = ruban1.split("#")

    ruban1 = list(part1)  # code de M (inutile ici mais conservé)
    ruban2 = list(part2) # ruban de travail
    ruban_compteur = int(part3)   # compteur d'étapes

    decodage = decodage_binaire(code_M, table_codage)
    transitions = lire_transitions(decodage, n_rubans)

    tete = 0

    while ruban_compteur > 0:
        i = 0

        while i < len(transitions):

            if (ruban3 == transitions[i][0] and
                0 <= tete < len(ruban2) and
                ruban2[tete] == transitions[i][1]):

                print(transitions[i])

                # appliquer transition
                ruban3 = transitions[i][-1]
                ruban2[tete] = transitions[i][1 + n_rubans]

                # déplacement
                if transitions[i][1+2*n_rubans] == '>':
                    if tete < 0:
                        ruban2.insert(0, '□')
                        tete = 0
                    elif tete >= len(ruban2):
                        ruban2.append('□')
                    else:
                        tete += 1
                elif transitions[i][1+2*n_rubans] == '<':
                    tete -= 1

                # décrément du compteur
                ruban_compteur -= 1

                i = 0
                continue

            i += 1

    if ruban3 == accepte:
        print("La machine accepte l'entrée.")
    else:
        print("La machine rejette l'entrée.")
    if ruban_compteur == 0:
        print("Arrêt après", n_etapes, "étapes.")

    return




# nom = input("Entrez le chemin du fichier à coder: ")
# print(codage(nom))
# print(codage_binaire(nom))


# code=input("Entrez le code binaire de la machine : ")
# mot=input("Entrez le mot à tester : ")
# table=input("Entrez la table de codage (sous forme de dictionnaire) : ")
# initial=input("Entrez l'état initial de la machine : ")
# accepte=input("Entrez l'état d'acceptation de la machine : ")

#machine_universelle("0000100000111000001110000110100000011000000110000011100000111000011010000000100000001000010010000100100001101000000010000001100001001000010010000110100000011000000010000101100001011000011110000010", "0111", 1, {'q0': '0000', 'q1': '0001', 'q2': '0010', '0': '0011', '1': '0100', '□': '0101', '>': '0110', '-': '0111', '|': '1000'}, '0','2')
machine_universelle_limitee("0000100000111000001110000110100000011000000110000011100000111000011010000000100000001000010010000100100001101000000010000001100001001000010010000110100000011000000010000101100001011000011110000010", "0110", 3, 1, {'q0': '0000', 'q1': '0001', 'q2': '0010', '0': '0011', '1': '0100', '□': '0101', '>': '0110', '-': '0111', '|': '1000'}, '0','2')
