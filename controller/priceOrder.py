from controller.tplsgenerator import calculate_tp_sl
from function.candelier_detector import detect_candlestick
from function.indicator import check_bollinger, check_ichimoku, check_ma, check_macd, check_rsi
from tatics.H4 import trading_signals_4H
from tatics.M30 import trading_signals_30M
from utils.json_custom import json_to_pd

def priceOrder(API, period, nb, currency):
    candles = API.get_Candles(period=period,symbol=currency, qty_candles=nb)
        
    filtered_data = [item for item in candles if "digits" not in item]
    data = json_to_pd(filtered_data)
    
    tp, sl = calculate_tp_sl(data)
    
    reponse = 'neutre'
    
    if period == "M30":
        data = trading_signals_30M(data)
        reponse = data['Signal'].iloc[-1]
        return reponse, tp, sl
        
    if period == "H4":
        data = trading_signals_4H(data)
        reponse = data['Signal'].iloc[-1]
        return reponse, tp, sl
    
    if period == "D1":
        return reponse, tp, sl