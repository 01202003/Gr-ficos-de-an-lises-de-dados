"""this file is for education""" #isso daq server pro pylint n ficar notificando um erro q fala pra vc colocar esse textinho de bla bla

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.io as pio

# Definindo a largura máxima das colunas (gpt)
pd.set_option('display.max_columns', None)

# Definindo a largura máxima das colunas para exibir todas as informações (gpt)
pd.set_option('display.max_colwidth', None)

# Definindo o número máximo de linhas a serem exibidas (gpt)
pd.set_option('display.max_rows', 10)

df_principal = pd.read_excel("C:/Users/haine/OneDrive/Documentos/ESTUDOS/IMERSÃO PYTON PLANILHA ALURA/Imersão Python - Tabela de ações.xlsx", sheet_name="Principal")

df_total_de_acoes = pd.read_excel("C:/Users/haine/OneDrive/Documentos/ESTUDOS/IMERSÃO PYTON PLANILHA ALURA/Imersão Python - Tabela de ações.xlsx", sheet_name="Total_de_acoes")

df_ticker = pd.read_excel("C:/Users/haine/OneDrive/Documentos/ESTUDOS/IMERSÃO PYTON PLANILHA ALURA/Imersão Python - Tabela de ações.xlsx", sheet_name="Ticker")

df_principal = df_principal [['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']]

df_principal = df_principal.rename(columns={'Último (R$)':'Valor_Final', "Var. Dia (%)":'Var_Dia_Porc'}).copy()

df_principal['Var_porc'] = df_principal['Var_Dia_Porc'] /100

df_principal['Valor_Inicial'] = df_principal['Valor_Final'] / (df_principal['Var_porc']+1)

df_principal = df_principal.merge(df_total_de_acoes, left_on='Ativo', right_on='Código', how='left') #juntando informações de uma planilha com a outra

df_principal = df_principal.drop(columns=['Código']) #excluindo a coluna repetida

df_principal['Varia._Dinho'] = (df_principal['Valor_Final'] - df_principal['Valor_Inicial']) * df_principal['Qtde. Teórica']

df_principal = df_principal.rename(columns={'Qtde. Teórica':'N_de_acoes'}).copy() #mudei o Qtde de Ações pra N de acoes

pd.options.display.float_format =  '{:.2f}'.format #formata os n pra aparecer numeros quebrados

df_principal['N_de_acoes'] = df_principal['N_de_acoes'].astype(int) #ta formatando o n de ações pra aparecer como numeros inteiros

df_principal['Resultado'] = df_principal['Varia._Dinho'].apply(lambda x: 'Subiu' if x>0 else ('Desceu' if x<0 else 'Estável')) #ta categorizando cada linha com as variaveis dizendo se a variação do dinheiro subiu, desceu ou ficou estável

df_principal = df_principal.merge(df_ticker, left_on='Ativo', right_on='Ticker', how='left')
df_principal = df_principal.drop(columns=['Ticker'])

df_chatgpt = pd.read_excel("C:/Users/haine/OneDrive/Documentos/ESTUDOS/IMERSÃO PYTON PLANILHA ALURA/Imersão Python - Tabela de ações.xlsx", sheet_name="chatgpt")

df_principal = df_principal.merge(df_chatgpt, left_on='Nome', right_on='Empresas', how='left')
df_principal = df_principal.drop(columns=['Empresas'])

df_principal = df_principal.rename(columns={'Idade em anos':'Idade_Anos'})

df_principal['Idade_Anos'] = df_principal['Idade_Anos'].fillna(0)
df_principal['Idade_Anos'] = df_principal['Idade_Anos'].astype(int) #comando q o chatgpt me deu pra corrigir todos os numeros da coluna de idade, já que estava dizendo q tais numeros eram "não finitos", ai o comando substitui eles por 0; o inplace significa q ele vai colocar todas essas informações substituindo os numeros antigos, sem criar outra coluna com numeros novos

df_principal['Cat_Idade'] = df_principal['Idade_Anos'].apply(lambda x: 'Mais de 100' if x>100 else('Menos de 50' if x<50 else 'Entre 50 e 100'))

maior = df_principal['Varia._Dinho'].max()
menor = df_principal['Varia._Dinho'].min()
media = df_principal['Varia._Dinho'].mean()
media_subiu = df_principal[df_principal ['Resultado'] == 'Subiu']['Varia._Dinho'].mean()
media_desceu = df_principal[df_principal ['Resultado'] == 'Desceu']['Varia._Dinho'].mean()

df_principal_subiu = df_principal[df_principal['Resultado'] == 'Subiu']

df_analise_segmento = df_principal_subiu.groupby('Segmento')['Varia._Dinho'].sum().reset_index() #agrupando as informações doq subiu por segmento e depois somando a variação em dinheiro

df_analise_saldo = df_principal.groupby('Resultado')['Varia._Dinho'].sum().reset_index()

#print moments

print(df_principal)
print(df_principal_subiu)
print(df_analise_segmento)
print(df_analise_saldo)
print(f"Maior\tR$ {maior:,.2f}")
print(f"Menor\tR$ {menor:,.2f}")
print(f"Média\tR$ {media:,.2f}")
print(f"Média de quem subiu\tR$ {media_subiu:,.2f}")
print(f"Média de quem desceu\tR$ {media_desceu:,.2f}")

#px moments
fig = px.bar(df_analise_saldo, x= 'Resultado', y= 'Varia._Dinho', text='Varia._Dinho', title= 'Variação em Reais dos Resultados')
pio.write_image(fig, 'grafico_barra.png')

# Converter valores negativos para positivos
df_analise_saldo['Varia._Dinho'] = df_analise_saldo['Varia._Dinho'].abs()
fig = go.Figure(data=[go.Pie(labels=df_analise_saldo['Resultado'], values=df_analise_saldo['Varia._Dinho'])])
fig.update_layout(title='Variação em Reais dos Resultados')
pio.write_image(fig, 'grafico_pizza.png')

print("Gráfico salvo em: grafico_pizza.png") #ele vai abrir uma janela pra mostrar o gráfico, acho q o vs code nn lê no terminal dele
