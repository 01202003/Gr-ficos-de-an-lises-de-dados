"""this file is for education"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import yfinance as yf #api q procura coisas de valores de empresas e é americana
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pd.set_option('display.max_columns', None)


dados = yf.download('PETR4.SA', start='2023-01-01', end='2023-12-31')

#dessa forma de renomeação é preciso renomear todas as colunas em ordem
dados.columns = ['Abertura', 'Maximo', 'Minimo', 'Fechamento', 'Fech_Ajus', 'Volume']

dados = dados.rename_axis('Data')

dados['Fechamento'].plot(figsize=(10,6))

#

dados = dados.head(60).copy()
dados['Data'] = dados.index #esse é oq o chatgpt me deu e funcionou
#este é do curso e n funcionou: dados['Data'] = dados.index #convertendo o indice me uma coluna de data

dados['Data'] = dados['Data'].apply(mdates.date2num) #ta transformando a data em um número q o matplot entende, q o computador entende

#fig ax é o princel desenhando o código
  #montou o fundo branco e as linhas do graf. velas petr4
fig, ax = plt.subplots(figsize=(15, 8))

 #definindo a largura dos candles no grafico
width = 0.7

 #estrutura de repetição
  #o len aqui é 60, ou seja, largura 60; len é de largura em ing;range conta de 0 ate o tamanho do len (de 0 a 60 itens); entao ele vai data a data escrevendo 60 itens
for i in range(len(dados)):
    if dados['Fechamento'].iloc[i] > dados['Abertura'].iloc[i]:
        color = 'green'
    else:
        color = 'red'

    ax.plot([dados['Data'].iloc[i], dados['Data'].iloc[i]],
            [dados['Minimo'].iloc[i], dados['Maximo'].iloc[i]],
            color=color, linewidth=1)

    # Adiciona o retângulo (candlestick) para cada linha do DataFrame
    rect = plt.Rectangle((dados['Data'].iloc[i] - width/2, dados['Abertura'].iloc[i]), 
                         width, abs(dados['Fechamento'].iloc[i] - dados['Abertura'].iloc[i]), 
                         facecolor=color)
    ax.add_patch(rect)

#o i no caso é de interação; aqui define se i é fechamento ou abertura, atribuindo as cores vermelha e verde pra fechamnto e abertura respectivamente
    #O .iloc é usado para acessar os valores da coluna 'Fechamento' do DataFrame dados por meio de sua posição numérica. Por exemplo, se você quiser acessar o valor na primeira linha da coluna 'Fechamento', você usaria .iloc[0]. Se quiser acessar o valor na segunda linha, usaria .iloc[1], e assim por diante(DO FOR ATE O COLOR RED)

#desenhando a linha vertical de candle (mecha)
  #essa linha mostra os preços maximos e minimos do dia (topo e base da linha)
  #usamos o ax.plot pra desenha uma linha vertical
  #[dados['Data'].iloc[i], dados['Data'].iloc] define o ponto x da linha (data), e dados['Minimo'].iloc[i], dados['Maximo'].iloc[i] define a coluna, a candle (AX.PLOT ATE O LINE WIDTH=1)

#tá na hora de fazer retangulo, a vela
 #add_patch adiciona objetos dentro do plot, o retangulo no caso(DA LINHA DO ADD PATCH)

dados['MA7'] = dados['Fechamento'].rolling(window=7).mean()
dados['MA14'] = dados['Fechamento'].rolling(window=14).mean()

# Agora plotando a linha de média móvel
ax.plot(dados['Data'], dados['MA7'], color='orange', label='Média de 7 dias')
ax.plot(dados['Data'], dados['MA14'], color='yellow', label='Média de 14 dias')
# Adicionando legenda da média móvel
ax.legend()

#esse daq eu copiei do codigo da alura

# Formatando o eixo x para mostrar as datas
# Configuramos o formato da data e a rotação para melhor legibilidade
ax.xaxis_date() #O método xaxis_date() é usado para dizer ao Matplotlib que as datas estão sendo usadas no eixo x
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# Adicionando título e rótulos para os eixos x e y
plt.title("Gráfico de Candlestick - PETR4.SA com matplotlib")
plt.xlabel("Data")
plt.ylabel("Preço")

# Adicionando uma grade para facilitar a visualização dos valores
plt.grid(True)
#vai ate aq o copiar


###aqui começa a parte da aula pra deixar o gráfico interativo!

# Criando subplots
'''
"Primeiro, criamos uma figura que conterá nossos gráficos usando make_subplots.
Isso nos permite ter múltiplos gráficos em uma única visualização.
Aqui, teremos dois subplots: um para o gráfico de candlestick e outro para o volume de transações."

'''
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=('Candlesticks', 'Volume Transacionado'),
                    row_width=[0.2, 0.7])

'''
"No gráfico de candlestick, cada candle representa um dia de negociação,
mostrando o preço de abertura, fechamento, máximo e mínimo. Vamos adicionar este gráfico à nossa figura."
'''
# Adicionando o gráfico de candlestick
fig.add_trace(go.Candlestick(x=dados.index,
                             open=dados['Abertura'],
                             high=dados['Maximo'],
                             low=dados['Minimo'],
                             close=dados['Fechamento'],
                             name='Candlestick'),
                             row=1, col=1)

# Adicionando as médias móveis
# Adicionamos também médias móveis ao mesmo subplot para análise de tendências
fig.add_trace(go.Scatter(x=dados.index,
                         y=dados['MA7'],
                         mode='lines',
                         name='MA7 - Média Móvel 7 Dias'),
                         row=1, col=1)

fig.add_trace(go.Scatter(x=dados.index,
                         y=dados['MA14'],
                         mode='lines',
                         name='MA14 - Média Móvel 14 Dias'),
                         row=1, col=1)

# Adicionando o gráfico de barras para o volume
# Em seguida, criamos um gráfico de barras para o volume de transações, que nos dá uma ideia da atividade de negociação naquele dia
fig.add_trace(go.Bar(x=dados.index,
                     y=dados['Volume'],
                     name='Volume'),
                     row=2, col=1)

# Atualizando layout
#Finalmente, configuramos o layout da figura, ajustando títulos, formatos de eixo e outras configurações para tornar o gráfico claro e legível.
fig.update_layout(yaxis_title='Preço',
                  xaxis_rangeslider_visible=False,  # Desativa o range slider
                  width=1100, height=600)

# Exibindo o gráfico (navegador)
fig.show(renderer="browser")

print(dados)
