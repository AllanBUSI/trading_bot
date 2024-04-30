import numpy as np
import pandas as pd

def estimate_returns(price_series):
    """
    Estime le rendement moyen quotidien et le rendement annuelisé d'un actif.

    :param price_series: pandas.Series contenant les prix historiques de l'actif.
    :return: Un tuple contenant le rendement moyen quotidien et le rendement annuelisé.
    """
    
    price_series = price_series[price_series > 0]

    # Calculer les rendements logarithmiques
    log_returns = np.log(price_series / price_series.shift(1))
    
    mean_daily_return = log_returns.mean(skipna=True)

    # Calculer le rendement annuelisé
    annualized_return = mean_daily_return * 365  # Multiplier par le nombre de jours de trading dans une année

    return mean_daily_return, annualized_return

