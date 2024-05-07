import time
import pandas as pd
import yfinance as yf

def fetch_financial_data():
    # Exemple de liste de symboles du S&P 500 (réduit pour l'exemple)
    sp500_symbols = [ 'A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACN', 'ACE', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADS', 'ADSK', 'ADT', 'AEE',
    'AEP', 'AES', 'AET', 'AFL', 'AGN', 'AIG', 'AIV', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALK', 'ALL', 'ALLE', 'ALXN', 'AMAT', 'AMD', 'AME',
    'AMGN', 'AMP', 'AMT', 'AMZN', 'AN', 'ANSS', 'ANTM', 'AON', 'APA', 'APC', 'APD', 'APH', 'APO', 'APTV', 'ARE', 'ARG', 'ATI', 'ATO',
    'ATR', 'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO', 'BA', 'BAC', 'BAX', 'BBT', 'BBY', 'BDX', 'BEAV', 'BEN', 'BF-B', 'BHI',
    'BIIB', 'BIO', 'BK', 'BKNG', 'BLK', 'BLL', 'BMY', 'BMRN', 'BR', 'BRK-B', 'BRO', 'BSX', 'BTU', 'BUD', 'BXP', 'C', 'CAG', 'CAH', 'CAT',
    'CB', 'CBOE', 'CBRE', 'CBS', 'CCE', 'CCI', 'CCL', 'CDNS', 'CDW', 'CE', 'CELG', 'CERN', 'CF', 'CFR', 'CHD', 'CHRW', 'CI', 'CINF',
    'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNP', 'CNX', 'COF', 'COG', 'COH', 'COL', 'COP', 'COST', 'COTY', 'CPB',
    'CPRT', 'CRM', 'CSC', 'CSCO', 'CSX', 'CTAS', 'CTSH', 'CTXS', 'CTVA', 'CVX', 'CW', 'CZR', 'D', 'DAL', 'DD', 'DDS', 'DE', 'DELL',
    'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISCA', 'DISCK', 'DISH', 'DK', 'DLR', 'DLTR', 'DNB', 'DO', 'DOV', 'DOW', 'DPS', 'DRI',
    'DTE', 'DUK', 'DVA', 'DVN', 'DXCM', 'DXR', 'EA', 'EAT', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR', 'ENDP', 'EOG',
    'EQIX', 'EQR', 'ES', 'ESS', 'ETFC', 'ETN', 'ETR', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FAST', 'FB', 'FCX', 'FDC',
    'FDX', 'FE', 'FIS', 'FISV', 'FITB', 'FLIR', 'FLS', 'FLT', 'FMC', 'FOSL', 'FOX', 'FOXA', 'FRX', 'FSLR', 'FTV', 'FTI', 'FTR', 'GAS',
    'GD', 'GE', 'GILD', 'GIS', 'GLW', 'GM', 'GME', 'GNRC', 'GNW', 'GOOGL', 'GOOG', 'GPC', 'GPS', 'GRMN', 'GS', 'GWW', 'HAL', 'HAR',
    'HAS', 'HBAN', 'HBI', 'HCA', 'HD', 'HES', 'HIG', 'HII', 'HON', 'HRL', 'HRS', 'HST', 'HSY', 'HUM', 'IBM', 'ICE', 'IDXX', 'IEX',
    'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 'IP', 'IPG', 'IQV', 'IR', 'IRM', 'ITW', 'IVZ', 'JBHT', 'JCI', 'JEC', 'JNJ', 'JPM', 'K',
    'KEY', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KO', 'KR', 'KSS', 'L', 'LABL', 'LB', 'LBTYA', 'LBTYB', 'LBTYK', 'LC', 'LEG', 'LEN',
    'LH', 'LHX', 'LIN', 'LKQ', 'LLL', 'LLY', 'LM', 'LMT', 'LNC', 'LNT', 'LO', 'LOW', 'LRCX', 'LUV', 'LYB', 'LYV', 'M', 'MA', 'MAA',
    'MAC', 'MAR', 'MAS', 'MAT', 'MCD', 'MCK', 'MDLZ', 'MDT', 'MET', 'MGM', 'MHK', 'MKC', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MON',
    'MOS', 'MPC', 'MRK', 'MRO', 'MS', 'MSFT', 'MSI', 'MTB', 'MTD', 'MU', 'MYL', 'NDAQ', 'NEE', 'NEM', 'NFLX', 'NFX', 'NI', 'NKE',
    'NL', 'NOC', 'NOV', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUAN', 'NUE', 'NVDA', 'NWL', 'NWSA', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OXY',
    'PAYX', 'PBCT', 'PCAR', 'PCG', 'PCL', 'PCLN', 'PCP', 'PDCO', 'PEP', 'PETM', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD',
    'PM', 'PNC', 'PNR', 'PNW', 'POM', 'PPG', 'PPL', 'PX', 'PXD', 'QCOM', 'QRVO', 'R', 'RAI', 'RCL', 'REG', 'REGN', 'RF', 'RHI', 'RHT',
    'RIG', 'RJF', 'RL', 'ROK', 'ROL', 'ROP', 'ROST', 'RRC', 'RSG', 'RTN', 'SBAC', 'SBNY', 'SBUX', 'SCG', 'SCHW', 'SE', 'SEE', 'SHW',
    'SIG', 'SJM', 'SLB', 'SLG', 'SLM', 'SNP', 'SNPS', 'SNV', 'SO', 'SPG', 'SPLS', 'SRE', 'STI', 'STJ', 'STT', 'STX', 'STZ', 'SWK',
    'SWKS', 'SYF', 'SYK', 'SYMC', 'SYY', 'T', 'TAP', 'TDG', 'TDC', 'TEF', 'TEL', 'TER', 'TFC', 'TGT', 'TGNA', 'THC', 'THO', 'THS',
    'TIF', 'TJX', 'TMO', 'TNAV', 'TOL', 'TPR', 'TROW', 'TRV', 'TSCO', 'TSN', 'TSS', 'TWX', 'TXN', 'TXT', 'TYC', 'TWC', 'TWTR', 'TWO',
    'UA', 'UHS', 'UNH', 'UNP', 'UNUM', 'UPS', 'URI', 'USB', 'USG', 'UTX', 'VAR', 'VFC', 'VLO', 'VMC', 'VNO', 'VRSN', 'VRTX', 'VTR',
    'VZ', 'WAB', 'WAG', 'WAT', 'WBA', 'WDC', 'WEC', 'WELL', 'WFC', 'WFM', 'WHR', 'WIN', 'WMB', 'WM', 'WMT', 'WNC', 'WPG', 'WU', 'WY',
    'WYN', 'XEL', 'XLNX', 'XOM', 'XRX', 'XYL', 'YHOO', 'YUM', 'ZION', 'ZMH', 'ZTS']

    # Initialiser un DataFrame pour stocker les résultats financiers
    financial_data = pd.DataFrame()

    for symbol in sp500_symbols:
        try:
            print(f"Fetching data for {symbol}")
            # Télécharger les données historiques
            ticker = yf.Ticker(symbol)
            
            fin_data = ticker.financials  # Utiliser 'financials' pour les états financiers
            
            # Ajouter une colonne pour le symbole
            fin_data['Symbol'] = symbol
            
            # Transposer les données financières pour aligner les dates en lignes
            fin_data_transposed = fin_data.T
            
            # Concaténer les données dans le DataFrame principal
            financial_data = pd.concat([financial_data, fin_data_transposed])
            
        except Exception as e:
            print(f"Erreur lors du téléchargement des données pour {symbol}: {e}")
        time.sleep(1)  # Pause pour éviter de surcharger l'API

    # Réinitialiser l'index pour une meilleure organisation une fois toutes les données téléchargées
    financial_data.reset_index(inplace=True, drop=False)
    print(financial_data.head())

    # Sauvegarder les résultats dans un fichier CSV
    financial_data.to_csv('sp500_financial_data.csv', index=False)

fetch_financial_data()
