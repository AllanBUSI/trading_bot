import json

import pandas as pd

# Fonction pour lire un fichier JSON
def read_json(nom_de_fichier):
    try:
        # Ouvrir le fichier en mode lecture
        with open(nom_de_fichier, 'r', encoding='utf-8') as fichier:
            # Charger le contenu du fichier JSON dans un dictionnaire
            donnees = json.load(fichier)
        return donnees
    except FileNotFoundError:
        print("Le fichier spécifié n'a pas été trouvé.")
    except json.JSONDecodeError:
        print("Le fichier n'est pas un JSON valide.")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")


def json_to_pd(json):
    return pd.DataFrame(json)
