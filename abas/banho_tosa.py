from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo, askyesno
import requests
from requests.models import Response


#uma lista de dicionários 
URL_BANHO_TOSA = "http://localhost:3000/banho_tosa"
banho_tosa = None
# r = requests.get(url=URL_CAES)
# caes = r.json()
# print(caes)

#uma lista de dicionários 
URL_CAES = "http://localhost:3000/caes"
caes = None
r = requests.get(url=URL_CAES)
caes = r.json()
print(caes)


URL_CLIENTES = "http://localhost:3000/clientes"
clientes = None
r = requests.get(url=URL_CLIENTES)
clientes = r.json()
# print(clientes)


def monta_tela_banho_tosa(notebook):

    def buscar():
        lista = busca_tk.get()
        limpar_tela()
        for bt in banho_tosa:
            if lista.lower() in bt['nome'].lower():          
                tree.insert('', END, values=(bt["id"], bt["dia"], bt["hora"],bt["preco"],bt["cliente"], bt["nome_do_cachorro"], bt["raca"],))
            

    #limpa a tela depois de uma consulta 
    def limpar():
        limpar_tela()
        adicionar_dados(tree)


    # função para salvar pet pela id
    pet_nome_id = 0
    def pet_selecionada(*args):
        global pet_nome_id
        current_value = caes_cb.get()
        for cao in caes:
            if cao["nome"] == current_value:
                pet_nome_id = cao["id"] 

    nome_do_cliente = 0
    def cliente_selecionado(*args):
        global nome_do_cliente
        current_value = clientes_cb.get()
        for cliente in clientes:
            if cliente["nome"] == current_value:
                nome_do_cliente = cliente["id"]  


    lista_pet=[]
    #percorre a lista de dicionários de pets
    for cao in caes:
        lista_pet.append(cao['nome'])

    lista_clientes=[]
    #percorre a lista de dicionários de pets
    for cliente in clientes:
        lista_clientes.append(cliente['nome'])



    def limpar_tela():
        for i in tree.get_children():
            tree.delete(i)

    def atualizar_lista():
        global banho_tosa
        r = requests.get(url=URL_BANHO_TOSA)
        banho_tosa = r.json()
    


    def atualizar_bt():
        global cao_id
        cao_id=item_selected(any)
        dados2 = {
            "dia":dia.get(),
            "hora": hora.get(),
            "preco": servico.get(),
            "cliente_id":nome_do_cliente,
            "caes_cadastrados_id":pet_nome_id
        }
        print(dados2)
        response = requests.put(URL_CAES +"/"+str(cao_id),json=dados2)
        print(response.text)
        print(response.status_code)
        
        if response.status_code == 200:
            showinfo(title='Pet Atualizado',
                message=f"Código do Pet{response.text}")
        else:
            showinfo(title='Erro...',
                message=f"Pet não pode ser atualizado")
        limpar_tela()
        adicionar_dados(tree)
        limpar()



    def deletar_bt():
        global bt_id
        bt_id=item_selected(any)
        print(bt_id)

        response = requests.delete(URL_BANHO_TOSA + "/" + str(bt_id) )
        print(response.text)
        print(response.status_code)
        if response.status_code == 200:
            showinfo(title='Procedimento Excluido',
                message=f"{response.text}")
        else:
            showinfo(title='Erro...',
                message=f"Procedimento não pode ser Excuido")
        limpar_tela()
        adicionar_dados(tree)

    def incluir_bt():
        dados = {
            "dia":dia.get(),
            "hora": hora.get(),
            "preco": servico.get(),
            "cliente_id":nome_do_cliente,
            "caes_cadastrados_id":pet_nome_id
        }
        # pass
        print(dados)
        response = requests.post(URL_BANHO_TOSA, json=dados)
        print(response.text)
        print(response.status_code)
    
        if response.status_code == 201:
            showinfo(title='Pet Cadastrado',
                message=f"Código do Pet{response.text}")
        else:
            showinfo(title='Erro...',
                message=f"Pet não cadastrado")

        
        limpar_tela()
        adicionar_dados(tree)
        atualizar_lista()



