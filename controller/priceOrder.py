from controller.tplsgenerator import calculate_tp_sl
from function.indicator import check_bollinger, check_ichimoku, check_ma, check_macd, check_rsi
from utils.json_custom import json_to_pd
from utils.rendement import estimate_returns
from utils.volatility import calculate_volatility

def priceOrder(API, period, nb):
    candles = API.get_Candles(period=period,symbol="ETHEREUM", qty_candles=nb)
    
    
    filtered_data = [item for item in candles if "digits" not in item]
    data = json_to_pd(filtered_data)
    
    vola = calculate_volatility(data['close'])
    print(f"La volatilité annuelle de l'actif est de: {vola:.2%}")
        
    daily_return, annualized_return = estimate_returns(data['close'])
    print(f"Rendement moyen quotidien: {daily_return:.4f}")
    print(f"Rendement annuelisé: {annualized_return:.4f}")    
    
    tp, sl = calculate_tp_sl(data)
    
    reponse = []
    
    moyenMobile = check_ma(data, nb)
    
    reponse.append(moyenMobile)
    
    moyenMobileDivergenceConvergence = check_macd(data)
    
    reponse.append(moyenMobileDivergenceConvergence)
    
    rsi = check_rsi(data)
    
    reponse.append(rsi)
    
    bollinger = check_bollinger(data, nb)
    
    reponse.append(bollinger)
    
    ichimoku = check_ichimoku(data)
    
    reponse.append(ichimoku)

    return reponse, tp, sl