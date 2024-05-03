import pandas as pd
import numpy as np
def estimate_window_size( min_window=5, max_window=50):
    """
    Estimate the rolling window size for detecting support levels based on historical volatility.

    Args:
    price_data (pd.Series): A series of price data, assumed to have a 'close' column.
    min_window (int): Minimum size of the window.
    max_window (int): Maximum size of the window.

    Returns:
    int: An estimated window size.
    """
    # Estimer la taille de la fenêtre en fonction de la volatilité
    window_size = int((12 * (max_window - min_window)) + min_window)

    # Assurer que la taille de la fenêtre est au moins le minimum et au plus le maximum
    window_size = max(min_window, min(max_window, window_size))

    return window_size

