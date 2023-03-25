import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import Tk, StringVar, ttk
import customtkinter as tkc
from PIL import Image, ImageTk
from grafico import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from sms import *

urls = ['https://www.google.com/search?q=cota%C3%A7%C3%A3o+dolar','https://www.google.com/search?q=bitcoin+dolar', 'https://www.google.com/search?q=ethereum+dolar', 'https://www.google.com/search?q=cardano+dolar', 'https://brapi.dev/api/quote/PETR4%2CVALE3%2CWEGE3%2CKLBN4%2CBBAS3']

def cotacao(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        cotacao = soup.find('span', {'class': 'pclqee'}).text
        nome_moeda = soup.find('span',{'class': "wUrVib OSrXXb"}).text

        return nome_moeda[10:] + ' ' + cotacao + ' ' + 'USD'
    
    except:
        cotacao = soup.find('span', {'class': 'DFlfde SwHCTb'}).text
        nome_moeda = soup.find('span',{'class':'vLqKYe'}).text
        
        return nome_moeda[:5] + ' ' + cotacao + ' ' + 'USD'

def cotacao_acoes(url):
    lista = []
    cotacao = requests.get(url)
    cotacao = cotacao.json()
    cotacao_todos = cotacao['results']
    for i in cotacao_todos:
        nome = i['symbol']
        preco = i['regularMarketPrice']
        completo = nome + ' ' + str(preco) + ' ' +'R$' 
        lista.append(completo)
    
    return lista

def atualizar_cotacao():
    cotacoes = []
    if var.get() == 0:
        cotacoes.append(cotacao(urls[0]))
    elif var.get() == 1:
       for url in urls[1:-1]:
            cotacoes.append(cotacao(url))
    else:
        acao = cotacao_acoes(urls[-1])
        for i in acao:
            cotacoes.append(i)
    label_cotacao.configure(text='\n'.join(cotacoes))

    valore_para_sms = label_cotacao._text

    #chama a função de habilitar o checkbutton do grafico
    verificar_botao()

    return valore_para_sms

#habilitar botao sms depois de clicar no botao de cotação
def habilitar_btn_sms():
    btn_sms.configure(state=tkc.NORMAL)


app = tkc.CTk()
app.geometry('450x450')
app.title('Cotação')

#logo
imagem = tkc.CTkImage(dark_image=Image.open('dolar.png'), size=(45, 45))
logo = tkc.CTkLabel(app, text="", height=10, image=imagem)
logo.place(x=70,y=12)

#texto intro
intro = tkc.CTkLabel(app, text="Cotação Atual", font=('Ivy', 28, 'bold'), height=10)
intro.place(x=145,y=18)

linha = tkc.CTkLabel(app, text="", width=450, height=1, font=('Ivy', 1), fg_color=('#1cacfc'))
linha.place(x=0,y=70)

# Variável do Checkbutton
var = tkc.IntVar()
var.set(0)

# Frame para o Checkbutton
frame = tkc.CTkFrame(app)
frame.pack(padx=10, pady=100)

check_dolar = tkc.CTkRadioButton(frame, text="Dólar", font=('Ivy', 14), text_color='white', fg_color=('#1cacfc'), variable=var, value=0, border_width_checked=4, border_width_unchecked=2, radiobutton_width=15, radiobutton_height=15)
check_dolar.pack(side=tkc.LEFT, padx=5)

check_moedas = tkc.CTkRadioButton(frame, text="Moedas", font=('Ivy', 14), text_color='white', fg_color=('#1cacfc'), variable=var, value=1, border_width_checked=4, border_width_unchecked=2, radiobutton_width=15, radiobutton_height=15)
check_moedas.pack(side=tkc.LEFT, padx=5)

check_acoes = tkc.CTkRadioButton(frame, text="Ações", font=('Ivy', 14), text_color='white', fg_color=('#1cacfc'), variable=var, value=2, border_width_checked=4, border_width_unchecked=2, radiobutton_width=15, radiobutton_height=15)
check_acoes.pack(side=tkc.LEFT, padx=5)

# Variável do Checkbutton de grafico
var2 = tkc.IntVar()
var2.set(0)

# Frame para o Checkbutton de grafico
frame2 = tkc.CTkFrame(app)
frame2.place(x=35, y=150)

#função para verifcar se deve habilitar o checkbutton de grafico
    
def verificar_botao():
    #limpa botao antigo e cria um novo
    if check_acoes._check_state == True:
        
        for widget in frame2.winfo_children():
            widget.destroy()

        check_dolar2 = tkc.CTkRadioButton(frame2, text="Grafico Petrobras", text_color='white', font=('Ivy', 14), fg_color=('#1cacfc'), variable=var2, value=0, border_width_checked=4, border_width_unchecked=2, radiobutton_width=15, radiobutton_height=15)
        check_dolar2.pack(side=tkc.LEFT, padx=5)

        check_moedas2 = tkc.CTkRadioButton(frame2, text="Grafico Weg", text_color='white', font=('Ivy', 14), fg_color=('#1cacfc'), variable=var2, value=1, border_width_checked=4, border_width_unchecked=2, radiobutton_width=15, radiobutton_height=15)
        check_moedas2.pack(side=tkc.LEFT, padx=5)

        check_acoes2 = tkc.CTkRadioButton(frame2, text="Grafico Vale", text_color='white', font=('Ivy', 14), fg_color=('#1cacfc'), variable=var2, value=2, border_width_checked=4, border_width_unchecked=2, radiobutton_width=15, radiobutton_height=15)
        check_acoes2.pack(side=tkc.LEFT, padx=5)
        
    else:
        for widget in frame2.winfo_children():
            widget.destroy()
        check_dolar2 = tkc.CTkRadioButton(frame2, text="Grafico Petrobras", text_color='white', font=('Ivy', 14), fg_color=('#1cacfc'), variable=var2, value=0, border_width_checked=4, border_width_unchecked=2, radiobutton_width=15, radiobutton_height=15, state=tkc.DISABLED)
        check_dolar2.pack(side=tkc.LEFT, padx=5)

        check_moedas2 = tkc.CTkRadioButton(frame2, text="Grafico Weg", text_color='white', font=('Ivy', 14), fg_color=('#1cacfc'), variable=var2, value=1, border_width_checked=4, border_width_unchecked=2, radiobutton_width=15, radiobutton_height=15, state=tkc.DISABLED)
        check_moedas2.pack(side=tkc.LEFT, padx=5)

        check_acoes2 = tkc.CTkRadioButton(frame2, text="Grafico Vale", text_color='white', font=('Ivy', 14), fg_color=('#1cacfc'), variable=var2, value=2, border_width_checked=4, border_width_unchecked=2, radiobutton_width=15, radiobutton_height=15, state=tkc.DISABLED)
        check_acoes2.pack(side=tkc.LEFT, padx=5)

#botao
btn_atualizar = tkc.CTkButton(app, text="Buscar cotação", text_color='white', font=('Ivy', 15, 'bold'), corner_radius=10, compound='top', fg_color=('#1cacfc'), command=lambda:[atualizar_cotacao(), habilitar_btn_sms()])
btn_atualizar.place(x=70,y=210)

btn_sms = tkc.CTkButton(app, text="Enviar SMS", text_color='white', font=('Ivy', 15, 'bold'), corner_radius=10, compound='top', fg_color=('#1cacfc'), command=lambda:[atualizar_cotacao(), enviar_mensagem(label_cotacao._text)], state=tkc.DISABLED, text_color_disabled='grey')
btn_sms.place(x=240,y=210)

#label pra imprimir
label_cotacao = tkc.CTkLabel(app, text="", text_color='white', font=('Ivy', 20), width=410, height=180, fg_color=('black', '#323232'), corner_radius=8)
label_cotacao.place(x=20,y=260)

print(label_cotacao._text)

verificar_botao()
app.mainloop()




