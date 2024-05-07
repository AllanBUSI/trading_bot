import json
import os
import joblib
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from data_sp500 import download
from datetime import datetime, timedelta
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import CustomObjectScope
import matplotlib.dates as mdates
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint



def prepare_data(data, window_size):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))
    X, y = [], []
    for i in range(window_size, len(scaled_data)):
        X.append(scaled_data[i-window_size:i, 0])
        y.append(scaled_data[i, 0])
    return np.array(X), np.array(y), scaler

def create_model(window_size):
    model = Sequential([
        Input(shape=(window_size, 1)),  # Remplacer 'window_size' par la taille réelle de la fenêtre
        LSTM(20, return_sequences=True),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error',  metrics=['mean_absolute_error'])
    return model

def online_train_predict(model, X, y, scaler, epochs=100, batch_size=5):
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1, validation_split=0.4,
        callbacks=[early_stopping])
    pred = model.predict(X)
    predictions = scaler.inverse_transform(pred).flatten().tolist()
    return predictions

def save_model_and_scaler(model, scaler, model_path='model_complete.weights.h5', weights_path='model_weights.weights.h5', scaler_path='scaler.pkl'):
    # Sauvegarde du modèle complet
    model.save(model_path)
    # Sauvegarde des poids du modèle
    model.save_weights(weights_path)
    # Sauvegarde de l'objet scaler
    joblib.dump(scaler, scaler_path)
    


def load_model_and_scaler(model_path='model_complete.h5', scaler_path='scaler.pkl'):
    # Tenter de charger le modèle
    if os.path.exists(model_path):
        try:
            with CustomObjectScope({'leaky_relu': tf.nn.leaky_relu}):
                model = load_model(model_path)
        except Exception as e:
            print(f"Erreur lors du chargement du modèle : {e}")
            model = None
    else:
        model = None
    
    # Tenter de charger le scaler
    if os.path.exists(scaler_path):
        try:
            scaler = joblib.load(scaler_path)
        except Exception as e:
            print(f"Erreur lors du chargement du scaler : {e}")
            scaler = None
    else:
        scaler = None
    
    return model, scaler



def adjust_dates(start_date, end_date):
    # Convertir les chaînes de dates en objets datetime
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Initialiser la liste des résultats avec la date de départ
    result_dates = [start]
    
    # Boucler jusqu'à atteindre ou dépasser la date de fin
    while True:
        # Calculer la prochaine date en ajoutant 10 jours
        next_date = result_dates[-1] + timedelta(days=10)
        if next_date > end:
            break
        result_dates.append(next_date)
    
    # Vérifier la différence de jours entre la dernière date ajoutée et la date de fin
    last_added_date = result_dates[-1]
    days_diff = (end - last_added_date).days
    
    # Appliquer les règles d'arrondi spécifiques
    if days_diff > 0:
        if days_diff <= 10:  # Si moins de 10 jours restants, arrondir à 10 jours
            result_dates.append(last_added_date + timedelta(days=10))
    
    # Convertir les dates de retour au format de chaîne pour la sortie
    result_dates = [date.strftime("%Y-%m-%d") for date in result_dates]
    
    return result_dates

def predictions_to_json(predictions, start_date):
    # Convertir la date de début en objet datetime
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    
    # Créer une liste pour stocker les objets de prédiction avec les dates
    result = []
    for i, prediction in enumerate(predictions):
        # Calculer la date pour cette prédiction
        current_date = start_datetime + timedelta(days=i)
        # Ajouter un dictionnaire avec la date et la prédiction à la liste de résultats
        result.append({"date": current_date.strftime("%Y-%m-%d"), "prediction": float(prediction)})
    
    # Convertir la liste en JSON
    return json.dumps(result, indent=4)

def remove_non_trading_days(json_data):
    # Charger les données JSON, peut être une chaîne ou directement des données
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    # Préparer la liste pour les données filtrées
    filtered_data = []

    # Itérer sur les éléments du JSON
    for item in data:
        # Convertir la chaîne de date en objet datetime
        date = pd.to_datetime(item['date'])

        # Vérifier si le jour est un jour de trading (lundi à vendredi et pas un jour férié)
        if date.weekday() < 5 and not is_holiday(date):
            filtered_data.append(item)

    # Retourner les données filtrées
    return json.dumps(filtered_data, indent=4)

def is_holiday(date):
    # Cette fonction doit vérifier si la date est un jour férié
    # Ici, nous utilisons un ensemble fictif de jours fériés pour l'exemple
    holidays = pd.to_datetime([
        "2024-01-01",  # Nouvel An
        "2024-07-04",  # Jour de l'Indépendance
        "2024-12-25",  # Noël
    ])
    return date in holidays

# Exemple d'utilisation de la fonction
start_date = "2024-01-01"
end_date = "2024-05-05"
adjusted_dates = adjust_dates(start_date, end_date)

model, scaler = load_model_and_scaler('model_complete.weights.h5', 'scaler.pkl')

if model is None or scaler is None:
    print(model, scaler, "Le modèle ou le scaler n'a pas pu être chargé, initialisation à None.")
    # Vous pouvez ici initialiser un nouveau modèle et scaler si nécessaire
else:
    print("Modèle et scaler chargés avec succès.")

model = None  # Initialiser le modèle en dehors de la boucle
scaler = None  # Initialiser le scaler en dehors de la boucle

i = 0
for date in adjusted_dates:
    if date == start_date:
        continue
    
    # Téléchargement des données pour la période spécifiée
    download(['AAPL'], start=start_date, end=date)
    data = pd.read_csv('sp500_data.csv')
    data = data.reset_index()

    if model is None or scaler is None:  # Créer le modèle et le scaler une seule fois
        X, y, scaler = prepare_data(data, window_size=1)
        model = create_model(window_size=1)
    else:
        X, y, _ = prepare_data(data, window_size=1)
    
    # Formation continue du modèle
    predictions = online_train_predict(model, X, y, scaler)
    json_output = predictions_to_json(predictions, start_date)
    
    json_output = json.loads(json_output)
    
    
    if not json_output:
        continue
    else:
    
        json_output = remove_non_trading_days(json_output)
        json_output = json.loads(json_output)
        
        # Extraire les dates et les prédictions
        dates = [datetime.strptime(item['date'], "%Y-%m-%d") for item in json_output]
        predictions = [item['prediction'] for item in json_output]
        

        
        # Sélectionner les colonnes nécessaires
        data = data[['Date', 'Close']]
        # Renommer les colonnes
        data.rename(columns={'Date': 'date', 'Close': 'prediction'}, inplace=True)
        # Convertir le DataFrame en une liste de dictionnaires
        data = data.to_dict(orient='records')
        
        dates2 = [datetime.strptime(item['date'], "%Y-%m-%d") for item in data]

        predictions2 = [item['prediction'] for item in data]
        
        print(dates2, predictions2)
        
        change_date = datetime.strptime(start_date, "%Y-%m-%d")
        
        change_index = next(i for i, date in enumerate(dates) if date >= change_date)
        
        if i % 10 == 0:
            # Créer le graphique
            plt.figure(figsize=(10, 5))
            plt.plot(dates, predictions, 'r', label='Après 2024-03-23', marker='o', linestyle='-')
            plt.plot(dates2, predictions2, 'b', label='Après 2024-03-23', marker='o', linestyle='-')
            plt.title('Prédictions des Prix')
            plt.xlabel('Date')
            plt.ylabel('Prix Prédit')
            plt.grid(True)

            # Formater les dates sur l'axe des x pour une meilleure lisibilité
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
            plt.gcf().autofmt_xdate()  # Rotation des dates pour mieux les afficher

            plt.show()
        i+1


save_model_and_scaler(model, scaler)
