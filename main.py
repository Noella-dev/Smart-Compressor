import os
import time
from utils import generer_donnees_test, verifier_taille, calculer_hash_sha256
import codec

def afficher_interface():
    print("""
    ===========================================
    #       SMART-COMPRESSOR                  #
    #    Architecture : LZ77 + Huffman        #
    ===========================================
    """)

def lancer_programme():
    afficher_interface()
    
    #selection de la source de donnees
    print("--- SOURCE DES DONNEES ---")
    print("1) Générer un fichier étalon (105 Mo)")
    print("2) Sélectionner un fichier existant (CSV, TXT, XML...)qui place à la racine du projet, au même niveau que le fichier main.py.")
    choix = input("\nVotre choix (1 ou 2) : ")

    if choix == "1":
        nom_fichier = "test_donnees.txt"
        generer_donnees_test(nom_fichier, 105)
    else:
        nom_fichier = input("Entrez le nom exact du fichier (ex: MedQuAD.csv)au même niveau que le fichier main.py: ")

    # Validation des contraintes de l'examen (> 100 Mo)
    if not os.path.exists(nom_fichier):
        print(f"Erreur : Le fichier '{nom_fichier}' est introuvable.")
        return

    if not verifier_taille(nom_fichier):
        return 
 
    #Phase de Compression
    print(f"\n---  LANCEMENT DE LA COMPRESSION ---")
    empreinte_originale = calculer_hash_sha256(nom_fichier)
    print(f"Hash Original (SHA-256) : {empreinte_originale}")
    
    debut_chrono = time.time()
    fichier_compresse = nom_fichier + ".bin"
    
    try:
        codec.compresser_fichier(nom_fichier, fichier_compresse)
        fin_chrono = time.time()
        
        # Calcul des Statistiques
        temps_total = fin_chrono - debut_chrono
        taille_initiale = os.path.getsize(nom_fichier) / (1024 * 1024)
        taille_finale = os.path.getsize(fichier_compresse) / (1024 * 1024)
        gain_pourcentage = (1 - (taille_finale / taille_initiale)) * 100

        print("\n--- RAPPORT DE PERFORMANCE ---")
        print(f"Temps d'exécution  : {temps_total:.2f} secondes")
        print(f"Taille Initiale    : {taille_initiale:.2f} Mo")
        print(f"Taille Compressée  : {taille_finale:.2f} Mo")
        print(f"Gain d'espace      : {gain_pourcentage:.2f} %")
        print(f"Fichier généré     : {fichier_compresse}")

        # Phase de Decompression (Validation de l'integrite)
        print("\n--- PHASE DE DÉCOMPRESSION ---")
        nom_restaure = "RESTAURE_" + nom_fichier
        debut_dec = time.time()
        
        codec.decompresser_fichier(fichier_compresse, nom_restaure)
        
        temps_dec = time.time() - debut_dec
        print(f"Temps de décompression : {temps_dec:.2f} secondes")

        #Verification Finale SHA-256 (Preuve du Lossless)
        print("\n---  VÉRIFICATION D'INTEGRITE ---")
        empreinte_restauree = calculer_hash_sha256(nom_restaure)
        
        print(f"Hash Original : {empreinte_originale}")
        print(f"Hash Restauré : {empreinte_restauree}")

        if empreinte_originale == empreinte_restauree:
            print("\n SUCCÈS : Restauration bit à bit parfaite (Algorithme Lossless) !")
        else:
            print("\n ECHEC : Le fichier restauré présente des différences.")

    except Exception as e:
        print(f"\n Une erreur est survenue durant le traitement : {e}")

if __name__ == "__main__":
    try:
        lancer_programme()
    except KeyboardInterrupt:
        print("\n\n Programme interrompu par l'utilisateur.")