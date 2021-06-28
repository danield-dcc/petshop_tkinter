from tkinter import *
from tkinter import ttk
import requests
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 



#uma lista de dicionários 
URL_CAES_EST = "http://localhost:3000/caes/dados"
caes = None
r = requests.get(url=URL_CAES_EST)
caes = r.json()

def monta_tela_estatisticas(notebook):

    rootframe = ttk.Frame(notebook, width=800, height=700)
    frame1 = LabelFrame(rootframe, text="Dados Estatisticos")
    frame1.pack(fill="both", expand="yes", padx=20, pady=10)

    # Labels para exibir dados
    ttk.Label(frame1, text=f"Número de Pets Cadastrados: { caes['total']}").grid(column=1, row=1, sticky=W)
    ttk.Label(frame1, text=f"Idade do Pet Mais Novo: {caes['menorIdade']}").grid(column=1, row=2, sticky=W)
    ttk.Label(frame1, text=f"Idade do Pet mais velho: {caes['maiorIdade']}").grid(column=1, row=3, sticky=W)
    ttk.Label(frame1, text=f"Quantidade de Pets em destaque: {caes['qtdDestaques']}").grid(column=1, row=4, sticky=W)
    ttk.Label(frame1, text=f"Média da idade dos Pets: {caes['mediaIdade']}").grid(column=1, row=5, sticky=W)
    ttk.Label(frame1, text=f"Qantidade de agendamentos R$: {caes['totalAgendamentos']}").grid(column=1, row=6, sticky=W)
    ttk.Label(frame1, text=f"Soma do retorno dos agendamentos R$: {caes['valorTotal']}").grid(column=1, row=7, sticky=W)

    return rootframe