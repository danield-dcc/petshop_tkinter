from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo
import requests

#uma lista de dicionários 
URL_CAES = "http://localhost:3000/caes"
r = requests.get(url=URL_CAES)
caes = r.json()
#print(caes)

URL_CLIENTES = "http://localhost:3000/clientes"
clientes = None
# r = requests.get(url=URL_CLIENTES)
# clientes = r.json()
#print(clientes)

def monta_tela_clientes(notebook):

    def atualizar_lista():
        global clientes
        r = requests.get(url=URL_CLIENTES)
        clientes = r.json()


    def buscar():
        lista = busca_tk.get()

        limpar_tela()

        for cliente in clientes:
            if lista.lower() in cliente['nome'].lower() :          
                tree.insert('', END, values=(cliente["id"],cliente["nome"], cliente["nome_do_cachorro"],cliente["endereco"],cliente["cpf"],cliente["telefone"]))


    lista=[]
    #percorre a lista de dicionários para o Combobox
    for cao in caes:
        lista.append(cao['nome'])

    def limpar_tela():
        for i in tree.get_children():
            tree.delete(i)


    #limpa a tela depois de uma consulta 
    def limpar():
        limpar_tela()
        adicionar_dados(tree)

    #Função para salvar nome do cachorro pelo id
    nome_do_cachorro=0
    def pet_selecionada(*args):
        global nome_do_cachorro

        current_value = caes_cb.get()
        for cao in caes:
            if cao["nome"] == current_value:
                nome_do_cachorro = cao["id"] 

    def atualizar_cliente():
        global cliente_id
        cliente_id=item_selected(any)
        dados2 = {
            "nome":nome.get(),
            "caes_cadastrados_id": nome_do_cachorro,
            "endereco":endereco.get(),
            "cpf":cpf.get(),
            "telefone":telefone.get(),
        }
        print(cliente_id)
        print(dados2)
        response = requests.put(URL_CLIENTES +"/atualizar/"+str(cliente_id), json=dados2)
        print(response.text)
        print(response.status_code)
    
        if response.status_code == 200:
            showinfo(title='Cliente Atualizado',
                message=f"Código do Pet{response.text}")
        else:
            showinfo(title='Erro...',
                message=f"Cliente não pode ser atualizado")
        limpar_tela()
        adicionar_dados(tree)



    def deletar_cliente():
        global cliente_id
        cliente_id=item_selected(any)


        response = requests.delete(URL_CLIENTES + "/" + str(cliente_id) ) #str(selected[0]   str(cliente_id)
        print(response.text)
        print(response.status_code)
        if response.status_code == 200:
            showinfo(title='Cliente Excluido',
                message=f"{response.text}")
        else:
            showinfo(title='Erro...',
                message=f"Cliente não pode ser Excuido")
        limpar_tela()
        adicionar_dados(tree)
        limpar()



    # root = Tk()
    # root.title("Petshop")
    # root.geometry("800x700")
    rootframe = ttk.Frame(notebook, width=800, height=700)


    frame1 = LabelFrame(rootframe, text="Lista de Clientes")
    frame2 = LabelFrame(rootframe, text="Busca")
    frame3 = LabelFrame(rootframe, text="Cadastro de Clientes")

    frame1.pack(fill="both", expand="yes", padx=20, pady=10)
    frame2.pack(fill="both", expand="yes", padx=20, pady=10)
    frame3.pack(fill="both", expand="yes", padx=20, pady=10)

    ##Cadastro FRAME 3
    cadframe = ttk.Frame(frame3, padding="3 3 12 12")
    cadframe.grid(column=0, row=0, sticky=(W, E))
    rootframe.columnconfigure(0, weight=1)
    rootframe.rowconfigure(0, weight=1)

    #labes do Formulário
    ttk.Label(cadframe, text="Nome: ").grid(column=1, row=1, sticky=E)
    ttk.Label(cadframe, text="Pet: ").grid(column=1, row=2, sticky=E)
    ttk.Label(cadframe, text="Endereço: ").grid(column=1, row=3, sticky=E)
    ttk.Label(cadframe, text="CPF: ").grid(column=1, row=4, sticky=E)
    ttk.Label(cadframe, text="Telefone: ").grid(column=1, row=5, sticky=E)

    #campo de entrada de dados
    nome = StringVar()
    nome_entry = ttk.Entry(cadframe, width=40, textvariable=nome)
    nome_entry.grid(column=2, row=1, sticky=W)

    #utiliza o método Combobox para listar os cães
    caes_cb = ttk.Combobox(cadframe)
    caes_cb["values"] = lista
    caes_cb.grid(column=2, row=2, sticky=W)
    caes_cb.bind('<<ComboboxSelected>>', pet_selecionada)

    endereco = StringVar()
    ttk.Entry(cadframe, width=60, textvariable=endereco).grid(column=2, row=3, sticky=(W))

    cpf = StringVar()
    ttk.Entry(cadframe, width=15, textvariable=cpf).grid(column=2, row=4, sticky=(W))

    telefone = StringVar()
    ttk.Entry(cadframe, width=20, textvariable=telefone).grid(column=2, row=5, sticky=(W))

    #Acrescenta um expassamento entre as linhas do form
    for child in cadframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    def incluir():
        dados = {
            "nome":nome.get(),
            "caes_cadastrados_id": nome_do_cachorro,
            "endereco":endereco.get(),
            "cpf":cpf.get(),
            "telefone":telefone.get(),
        }

        response = requests.post(URL_CLIENTES, json=dados)
        print(response.text)
        print(response.status_code)
    
        if response.status_code == 201:
            showinfo(title='Cliente Cadastrado',
                message=f"Código do Cliente{response.text}")
        else:
            showinfo(title='Erro...',
                message=f"Cliente não cadastrado")
        limpar()
        
    
    #frame para os botões
    botoes_frame = ttk.Frame(cadframe)
    botoes_frame.grid(row=6, column=2, pady=12) # pady=12

    ttk.Button(botoes_frame, text="Incluir Cliente", command=incluir).grid(column=2, row=5, sticky=W,padx=10 )
    ttk.Button(botoes_frame, text="Editar Cliente", command=atualizar_cliente).grid(column=3, row=5, sticky=W)
    ttk.Button(botoes_frame, text="Excluir Cliente", command=deletar_cliente).grid(column=4, row=5,sticky=W, padx=10)

