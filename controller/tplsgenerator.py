import pandas as pd
import numpy as np
from ta.volatility import AverageTrueRange

def calculate_tp_sl(data, atr_multiplier_tp=1.2, atr_multiplier_sl=1, risk_tolerance=1):
    """
    Calcule le Take Profit (TP) et le Stop Loss (SL) en utilisant l'ATR et la tolérance au risque.

    :param data: DataFrame contenant les colonnes 'high', 'low', et 'close'.
    :param atr_multiplier_tp: Multiplicateur ATR pour le calcul du TP.
    :param atr_multiplier_sl: Multiplicateur ATR pour le calcul du SL.
    :param risk_tolerance: Facteur ajustant l'agressivité du TP et du SL.
    :return: Un tuple contenant les valeurs de TP et SL.
    """
    
    # Calcul de l'Average True Range (ATR)
    atr = AverageTrueRange(high=data['high'], low=data['low'], close=data['close'], window=14)
    current_atr = atr.average_true_range().iloc[-1]

    # Calcul du dernier prix de clôture
    last_close = data['close'].iloc[-1]

    # Calcul de TP et SL selon la volatilité et la tolérance au risque
    tp = last_close + (current_atr * atr_multiplier_tp * risk_tolerance)
    sl = last_close - (current_atr * atr_multiplier_sl * risk_tolerance)

    print("Take Profit:", tp, "Stop Loss:", sl)
    return tp, sl
