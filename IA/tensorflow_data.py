import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_absolute_error
import joblib
from data_sp500 import download


# Définir les symboles S&P 500
sp500_symbols = [ 'A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACN', 'ACE', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADS', 'ADSK', 'ADT', 'AEE',
'AEP', 'AES', 'AET', 'AFL', 'AGN', 'AIG', 'AIV', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALK', 'ALL', 'ALLE', 'ALXN', 'AMAT', 'AMD', 'AME',
'AMGN', 'AMP', 'AMT', 'AMZN', 'AN', 'ANSS', 'ANTM', 'AON', 'APA', 'APC', 'APD', 'APH', 'APO', 'APTV', 'ARE', 'ARG', 'ATI', 'ATO',
'ATR', 'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO', 'BA', 'BAC', 'BAX', 'BBT', 'BBY', 'BDX', 'BEAV', 'BEN', 'BF-B', 'BHI',
'BIIB', 'BIO', 'BK', 'BKNG', 'BLK', 'BLL', 'BMY', 'BMRN', 'BR', 'BRK-B', 'BRO', 'BSX', 'BTU', 'BUD', 'BXP', 'C', 'CAG', 'CAH', 'CAT',
'CB', 'CBOE', 'CBRE', 'CBS', 'CCE', 'CCI', 'CCL', 'CDNS', 'CDW', 'CE', 'CELG', 'CERN', 'CF', 'CFR', 'CHD', 'CHRW', 'CI', 'CINF',
'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNP', 'CNX', 'COF', 'COG', 'COH', 'COL', 'COP', 'COST', 'COTY', 'CPB',
'CPRT', 'CRM', 'CSC', 'CSCO', 'CSX', 'CTAS', 'CTSH', 'CTXS', 'CTVA', 'CVX', 'CW', 'CZR', 'D', 'DAL', 'DD', 'DDS', 'DE', 'DELL',
'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISCA', 'DISCK', 'DISH', 'DK', 'DLR', 'DLTR', 'DNB', 'DO', 'DOV', 'DOW', 'DPS', 'DRI',
'DTE', 'DUK', 'DVA', 'DVN', 'DXCM', 'DXR', 'EA', 'EAT', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR', 'ENDP', 'EOG',
'EQIX', 'EQR', 'ES', 'ESS', 'ETFC', 'ETN', 'ETR', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FAST', 'FB', 'FCX', 'FDC',
'FDX', 'FE', 'FIS', 'FISV', 'FITB', 'FLIR', 'FLS', 'FLT', 'FMC', 'FOSL', 'FOX', 'FOXA', 'FRX', 'FSLR', 'FTV', 'FTI', 'FTR', 'GAS',
'GD', 'GE', 'GILD', 'GIS', 'GLW', 'GM', 'GME', 'GNRC', 'GNW', 'GOOGL', 'GOOG', 'GPC', 'GPS', 'GRMN', 'GS', 'GWW', 'HAL', 'HAR',
'HAS', 'HBAN', 'HBI', 'HCA', 'HD', 'HES', 'HIG', 'HII', 'HON', 'HRL', 'HRS', 'HST', 'HSY', 'HUM', 'IBM', 'ICE', 'IDXX', 'IEX',
'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 'IP', 'IPG', 'IQV', 'IR', 'IRM', 'ITW', 'IVZ', 'JBHT', 'JCI', 'JEC', 'JNJ', 'JPM', 'K',
'KEY', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KO', 'KR', 'KSS', 'L', 'LABL', 'LB', 'LBTYA', 'LBTYB', 'LBTYK', 'LC', 'LEG', 'LEN',
'LH', 'LHX', 'LIN', 'LKQ', 'LLL', 'LLY', 'LM', 'LMT', 'LNC', 'LNT', 'LO', 'LOW', 'LRCX', 'LUV', 'LYB', 'LYV', 'M', 'MA', 'MAA',
'MAC', 'MAR', 'MAS', 'MAT', 'MCD', 'MCK', 'MDLZ', 'MDT', 'MET', 'MGM', 'MHK', 'MKC', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MON',
'MOS', 'MPC', 'MRK', 'MRO', 'MS', 'MSFT', 'MSI', 'MTB', 'MTD', 'MU', 'MYL', 'NDAQ', 'NEE', 'NEM', 'NFLX', 'NFX', 'NI', 'NKE',
'NL', 'NOC', 'NOV', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUAN', 'NUE', 'NVDA', 'NWL', 'NWSA', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OXY',
'PAYX', 'PBCT', 'PCAR', 'PCG', 'PCL', 'PCLN', 'PCP', 'PDCO', 'PEP', 'PETM', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD',
'PM', 'PNC', 'PNR', 'PNW', 'POM', 'PPG', 'PPL', 'PX', 'PXD', 'QCOM', 'QRVO', 'R', 'RAI', 'RCL', 'REG', 'REGN', 'RF', 'RHI', 'RHT',
'RIG', 'RJF', 'RL', 'ROK', 'ROL', 'ROP', 'ROST', 'RRC', 'RSG', 'RTN', 'SBAC', 'SBNY', 'SBUX', 'SCG', 'SCHW', 'SE', 'SEE', 'SHW',
'SIG', 'SJM', 'SLB', 'SLG', 'SLM', 'SNP', 'SNPS', 'SNV', 'SO', 'SPG', 'SPLS', 'SRE', 'STI', 'STJ', 'STT', 'STX', 'STZ', 'SWK',
'SWKS', 'SYF', 'SYK', 'SYMC', 'SYY', 'T', 'TAP', 'TDG', 'TDC', 'TEF', 'TEL', 'TER', 'TFC', 'TGT', 'TGNA', 'THC', 'THO', 'THS',
'TIF', 'TJX', 'TMO', 'TNAV', 'TOL', 'TPR', 'TROW', 'TRV', 'TSCO', 'TSN', 'TSS', 'TWX', 'TXN', 'TXT', 'TYC', 'TWC', 'TWTR', 'TWO',
'UA', 'UHS', 'UNH', 'UNP', 'UNUM', 'UPS', 'URI', 'USB', 'USG', 'UTX', 'VAR', 'VFC', 'VLO', 'VMC', 'VNO', 'VRSN', 'VRTX', 'VTR',
'VZ', 'WAB', 'WAG', 'WAT', 'WBA', 'WDC', 'WEC', 'WELL', 'WFC', 'WFM', 'WHR', 'WIN', 'WMB', 'WM', 'WMT', 'WNC', 'WPG', 'WU', 'WY',
'WYN', 'XEL', 'XLNX', 'XOM', 'XRX', 'XYL', 'YHOO', 'YUM', 'ZION', 'ZMH', 'ZTS']

