from scipy.optimize import minimize
import numpy as np
import pandas as pd

def allocate_assets(returns, prices, total_investment, risk_tolerance):
    """
    Calcule l'allocation d'actifs optimale et la quantité maximale d'actifs à acheter.
    
    :param returns: DataFrame contenant les rendements historiques des actifs.
    :param prices: DataFrame contenant les prix actuels des actifs.
    :param total_investment: Montant total que l'investisseur est prêt à investir.
    :param risk_tolerance: Un float qui représente la tolérance au risque de l'investisseur (plus élevé signifie plus de risque).
    :return: Un dictionnaire contenant l'allocation pourcentage de chaque actif et la quantité à acheter.
    """
    
    # Calculer la matrice de covariance des rendements
    covariance_matrix = returns.cov()
    
    # Initialiser les poids de manière égale
    initial_weights = np.array([1.0 / len(returns.columns)] * len(returns.columns))
    
    # Contrainte: la somme des poids doit être égale à 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    
    # Limiter les poids à des valeurs entre 0 et 1
    bounds = tuple((0, 1) for asset in range(len(returns.columns)))
    
    # Fonction objectif pour minimiser la variance du portefeuille ajustée par la tolérance au risque
    def portfolio_variance(weights):
        return risk_tolerance * (weights.T @ covariance_matrix @ weights)
    
    # Optimisation pour minimiser la variance ajustée selon la tolérance au risque
    result = minimize(portfolio_variance, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    
    # Créer un dictionnaire pour l'allocation d'actifs et la quantité à acheter
    allocation = {}
    for i, weight in enumerate(result.x):
        asset_name = returns.columns[i]
        allocated_amount = weight * total_investment
        asset_quantity = allocated_amount / prices[asset_name].iloc[-1]
        allocation[asset_name] = {
            'percentage': round(weight * 100, 2),
            'quantity': np.floor(asset_quantity)  # Arrondir à la baisse pour éviter d'acheter plus que possible
        }
    
    return allocation

# Exemple d'utilisation
data = {
    'ETH': np.random.normal(0.12, 0.3, 1000000),
    'BTC': np.random.normal(0.15, 0.35, 1000000),
    'SOL': np.random.normal(0.19, 0.40, 1000000),
    'USD': np.random.normal(0.01, 0.01, 1000000),
}
returns = pd.DataFrame(data)
prices = pd.DataFrame({
    'ETH': [2000],  # Prix actuel d'ETH
    'BTC': [50000], # Prix actuel de BTC
    'SOL': [150],    # Prix actuel de SOL
    'USD': [1]

})
total_investment = 20000  # Total de $10,000 à investir
risk_tolerance = 0.1

allocation = allocate_assets(returns, prices, total_investment, risk_tolerance)
print("Allocation d'actifs optimale et quantités à acheter:", allocation)
