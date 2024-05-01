from controller.tplsgenerator import calculate_tp_sl
from function.candelier_detector import detect_candlestick
from function.indicator import check_bollinger, check_ichimoku, check_ma, check_macd, check_rsi
from utils.json_custom import json_to_pd

def priceOrder(API, period, nb, currency):
    candles = API.get_Candles(period=period,symbol=currency, qty_candles=nb)
    
    print(currency, candles[-1])
    
    filtered_data = [item for item in candles if "digits" not in item]
    data = json_to_pd(filtered_data)

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
    
    candle = detect_candlestick(data.iloc[-1]['open'],data.iloc[-1]['high'],data.iloc[-1]['low'], data.iloc[-1]['close'])
    
    return reponse, tp, sl, candle