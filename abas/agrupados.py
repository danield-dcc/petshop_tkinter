from tkinter import *
from tkinter import ttk
import requests

#uma lista de dicionários 
URL_CAES = "http://localhost:3000/caes"
caes = None
r = requests.get(url=URL_CAES)
caes = r.json()



URL_CLIENTES = "http://localhost:3000/clientes"
clientes = None
r = requests.get(url=URL_CLIENTES)
clientes = r.json()
# print(clientes)

pets = {}
racas = {}

def monta_tela_agrupados(notebook):
    

    def agrupa_pets():
        global pets, racas
        racas = {}
        r = requests.get(url=URL_CAES)
        caes = r.json()
        for cao in caes:
            if cao['raca'] in racas:
                racas[cao["raca"]] += 1
            else:
                racas[cao["raca"]] = 1

    def adicionar_dados(tree):
        agrupa_pets()
        for raca, num in racas.items():
            tree.insert('', END, values=(raca, num))

    rootframe = ttk.Frame(notebook, width=800, height=700)
    frame1 = LabelFrame(rootframe, text="Lista de Agrupados")
    frame1.pack(fill="both", expand="yes", padx=20, pady=10)

    columns = ("#1", "#2")

    tree = ttk.Treeview(frame1, columns=columns, show='headings')

    # define headings
    tree.heading('#1', text='Raças de Pets')
    tree.heading('#2', text='Qtd Cadastrada')

    #largura
    tree.column("#1", width=150)
    tree.column("#2", width=100, anchor=CENTER)

    adicionar_dados(tree)

    # bind the select event
    def item_selected(event):
        selected = tree.focus()
        temp = tree.item(selected, 'values')

    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=1, column=0, sticky='nsew', padx=(10, 0), pady=10)

    # add a scrollbar
    scrollbar = ttk.Scrollbar(frame1, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky='ns')

    return rootframe
    
