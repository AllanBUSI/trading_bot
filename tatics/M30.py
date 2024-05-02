import pandas as pd
import numpy as np

def trading_signals_30M(data):
    # Calcul des EMA
    data['EMA_9'] = data['close'].ewm(span=9, adjust=False).mean()
    data['EMA_21'] = data['close'].ewm(span=21, adjust=False).mean()

    # Calcul du RSI
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Calcul du MACD
    exp1 = data['close'].ewm(span=12, adjust=False).mean()
    exp2 = data['close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

    # Initialisation de la colonne des signaux avec le type object
    data['Signal'] = pd.Series(dtype='object')

    # Définir les signaux basés sur les EMA, RSI, et MACD
    for i in range(len(data)):
        conditions = {
            'ema': data.loc[i, 'EMA_9'] > data.loc[i, 'EMA_21'],
            'rsi_buy': data.loc[i, 'RSI'] < 20,
            'rsi_sell': data.loc[i, 'RSI'] > 80,
            'macd': data.loc[i, 'MACD'] > data.loc[i, 'Signal_Line']
        }
        
        if conditions['ema'] and conditions['macd'] and not conditions['rsi_sell']:
            data.loc[i, 'Signal'] = 'achat'
        elif not conditions['ema'] and not conditions['macd'] and not conditions['rsi_buy']:
            data.loc[i, 'Signal'] = 'vente'
        elif conditions['rsi_sell'] or (conditions['rsi_buy'] and conditions['ema'] and conditions['macd']):
            data.loc[i, 'Signal'] = 'vente' if conditions['rsi_sell'] else 'achat'
        else:
            data.loc[i, 'Signal'] = 'neutre'  # Neutral signal for conflicting or unclear situations

    return data[['close', 'EMA_9', 'EMA_21', 'RSI', 'MACD', 'Signal_Line', 'Signal']]
