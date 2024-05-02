import pandas as pd
import talib

def trading_signals_D1(data):
    # Calcul des SMA
    data['SMA_50'] = talib.SMA(data['close'], timeperiod=50)
    data['SMA_200'] = talib.SMA(data['close'], timeperiod=200)

    # Calcul du Parabolic SAR
    data['SAR'] = talib.SAR(data['high'], data['low'], acceleration=0.02, maximum=0.2)

    # Calcul du CCI
    data['CCI'] = talib.CCI(data['high'], data['low'], data['close'], timeperiod=20)

    # Initialisation de la colonne des signaux
    data['Signal'] = 'Neutral'  # Défaut à neutre

    # Golden Cross / Death Cross Logic
    data.loc[(data['SMA_50'] > data['SMA_200']) & (data['SMA_50'].shift(1) < data['SMA_200'].shift(1)), 'Signal'] = 'Buy'
    data.loc[(data['SMA_50'] < data['SMA_200']) & (data['SMA_50'].shift(1) > data['SMA_200'].shift(1)), 'Signal'] = 'Sell'

    # Parabolic SAR Logic
    data.loc[(data['close'] > data['SAR']), 'Signal'] = 'Buy'
    data.loc[(data['close'] < data['SAR']), 'Signal'] = 'Sell'

    # CCI Logic
    data.loc[data['CCI'] > 100, 'Signal'] = 'Sell'
    data.loc[data['CCI'] < -100, 'Signal'] = 'Buy'

    # Check for Neutral Signal - This can be adjusted according to more specific rules
    # This example checks if all conditions are neutral or conflicting
    for index, row in data.iterrows():
        if (row['SMA_50'] < row['SMA_200'] and row['close'] > row['SAR']) or (row['SMA_50'] > row['SMA_200'] and row['close'] < row['SAR']):
            data.at[index, 'Signal'] = 'Neutral'

    return data
