import pandas as pd
def calculate_volatility(price_series):
    """
    Calcule la volatilité annuelle d'une série de prix d'actifs.

    :param price_series: pandas.Series contenant les prix de l'actif
    :return: float, la volatilité annuelle de l'actif
    """
    # Calculer les rendements quotidiens
    returns = price_series.pct_change()

    # Calculer l'écart-type des rendements (volatilité)
    daily_volatility = returns.std()

    # Convertir la volatilité quotidienne en annuelle
    annual_volatility = daily_volatility * (252 ** 0.5)  # 252 jours de trading dans une année

    return annual_volatility/1000