# root = Tk()
# root.title("Petshop")
# root.geometry("800x700")

    rootframe = ttk.Frame(notebook, width=800, height=700)

    frame1 = LabelFrame(rootframe, text="Lista de Banho e Tosa")
    frame2 = LabelFrame(rootframe, text="Busca")
    frame3 = LabelFrame(rootframe, text="Cadastro de Banho e Tosa")

    frame1.pack(fill="both", expand="yes", padx=20, pady=10)
    frame2.pack(fill="both", expand="yes", padx=20, pady=10)
    frame3.pack(fill="both", expand="yes", padx=20, pady=10)

    ##Cadastro FRAME 3
    cadframe = ttk.Frame(frame3, padding="3 3 12 12")
    cadframe.grid(column=0, row=0, sticky=( W, E))
    rootframe.columnconfigure(0, weight=1)
    rootframe.rowconfigure(0, weight=1)

    #labes do Formulário
    ttk.Label(cadframe, text="Dia: ").grid(column=1, row=1, sticky=E)
    ttk.Label(cadframe, text="Hora: ").grid(column=1, row=2, sticky=E)
    ttk.Label(cadframe, text="Cliente: ").grid(column=1, row=3, sticky=E)
    ttk.Label(cadframe, text="Pet: ").grid(column=1, row=4, sticky=E)
    ttk.Label(cadframe, text="Banho e Tosa: ").grid(column=1, row=5, sticky=E)

    #campo de entrada de dados
    dia = StringVar()
    dia_entry = ttk.Entry(cadframe, width=20, textvariable=dia)
    dia_entry.grid(column=2, row=1, sticky=(W))

    hora = StringVar()
    hora_entry = ttk.Entry(cadframe, width=20, textvariable=hora)
    hora_entry.grid(column=2, row=2, sticky=(W))



    #utiliza o método Combobox para listar todos os clientes
    clientes_cb = ttk.Combobox(cadframe)
    clientes_cb["values"] = lista_clientes
    clientes_cb.grid(column=2, row=3, sticky=W)
    clientes_cb.bind('<<ComboboxSelected>>', cliente_selecionado)

    #utiliza o método Combobox para listar todos os cães
    caes_cb = ttk.Combobox(cadframe)
    caes_cb["values"] = lista_pet
    caes_cb.grid(column=2, row=4, sticky=W, padx=6)
    caes_cb.bind('<<ComboboxSelected>>', pet_selecionada)

    #frame para os radiobutton
    combobox_frame = ttk.Frame(cadframe)
    combobox_frame.grid(row=5, column=2, pady=12)

    #ESPAÇO PARA COLOCAR AS RADIONBOTTUNS
    servico = StringVar()
    servico.set("id")
    ttk.Radiobutton(combobox_frame, text='Banho', variable=servico, value=50).grid(column=1, row=1, sticky=W)
    ttk.Radiobutton(combobox_frame, text='Banho e tosa', variable=servico, value=80).grid(column=2, row=1, sticky=W)




    #Acrescenta um expassamento entre as linhas do form
    for child in cadframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)



    #frame para os botões

    botoes_frame = ttk.Frame(cadframe)
    botoes_frame.grid(row=6, column=2, pady=12) # pady=12

    ttk.Button(botoes_frame, text="Incluir Pet", command=incluir_bt).grid(column=2, row=5, sticky=W,padx=10 )
    ttk.Button(botoes_frame, text="Editar Pet", command=atualizar_bt).grid(column=3, row=5, sticky=W)
    ttk.Button(botoes_frame, text="Excluir Pet", command=deletar_bt).grid(column=4, row=5,sticky=W, padx=10)

