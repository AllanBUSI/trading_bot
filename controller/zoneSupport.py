import pandas as pd


def trading_decision(price_data, window_size=20, tolerance=0.05):
    """
    Make a trading decision based on detected support levels.

    Args:
    price_data (pd.Series): A series of price data.
    window_size (int): The size of the rolling window to identify local minima.
    tolerance (float): Tolerance for considering price is near the support level (as a fraction of price).

    Returns:
    str: A trading decision ('Buy', 'Short', 'Neutral').
    """
    # Détecter les niveaux de support
    support_info = detect_support_levels(price_data, window_size)
    
    # Dernier prix disponible
    last_price = price_data.iloc[-1]
    
    # Trouver le niveau de support le plus proche du dernier prix
    closest_support = support_info.iloc[(support_info['Support Level'] - last_price).abs().argsort()[:1]]

    if not closest_support.empty:
        support_level = closest_support['Support Level'].values[0]
        # Si le prix est proche d'un niveau de support
        if abs(last_price - support_level) <= tolerance * last_price:
            return 'achat'  # Acheter si proche du support
        elif last_price < support_level:
            return 'vente'  # Shorter si le prix est en-dessous du support
        else:
            return 'neutre'  # Neutre si le prix est loin du support
    else:
        return 'neutre'  # Neutre si aucun support n'est détecté ou significatif
    
def detect_support_levels(price_data, window_size=20):
    """
    Detect support levels in price data.

    Args:
    price_data (pd.Series): A series of price data.
    window_size (int): The size of the rolling window to identify local minima.

    Returns:
    pd.DataFrame: A DataFrame with support levels and their occurrences.
    """
    # Trouver les minimas locaux
    minima = price_data.rolling(window=window_size, center=True).min()
    
    # Filtrer les minimas uniques
    support_levels = minima.drop_duplicates().dropna()
    
    # Compter le nombre d'occurrences de chaque niveau de support
    support_counts = minima.value_counts()
    
    # Préparer le DataFrame de sortie
    support_info = pd.DataFrame({
        'Support Level': support_levels.values,
        'Occurrences': support_counts.loc[support_levels.values].values
    }).sort_values(by='Support Level')
    
    return support_info

