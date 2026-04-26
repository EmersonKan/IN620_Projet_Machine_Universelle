import os

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
                code_liste[j]=table_codage["q"+ code_liste[j]]+" "
            elif code_liste[j] in table_codage:
                code_liste[j]=table_codage[code_liste[j]]+" "

    return "".join(code_liste)

nom = input("Entrez le chemin du fichier à coder: ")
print(codage_binaire(nom))