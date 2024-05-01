def detect_candlestick(open, high, low, close):
    # Calcul de la taille du corps et des mèches
    body_size = abs(close - open)
    upper_wick = high - max(open, close)
    lower_wick = min(open, close) - low

    # Tolérance pour les variations mineures
    epsilon = 0.001 * (high - low)  # ajustez cette tolérance selon la volatilité

    # Détection des types de bougies et conseils d'achat/vente
    if body_size < epsilon and upper_wick > body_size and lower_wick > body_size:
        return 'neutre'
    elif open == low and close == high and body_size > (high - low) * 0.95:
        return 'achat'
    elif open == high and close == low and body_size > (high - low) * 0.95:
        return 'vente'
    elif close > open and lower_wick >= 2 * body_size and upper_wick < body_size:
        return 'achat'
    elif open > close and lower_wick >= 2 * body_size and upper_wick < body_size:
        return 'achat'
    elif close > open:
        return 'achat'
    elif open > close:
        return 'vente'
    else:
        return 'neutre'
