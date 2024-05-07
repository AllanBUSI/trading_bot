import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import model_from_json
from sklearn.preprocessing import MinMaxScaler
from data_sp500 import download
from tensorflow.keras.optimizers import Adam

# Charger l'architecture du modèle à partir du fichier JSON
with open("trainer_architecture.json", "r") as json_file:
    model_architecture_json = json_file.read()
model = model_from_json(model_architecture_json)

# Charger les poids du modèle à partir du fichier HDF5
model.load_weights("trainer_weights.weights.h5")

# Compiler le modèle
optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='mean_squared_error')

# Charger l'échelleur
scaler = joblib.load("scaler.save")

# Télécharger les nouvelles données
download(['MSFT'], '2024-02-06', '2024-04-06')

# Charger les données à partir du fichier CSV
data = pd.read_csv('sp500_data.csv')
data['Date'] = pd.to_datetime(data['Date'])
data = data.sort_values('Date')

# Préparation des données
selected_columns = ['Date', 'Close']
data = data[selected_columns]
last_observations = data.tail(30)['Close'].values.reshape(-1, 1)

# Normaliser les données
scaled_data = scaler.transform(last_observations)


def online_learning_and_prediction(model, scaler, scaled_data, window_size, num_days):
    future_predictions = []
    input_data = np.array(scaled_data[-window_size:]).reshape(1, window_size, 1)

    # Configuration de l'optimiseur avec gradient clipping
    optimizer = Adam(learning_rate=0.001, clipvalue=1.0)  # Clipvalue peut être ajusté selon le besoin
    model.compile(optimizer=optimizer, loss='mean_squared_error')

    for _ in range(num_days):
        prediction = model.predict(input_data)
        prediction_unscaled = scaler.inverse_transform(prediction)[0][0]
        future_predictions.append(prediction_unscaled)

        # Mise à jour des données d'entrée pour la prédiction suivante
        input_data = np.append(input_data[:, 1:, :], prediction.reshape(1, 1, 1), axis=1)

        # Convertir la prédiction à la bonne forme et échelle pour l'apprentissage
        prediction_scaled = scaler.transform([[prediction_unscaled]])

        # Apprentissage en ligne: ajuster le modèle avec les nouvelles données
        model.fit(input_data, prediction_scaled, epochs=1, batch_size=1, verbose=0)

    return future_predictions

# Définir la taille de la fenêtre et prédire les prix futurs tout en apprenant
window_size = 30
future_price_predictions = online_learning_and_prediction(model, scaler, scaled_data, window_size, 30)
print("Prix prédits pour les 30 prochains jours :", future_price_predictions)
