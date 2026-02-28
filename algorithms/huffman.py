import heapq
from collections import Counter

class NoeudHuffman:
    def __init__(self, symbole, frequence):
        self.symbole = symbole # L'octet original
        self.frequence = frequence
        self.gauche = None
        self.droite = None

    def __lt__(self, autre):
        return self.frequence < autre.frequence

def generer_dictionnaire_codes(racine, code_actuel="", codes=None):
    if codes is None:
        codes = {}
    if racine is None:
        return
    if racine.symbole is not None:
        codes[racine.symbole] = code_actuel
        
    generer_dictionnaire_codes(racine.gauche, code_actuel + "0", codes)
    generer_dictionnaire_codes(racine.droite, code_actuel + "1", codes)
    return codes

def compresser(donnees):
    #Calcul des fréquences des symboles
    frequences_symboles = Counter(donnees)
    
    #Construction de l'Arbre de Huffman
    file_priorite_noeuds = [NoeudHuffman(s, f) for s, f in frequences_symboles.items()]
    heapq.heapify(file_priorite_noeuds)

    while len(file_priorite_noeuds) > 1:
        n1 = heapq.heappop(file_priorite_noeuds)
        n2 = heapq.heappop(file_priorite_noeuds)
        # creation d'un noeud parent (fusion)
        fusion = NoeudHuffman(None, n1.frequence + n2.frequence)
        fusion.gauche = n1
        fusion.droite = n2
        heapq.heappush(file_priorite_noeuds, fusion)

    arbre_huffman_racine = file_priorite_noeuds[0]
    dictionnaire_codes = generer_dictionnaire_codes(arbre_huffman_racine)
    
    #Encodage en flux de bits
    flux_bits = "".join(dictionnaire_codes[octet] for octet in donnees)
    return flux_bits, arbre_huffman_racine

def decompresser(flux_bits, arbre_huffman_racine):
    resultat = bytearray()
    noeud_actuel = arbre_huffman_racine
    
    for bit in flux_bits:
        noeud_actuel = noeud_actuel.gauche if bit == '0' else noeud_actuel.droite
            
        if noeud_actuel.symbole is not None:
            resultat.append(noeud_actuel.symbole)
            noeud_actuel = arbre_huffman_racine
            
    return resultat