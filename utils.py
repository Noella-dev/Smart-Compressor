import os
import hashlib

def generer_donnees_test(nom_fichier, taille_mo=105):
    """Genere un fichier avec des motifs repetitifs pour valider l'algorithme."""
    motif = "DATA_LOG_2026;MASTER_2_ALGO;MSG=TEST_COMPRESSION;STATUS=OK\n"
    taille_cible = taille_mo * 1024 * 1024
    
    print(f"Creation du fichier de test ({taille_mo} Mo)...")
    with open(nom_fichier, "w", encoding="utf-8") as f:
        taille_actuelle = 0
        while taille_actuelle < taille_cible:
            f.write(motif)
            taille_actuelle += len(motif)
    
    print(f"Fichier '{nom_fichier}' genere avec succes.")
    return nom_fichier

def verifier_taille(chemin):
    """Verifie le respect de la consigne : Taille > 100 Mo."""
    if not os.path.exists(chemin):
        print(f"Erreur : Le fichier {chemin} n'existe pas.")
        return False
        
    LIMITE_MINIMALE = 100 * 1024 * 1024 # 100 Mo
    taille_reelle = os.path.getsize(chemin)
    
    if taille_reelle > LIMITE_MINIMALE:
        print(f"Taille vérifiée : {taille_reelle / (1024*1024):.2f} Mo. (Conforme au sujet)")
        return True
    else:
        print(f"ERREUR : Le fichier fait seulement {taille_reelle / (1024*1024):.2f} Mo.")
        print("Le sujet impose des tests sur des fichiers de taille > 100 Mo.")
        return False

def calculer_hash_sha256(chemin):
    """Genere l'empreinte numerique unique du fichier pour prouver le Lossless."""
    empreinte = hashlib.sha256()
    with open(chemin, "rb") as f:
        # Lecture par blocs de 4Ko pour l'efficacite memoire
        for bloc in iter(lambda: f.read(4096), b""):
            empreinte.update(bloc)
    return empreinte.hexdigest()