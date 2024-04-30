from collections import Counter

def count_duplicates(array):
    # Utiliser Counter pour compter les occurrences de chaque élément
    counts = Counter(array)
    
    # Créer un dictionnaire pour stocker seulement les éléments qui apparaissent plus d'une fois
    duplicates = {key: value for key, value in counts.items() if value > 1}
    
    # Vérifier si le dictionnaire des doublons est non vide et retourner le résultat
    if duplicates:
        return True, duplicates
    else:
        return False, {}