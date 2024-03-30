"""this file is for education"""

import webbrowser
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import yfinance as yf #api q procura coisas de valores de empresas e é americana
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dados = yf.download('AAPL', start='2023-01-01', end='2023-12-31')
# Crie o gráfico e salve em um arquivo HTML
mpf.plot(dados.head(30), type='candle', figsize=(16, 8), volume=True, mav=(7, 14), style='charles', savefig='grafico.webp')

# Abra o arquivo HTML no navegador
webbrowser.open('grafico.webp')

##COMANDO PRA ABRIR COM O JUPYTER: jupyter notebook