# Télécharger les données
download(sp500_symbols)

# Charger les données
data = pd.read_csv('sp500_data.csv', index_col='Date', parse_dates=True)

# Définir les colonnes numériques et non numériques
numeric_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
non_numeric_columns = ['Symbol']

# Convertir les colonnes numériques en type numérique, gestion des erreurs
for column in numeric_columns:
    data[column] = pd.to_numeric(data[column], errors='coerce')

# Supprimer les lignes avec des valeurs manquantes dans les colonnes numériques
data = data.dropna(subset=numeric_columns)

# Normalisation des données numériques
scaler = MinMaxScaler()
data_close_normalized = pd.DataFrame(scaler.fit_transform(data[['Close']]), columns=['Close'], index=data.index)

# Concaténation des colonnes numériques normalisées avec les colonnes non numériques
data_normalized = pd.concat([data[non_numeric_columns], data_close_normalized], axis=1)

# Définir window_size à un nombre typique pour l'analyse financière, par exemple 20 jours
window_size = 20
X = []
y = []

# Créer des fenêtres glissantes (feature windows) et le vecteur de sortie y
for i in range(window_size, len(data_normalized)):

    X.append(data_normalized.iloc[i-window_size:i][['Close']].values)  # Utiliser iloc pour l'indexation numérique
    y.append(data_normalized.iloc[i]['Close'])  # Prédire le prix de clôture

X = np.array(X)
y = np.array(y)

# Affichage des données d'entrée (X) et de sortie (y)
print("X (input features):", X.shape)
print("y (output target):", y.shape)

# Diviser les données en ensembles d'entraînement et de test (80% pour l'entraînement et 20% pour le test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Paramètres du modèle
lstm_units = 64
num_layers = 2
dropout_rate = 0.2

# Créer le modèle RNN-LSTM
model = Sequential()
model.add(LSTM(lstm_units, activation='relu', return_sequences=True, input_shape=(window_size, 1)))
model.add(Dropout(dropout_rate))

for i in range(num_layers - 1):
    model.add(LSTM(lstm_units, activation='relu', return_sequences=True))
    model.add(Dropout(dropout_rate))

model.add(LSTM(lstm_units, activation='relu'))
model.add(Dropout(dropout_rate))
model.add(Dense(1))

# Compiler le modèle
model.compile(optimizer='adam', loss='mean_squared_error')

# Entraîner le modèle
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test), verbose=1)

# Enregistrer l'architecture du modèle au format JSON
model_architecture_json = model.to_json()
with open("trainer_architecture.json", "w") as json_file:
    json_file.write(model_architecture_json)

# Enregistrer les poids du modèle au format HDF5
model.save_weights("trainer_weights.weights.h5")

# Enregistrer l'échelleur
joblib.dump(scaler, "scaler.save")
