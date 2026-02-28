import struct
import pickle
import os
from algorithms import lz77, huffman

def compresser_fichier(chemin_entree, chemin_sortie):
    """Orchestre la compression LZ77 suivie de Huffman."""
    with open(chemin_entree, 'rb') as f:
        donnees_brutes = f.read()

    print("Step 1: Application de l'algorithme LZ77...")
    liste_triplets = lz77.compresser(donnees_brutes)
    
    print("Step 2: Preparation binaire des triplets...")
    donnees_compactes = bytearray()
    for distance, longueur, symbole in liste_triplets:
        # H=unsigned short (2 octets), B=unsigned char (1 octet)
        donnees_compactes.extend(struct.pack('>HBB', distance, longueur, symbole))
    
    print("Step 3: Encodage de Huffman...")
    flux_bits, arbre_huffman = huffman.compresser(donnees_compactes)
    
    with open(chemin_sortie, 'wb') as f_out:
        #on sauvegarde l'arbre pour la decompression
        pickle.dump(arbre_huffman, f_out)
        #on sauvegarde la longueur exacte pour gerer le padding binaire
        pickle.dump(len(flux_bits), f_out)
        # Conversion du flux de bits '0101' en octets réels
        entier_bits = int(flux_bits, 2)
        nb_octets = (len(flux_bits) + 7) // 8
        f_out.write(entier_bits.to_bytes(nb_octets, 'big'))

def decompresser_fichier(chemin_compresse, chemin_final):
    """Orchestre la décompression Huffman suivie de la reconstruction LZ77."""
    print(f"Decompression de {os.path.basename(chemin_compresse)}...")
    
    with open(chemin_compresse, 'rb') as f_in:
        arbre_huffman_racine = pickle.load(f_in)
        longueur_bits_attendue = pickle.load(f_in)
        donnees_binaires = f_in.read()
    
    print("Step 1: Decodage Huffman...")
    entier_huff = int.from_bytes(donnees_binaires, byteorder='big')
    #conversion en chaine de '0' et '1' avec remise du zero initial si besoin
    flux_bits = bin(entier_huff)[2:].zfill(longueur_bits_attendue)
    
    # Correction du decalage potentiel dû à la conversion int
    if len(flux_bits) > longueur_bits_attendue:
        flux_bits = flux_bits[-longueur_bits_attendue:]

    donnees_compactes = huffman.decompresser(flux_bits, arbre_huffman_racine)
    
    print("Step 2: Extraction des triplets (Distance, Longueur, Symbole)...")
    liste_triplets = []
    taille_format = struct.calcsize('>HBB')
    for k in range(0, len(donnees_compactes), taille_format):
        bloc = donnees_compactes[k : k + taille_format]
        if len(bloc) == taille_format:
            liste_triplets.append(struct.unpack('>HBB', bloc))
    
    print("Step 3: Reconstruction LZ77 finale...")
    donnees_finales = lz77.decompresser(liste_triplets)
    
    with open(chemin_final, 'wb') as f_out:
        f_out.write(donnees_finales)