#----------------------------
## BUSCA FRAME 2
    

    #label de busca
    ttk.Label(frame2, text="Dados de Busca: ").grid(column=1, row=1, sticky=W)


    #entrada de dados
    busca_tk = StringVar()
    busca_tk_entry = ttk.Entry(frame2, width=40, textvariable=busca_tk)
    busca_tk_entry.grid(column=2, row=1, sticky=(W))


    ttk.Button(frame2, text="Busca", command=buscar).grid(column=2, row=2, sticky=W,padx=10, pady=6 )
    ttk.Button(frame2, text="Limpar Tela", command=limpar).grid(column=2, row=2, sticky=W,padx=100, pady=6 )


#=====================================
    ##LISTAGEM FRAME 1
    # columns
    atualizar_lista()
    columns = ('#1', '#2', '#3', '#4', '#5', '#6')

    tree = ttk.Treeview(frame1, columns=columns, show='headings')

    # define headings
    tree.heading('#1', text='ID')
    tree.heading('#2', text='Nome')
    tree.heading('#3', text='Pet')
    tree.heading('#4', text='Endereço')
    tree.heading('#5', text='CPF')
    tree.heading('#6', text='Telefone')

    tree.column("#1", width=15)
    tree.column("#2", width=110)
    tree.column("#3", width=70, anchor=CENTER)
    tree.column("#4", width=170, anchor=W)
    tree.column("#5", width=70,anchor=W)
    tree.column("#6", width=60,anchor=W)
    # total de espacamento = 490


    # adding data to the treeview

    def adicionar_dados(tree):
        atualizar_lista()
        for cliente in clientes:
            tree.insert('', END, values=(cliente["id"],cliente["nome"], cliente["nome_do_cachorro"],cliente["endereco"],cliente["cpf"],cliente["telefone"]))
    adicionar_dados(tree)


    # bind the select event
    def item_selected(event):
        for selected_item in tree.selection():
            # dictionary
            item = tree.item(selected_item)
            # list
            record = item['values']
            #
            # showinfo(title='Information',
            #         message=','.join(record))
            nome.set(record[1])
            caes_cb.set(record[2])
            endereco.set(record[3])
            cpf.set(record[4])
            telefone.set(record[5])

            global cliente_id
            cliente_id = record[0]

            return cliente_id


    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=1, column=0, sticky='nsew', padx=(20,0), ipadx=100) #ipax para a largura da treeview

    # add a scrollbar
    scrollbar = ttk.Scrollbar(frame1, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky='ns')


    ##ORDENAÇÕES
    orderframe = ttk.Frame(frame2)
    orderframe.grid(row=1, column=3)

    def ordem():
        ttk.Label(orderframe, text="Ordenar dados:").grid(column=0, columnspan=3, row=0, sticky=W)

        order = StringVar()
        order.set("id")
        ttk.Radiobutton(orderframe, text='ID', variable=order, value='id').grid(column=0, row=1, sticky=W)
        ttk.Radiobutton(orderframe, text='Nome', variable=order, value='nome').grid(column=1, row=1, sticky=W)
        ttk.Radiobutton(orderframe, text='Pet', variable=order, value='Pe').grid(column=2, row=1, sticky=W)
    
    
        def ordenar():
            global clientes2
            if order.get() == "id":
                clientes2 = sorted(clientes, key=lambda x: x['id'], reverse=True) 
            elif order.get() == "nome":
                clientes2 = sorted(clientes, key=lambda x: x['nome']) 
            elif order.get() == "idade":  
                clientes2 = sorted(clientes, key=lambda x: x['idade']) 

        
            limpar_tela()
            for cliente in clientes2:                  
                tree.insert('', END, values=(cliente["id"],cliente["nome"], cliente["nome_do_cachorro"],cliente["endereco"],cliente["cpf"],cliente["telefone"]))

        ttk.Button(orderframe, text="Ordenar", command=ordenar).grid(column=3, row=2, sticky=W)
   
    ordem()
    return rootframe


#root.mainloop()