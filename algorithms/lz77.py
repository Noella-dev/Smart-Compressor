
def compresser(donnees, taille_fenetre=4096):
    i = 0
    liste_triplets = []
    taille_totale = len(donnees)
    table_hachage_indices = {}

    while i < taille_totale:
        meilleure_longueur = 0
        meilleure_distance = 0
        
        #on definit le Buffer d'entree
        #on ne cherche une correspondance que si le buffer possede au moins 3 octets
        if i + 3 < taille_totale:
            cle_triplet = (donnees[i], donnees[i+1], donnees[i+2])
            
            if cle_triplet in table_hachage_indices:
                #le buffer de Recherche contient les indices j deja encodees
                for j in reversed(table_hachage_indices[cle_triplet]):
                    if i - j > taille_fenetre:
                        break
                    
                    longueur = 3
                    while (i + longueur < taille_totale and 
                           donnees[j + longueur] == donnees[i + longueur] and 
                           longueur < 255):
                        longueur += 1
                    
                    if longueur > meilleure_longueur:
                        meilleure_longueur = longueur
                        meilleure_distance = i - j
                        if longueur == 255: break
                
                table_hachage_indices[cle_triplet].append(i)
                if len(table_hachage_indices[cle_triplet]) > 10:
                    table_hachage_indices[cle_triplet].pop(0)
            else:
                table_hachage_indices[cle_triplet] = [i]

        # creation du triplet (Distance, Longueur, Symbole_Suivant)
        pos_symbole_suivant = i + meilleure_longueur
        symbole_suivant = donnees[pos_symbole_suivant] if pos_symbole_suivant < taille_totale else 0
        
        liste_triplets.append((meilleure_distance, meilleure_longueur, symbole_suivant))
        i = pos_symbole_suivant + 1
        
    return liste_triplets

def decompresser(liste_triplets):
    resultat = bytearray()
    for distance, longueur, symbole in liste_triplets:
        if distance > 0:
            debut_copie = len(resultat) - distance
            for k in range(longueur):
                resultat.append(resultat[debut_copie + k])
        if symbole != 0:
            resultat.append(symbole)
    return resultat