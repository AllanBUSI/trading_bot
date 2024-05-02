import pandas as pd
import numpy as np

def trading_signals_4H(data):
    # Calcul des Bandes de Bollinger
    data['MA_20'] = data['close'].rolling(window=20).mean()
    data['STD_20'] = data['close'].rolling(window=20).std()
    data['Upper_Band'] = data['MA_20'] + (data['STD_20'] * 2)
    data['Lower_Band'] = data['MA_20'] - (data['STD_20'] * 2)

    # Calcul du Stochastic Oscillator
    data['Lowest_Low'] = data['low'].rolling(window=14).min()
    data['Highest_High'] = data['high'].rolling(window=14).max()
    data['%K'] = 100 * ((data['close'] - data['Lowest_Low']) / (data['Highest_High'] - data['Lowest_Low']))

    # Calcul de l'ADX
    plus_dm = data['high'].diff()
    minus_dm = data['low'].diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    minus_dm = abs(minus_dm)

    tr1 = data['high'] - data['low']
    tr2 = abs(data['high'] - data['close'].shift())
    tr3 = abs(data['low'] - data['close'].shift())
    tr = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
    atr = tr.rolling(window=14).mean()

    plus_di = 100 * (plus_dm.rolling(window=14).sum() / atr)
    minus_di = 100 * (minus_dm.rolling(window=14).sum() / atr)
    data['ADX'] = 100 * abs((plus_di - minus_di) / (plus_di + minus_di)).rolling(window=14).mean()

    # Définition des signaux de trading
    data['Signal'] = 'neutre'  # Initialisation de tous les signaux à Neutre
    data.loc[(data['ADX'] > 25) & (plus_di > minus_di), 'Signal'] = 'achat'
    data.loc[(data['ADX'] > 25) & (plus_di < minus_di), 'Signal'] = 'vente'
    data.loc[(data['%K'] > 80) & (data['close'] > data['Upper_Band']), 'Signal'] = 'vente'
    data.loc[(data['%K'] < 20) & (data['close'] < data['Lower_Band']), 'Signal'] = 'achat'
    
    # Ajout de conditions pour signaux neutres
    # Si les indicateurs sont contradictoires ou aucune condition n'est remplie, le signal reste neutre.
    # Exemple de condition neutre: quand les indicateurs sont entre les seuils ou suggèrent une direction opposée.
    
    data.loc[(data['%K'] > 20) & (data['%K'] < 80), 'Signal'] = 'neutre'
    data.loc[(data['ADX'] < 20), 'Signal'] = 'neutre'

    return data[['close', 'Upper_Band', 'Lower_Band', '%K', 'ADX', 'Signal']]

