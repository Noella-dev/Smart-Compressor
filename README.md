# Smart-Compressor
Système de compression et décompression de données **Lossless** (sans perte) optimisé pour les fichiers de grande taille (> 100 Mo). Ce projet a été réalisé dans le cadre de l'examen d'Algorithmique Avancée.

##  Présentation
Ce programme combine deux algorithmes fondamentaux pour maximiser le taux de compression tout en garantissant une intégrité totale des données :
1. **LZ77** : Réduction des redondances par dictionnaire (fenêtre glissante).
2. **Huffman** : Codage statistique pour optimiser l'espace au niveau des bits.

L'innovation majeure de cette implémentation réside dans l'utilisation d'une **Table de Hachage** pour accélérer la recherche des motifs LZ77, rendant le traitement de fichiers de 100 Mo fluide et rapide.

## Fonctionnalités
- **Compression Hybride** : Application successive de LZ77 et Huffman.
- **Sécurité de Taille** : Vérification automatique que le fichier source respecte la consigne des 100 Mo.
- **Validation SHA-256** : Comparaison des empreintes numériques (Hash) avant et après traitement pour prouver l'absence de perte de données.
- **Interface Interactive** : Menu simple pour générer des données de test ou utiliser ses propres fichiers.

## Installation et Utilisation

### Prérequis
- Python 3.x installé.
- Aucune bibliothèque externe n'est requise (utilisation de la bibliothèque standard).

### Lancement
1.Lancez le programme principal : 
   ```bash
  python main.py
```
## Résultats Expérimentaux
Le système a été validé sur différents types de jeux de données massifs (> 100 Mo) :

1. **Données de Test (Générées)** : 105 Mo -> 1.25 Mo (**98.81%** de gain).
2. **enwik8 (Benchmark)** : Ce fichier plus de 100Mo, standard de l'industrie pour les benchmarks de compression, a été utilisé pour valider la performance du système sur des données textuelles non répétitives (XML/Naturel). L'absence d'extension du fichier n'altère pas le processus, car notre algorithme traite le flux de données au niveau binaire (octets).

**Dans tous les cas, la vérification SHA-256 a confirmé une restauration bit à bit sans aucune perte.**
Lors de nos tests sur une machine Linux, nous avons obtenu les résultats suivants :

    Fichier Source : test_data.txt

    Taille Originale : 105.00 Mo

    Taille Compressée : 1.25 Mo

    Gain d'espace : 98.81 %

    Vérification d'intégrité : RÉUSSIE (SHA-256 identique)

3. **MedQuAD.csv (Données Réelles)** : ~22 Mo alors on a 
```bash
ERREUR : Le fichier fait 21.78 Mo.
Le programme accepte uniquement des fichiers > 100 Mo. 
```
 
## Architecture du Projet

- main.py : Point d'entrée du programme et gestion de l'interface.

- codec.py : Orchestrateur des processus de compression et décompression.

- utils.py : Utilitaires (Génération de données, Hash SHA-256, vérifications).

- algorithms/ :

    - lz77.py : Implémentation optimisée de LZ77.

    - huffman.py : Implémentation du codage de Huffman.