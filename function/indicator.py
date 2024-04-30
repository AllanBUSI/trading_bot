import pandas as pd
import ta


def check_ma(data, window):
    ma = data['close'].rolling(window=window).mean()
    last_close = data['close'].iloc[-1]
    last_ma = ma.iloc[-1]
    
    if last_close > last_ma:
        return 'achat'
    elif last_close < last_ma:
        return 'vente'
    else:
        return 'neutre'

def check_macd(data):
    macd_indicator = ta.trend.MACD(data['close'])
    
    macd_diff = macd_indicator.macd_diff()
    
    if macd_diff.iloc[-1] > 0 and macd_diff.iloc[-2] < 0:
        return 'achat'
    elif macd_diff.iloc[-1] < 0 and macd_diff.iloc[-2] > 0:
        return 'vente'
    else:
        return 'neutre'

def check_rsi(data, window=14):
    rsi = ta.momentum.RSIIndicator(data['close'], window=window).rsi()
    
    if rsi.iloc[-1] < 30:
        return 'achat'
    elif rsi.iloc[-1] > 70:
        return 'vente'
    else:
        return 'neutre'

def check_bollinger(data, window=20):
    bollinger = ta.volatility.BollingerBands(data['close'], window=window, window_dev=2)
    last_close = data['close'].iloc[-1]
    
    if last_close < bollinger.bollinger_lband().iloc[-1]:
        return 'achat'
    elif last_close > bollinger.bollinger_hband().iloc[-1]:
        return 'vente'
    else:
        return 'neutre'

def check_ichimoku(data):
    ichimoku = ta.trend.IchimokuIndicator(high=data['high'], low=data['low'], window1=9, window2=26, window3=52)

    conversion_line = ichimoku.ichimoku_conversion_line()
    base_line = ichimoku.ichimoku_base_line()
    leading_span_a = ichimoku.ichimoku_a()
    leading_span_b = ichimoku.ichimoku_b()
    lagging_span = data['close'].shift(-26)  # Le décalage est appliqué pour que la ligne soit 26 périodes derrière

    last_close = data['close'].iloc[-1]
    last_leading_span_a = leading_span_a.iloc[-26]  # Décalage pour aligner avec les prix actuels
    last_leading_span_b = leading_span_b.iloc[-26]  # Décalage pour aligner avec les prix actuels

    if last_close > max(last_leading_span_a, last_leading_span_b):
        return 'achat'  # Signal d'achat si le prix de clôture est au-dessus du nuage
    elif last_close < min(last_leading_span_a, last_leading_span_b):
        return 'vente'  # Signal de vente si le prix de clôture est en dessous du nuage
    else:
        return 'neutre'  # Aucun signal si le prix est dans le nuage