#----------------------------------------
## BUSCA FRAME 2

    #label de busca
    ttk.Label(frame2, text="Dados de Busca: ").grid(column=1, row=1, sticky=W)

    #entrada de dados
    busca_tk = StringVar()
    busca_tk_entry = ttk.Entry(frame2, width=40, textvariable=busca_tk)
    busca_tk_entry.grid(column=2, row=1, sticky=(W))

    ttk.Button(frame2, text="Busca", command=buscar).grid(column=2, row=2, sticky=W,padx=10, pady=6 )
    ttk.Button(frame2, text="Limpar Tela", command=limpar).grid(column=2, row=2, sticky=W,padx=100, pady=6 )


    ##LISTAGEM FRAME 1-----------------------------------
    # columns
    atualizar_lista()
    columns = ('#1', '#2', '#3', '#4', '#5', '#6', "#7")

    tree = ttk.Treeview(frame1, columns=columns, show='headings')

    # define headings
    tree.heading('#1', text='ID')
    tree.heading('#2', text='Data')
    tree.heading('#3', text='Hora')
    tree.heading('#4', text='Preço')
    tree.heading('#5', text='Cliente')
    tree.heading('#6', text='Pet')
    tree.heading('#7', text='Raça')

    tree.column("#1", width=10)
    tree.column("#2", width=40)
    tree.column("#3", width=40, anchor=CENTER)
    tree.column("#4", width=60, anchor=CENTER)
    tree.column("#5", width=120, anchor=CENTER)
    tree.column("#6", width=120,anchor=W)
    tree.column("#7", width=80,anchor=W)
    #total de espacamento = 490



    def adicionar_dados(tree):
        atualizar_lista()
        for bt in banho_tosa:
            tree.insert('', END, values=(bt["id"], bt["dia"], bt["hora"],bt["preco"],bt["cliente"], bt["nome_do_cachorro"], bt["raca"],))

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
            #ID == record[0]
            
            dia.set(record[1])
            hora.set(record[2])
            #preco.set(record[3])
            clientes_cb.set(record[4])
            caes_cb.set(record[5])

            
            global bt_id
            bt_id = record[0]

            return bt_id


    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=1, column=0, sticky='nsew', padx=(20,0), ipadx=100) #

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
        ttk.Radiobutton(orderframe, text='Dia', variable=order, value='dia').grid(column=1, row=1, sticky=W)
        ttk.Radiobutton(orderframe, text='Hora', variable=order, value='hora').grid(column=2, row=1, sticky=W)
        ttk.Radiobutton(orderframe, text='Preço', variable=order, value='preco').grid(column=3, row=1, sticky=W)
        ttk.Radiobutton(orderframe, text='Cliente', variable=order, value='cliente').grid(column=4, row=1, sticky=W)
        ttk.Radiobutton(orderframe, text='Pet', variable=order, value='nome_do_cachorro').grid(column=5, row=1, sticky=W)
        
        def ordenar():
            global banho_tosa2
            if order.get() == "id":
                banho_tosa2 = sorted(banho_tosa, key=lambda x: x['id'], reverse=True) 
            elif order.get() == "dia":
                banho_tosa2 = sorted(banho_tosa, key=lambda x: x['dia']) 
            elif order.get() == "hora":  
                banho_tosa2 = sorted(banho_tosa, key=lambda x: x['hora']) 
            elif order.get() == "preco":  
                banho_tosa2 = sorted(banho_tosa, key=lambda x: x['preco'], reverse=True) 
            elif order.get() == "cliente":  
                banho_tosa2 = sorted(banho_tosa, key=lambda x: x['cliente']) 
            elif order.get() == "nome_do_cachorro":  
                banho_tosa2 = sorted(banho_tosa, key=lambda x: x['nome_do_cachorro'], reverse=True)     

        
            limpar_tela()
            for bt in banho_tosa2:
                tree.insert('', END, values=(bt["id"], bt["dia"], bt["hora"],bt["preco"], bt["cliente"], bt["nome_do_cachorro"], bt["raca"],))

        ttk.Button(orderframe, text="Ordenar", command=ordenar).grid(column=3, row=2, sticky=W)
   
    ordem()
    return rootframe