import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

urls = ["https://brapi.dev/api/quote/VALE3?range=1mo&interval=1d", 
        "https://brapi.dev/api/quote/PETR4?range=1mo&interval=1d",
        "https://brapi.dev/api/quote/WEGE3?range=1mo&interval=1d"]

def extrair_dados():
    # criar a figura e os subplots
    sns.set_style('darkgrid')
    sns.set(rc={'figure.facecolor':'#d9d9d9'})
    fig, axs = plt.subplots(len(urls), 1, figsize=(12,9))

    for i, url in enumerate(urls):
        response = requests.get(url)
        valores = []
        datas = []
        data = response.json()
        novo = data["results"][0]
        data_histor = novo['historicalDataPrice']
        for j in data_histor:
            valor = j['close']
            data1 = dt.datetime.utcfromtimestamp(j['date'])
            data_form = data1.strftime('%Y-%m-%d')
            valores.append(valor)
            datas.append(data_form)

        # criar um DataFrame do pandas
        df = pd.DataFrame({'Data': datas, 'Valor': valores})
        df['Data'] = pd.to_datetime(df['Data'])

        # configurar a coluna "Data" como índice do DataFrame
        df.set_index('Data', inplace=True)

        # plotar o gráfico no subplot correspondente
        sns.lineplot(data=df, x='Data', y='Valor', ax=axs[i], color='green', marker='o')
        axs[i].legend(labels=["Valor"])
        axs[i].set_xlabel('Data', fontsize=14)
        axs[i].set_ylabel('Valor', fontsize=14)
        axs[i].set_title(f'Variação do valor das ações {novo["symbol"]}', fontsize=16)
        axs[i].tick_params(axis='both', labelsize=12)
        for x, y in zip(df.index, df['Valor']):
            axs[i].annotate(f'{y:.1f}', (x, y), textcoords="offset points", xytext=(0, 1.5), ha='center') 
    
    plt.tight_layout()
    plt.show()
   


