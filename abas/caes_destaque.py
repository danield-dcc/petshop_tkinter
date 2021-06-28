from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo, askyesno
import requests, json
from requests.models import Response


#uma lista de dicionários 
URL_CAES = "http://localhost:3000/caes"
caes = None
# r = requests.get(url=URL_CAES)
# caes = r.json()
# print(caes)

URL_RACA = "http://localhost:3000/raca"
r = requests.get(url=URL_RACA)
racas = r.json()
# print(racas)

def monta_formulario(notebook):

    def buscar():
        lista = busca_tk.get()
        limpar_tela()
        for cao in caes:
            if lista.lower() in cao['nome'].lower():          
                destaque = "*" if cao["destaque"] else ""
                tree.insert('', END, values=(cao["id"], cao["nome"], cao["raca"],cao["idade"],destaque, cao["foto"],))
            

    #limpa a tela depois de uma consulta 
    def limpar():
        limpar_tela()
        adicionar_dados(tree)


    # função para salvar raça do cachorro pela id
    raca_cachorro_id = 0

    def raca_selecionada(*args):
        global raca_cachorro_id
        current_value = racas_cb.get()
        for raca in racas:
            if raca["nome"] == current_value:
                raca_cachorro_id = raca["id"] 



    lista=[]
    #percorre a lista de dicionários de raça de cachorros
    for raca in racas:
        lista.append(raca['nome'])

    

    def atualizar_lista():
        global caes
        r = requests.get(url=URL_CAES)
        caes = r.json()
        


    def atualizar_pet():
        headers = {'Content-Type': "application/json", 'Accept': "application/json"}
        global cao_id
        cao_id=item_selected(any)
        dados2 = {
            "nome": nome.get(),
            "raca_cachorro_id": raca_cachorro_id,
            "idade":idade.get(),
            "foto":foto.get()
        }
        print(dados2)
        response = requests.put(URL_CAES +"/atualizar/"+str(cao_id),json=dados2, headers=headers)
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



    def deletar_pet():
        global cao_id
        cao_id=item_selected(any)

        response = requests.delete(URL_CAES + "/" + str(cao_id) ) #str(selected[0]   str(cao_id)
        print(response.text)
        print(response.status_code)
        if response.status_code == 200:
            showinfo(title='Pet Excluido',
                message=f"{response.text}")
        else:
            showinfo(title='Erro...',
                message=f"Pet não pode ser Excuido")
        limpar_tela()
        adicionar_dados(tree)




    # root = Tk()
    # root.title("Petshop")
    # root.geometry("800x700")
    # q = StringVar

    rootframe = ttk.Frame(notebook, width=800, height=700)

    frame1 = LabelFrame(rootframe, text="Lista de Pets")
    frame2 = LabelFrame(rootframe, text="Busca")
    frame3 = LabelFrame(rootframe, text="Cadastro de Pets")

    frame1.pack(fill="both", expand="yes", padx=20, pady=10)
    frame2.pack(fill="both", expand="yes", padx=20, pady=10)
    frame3.pack(fill="both", expand="yes", padx=20, pady=10)

    ##Cadastro FRAME 3
    cadframe = ttk.Frame(frame3, padding="3 3 12 12")
    cadframe.grid(column=0, row=0, sticky=( W, E))
    rootframe.columnconfigure(0, weight=1)
    rootframe.rowconfigure(0, weight=1)

    #labes do Formulário
    ttk.Label(cadframe, text="Nome: ").grid(column=1, row=1, sticky=E)
    ttk.Label(cadframe, text="Raça: ").grid(column=1, row=2, sticky=E)
    ttk.Label(cadframe, text="Idade: ").grid(column=1, row=3, sticky=E)
    ttk.Label(cadframe, text="URL da Foto: ").grid(column=1, row=4, sticky=E)

    #campo de entrada de dados
    nome = StringVar()
    nome_entry = ttk.Entry(cadframe, width=40, textvariable=nome)
    nome_entry.grid(column=2, row=1, sticky=(W))

    #utiliza o método Combobox para listar as raças de cães
    racas_cb = ttk.Combobox(cadframe)
    racas_cb["values"] = lista
    racas_cb.grid(column=2, row=2, sticky=W)
    racas_cb.bind('<<ComboboxSelected>>', raca_selecionada)

    idade = StringVar()
    #ttk.Entry(cadframe, width=10, textvariable=idade).grid(column=2, row=3, sticky=(W))
    idade_entry = ttk.Entry(cadframe, width=10, textvariable=idade)
    idade_entry.grid(column=2, row=3, sticky=(W))

    foto = StringVar()
    #ttk.Entry(cadframe, width=60, textvariable=foto).grid(column=2, row=4, sticky=(W))
    foto_entry = ttk.Entry(cadframe, width=60, textvariable=foto)
    foto_entry.grid(column=2, row=4, sticky=(W))


    #Acrescenta um expassamento entre as linhas do form
    for child in cadframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    def incluir():
        dados = {
            "nome":nome.get(),
            "raca_cachorro_id": raca_cachorro_id,
            "idade":idade.get(),
            "foto":foto.get()
        }
        # pass
        response = requests.post(URL_CAES, json=dados)
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
            

    def destacar_pet():
        cao_id
        selecionado = tree.focus()
        temp = tree.item(selecionado, 'values')

        if temp[4]:
            answer = askyesno(title='Confirmação',
                        message='Deseja Retirar do Destaque deste Pet?')
            if answer:
                requests.put(url=URL_CAES+"/destacar/"+str(temp[0]))
                tree.item(selecionado, values=(temp[0], temp[1], temp[2], temp[3],"", temp[5]))        
                limpar()
        else:
            answer = askyesno(title='Confirmação',
                        message='Deseja Destacar Este Pet?')
            if answer:
                requests.put(url=URL_CAES+"/destacar/"+str(temp[0]))
                tree.item(selecionado, values=(temp[0], temp[1], temp[2], temp[3],"*", temp[5]))
                limpar()

    #frame para os botões

    botoes_frame = ttk.Frame(cadframe)
    botoes_frame.grid(row=5, column=2, pady=12) # pady=12

    ttk.Button(botoes_frame, text="Incluir Pet", command=incluir).grid(column=2, row=5, sticky=W,padx=10 )
    ttk.Button(botoes_frame, text="Editar Pet", command=atualizar_pet).grid(column=3, row=5, sticky=W)
    ttk.Button(botoes_frame, text="Excluir Pet", command=deletar_pet).grid(column=4, row=5,sticky=W, padx=10)
    ttk.Button(botoes_frame, text="Destacar Pet", command=destacar_pet).grid(column=5, row=5,sticky=W, padx=10)
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
    columns = ('#1', '#2', '#3', '#4', '#5', '#6')

    tree = ttk.Treeview(frame1, columns=columns, show='headings')

    # define headings
    tree.heading('#1', text='ID')
    tree.heading('#2', text='Nome')
    tree.heading('#3', text='Raça')
    tree.heading('#4', text='Idade')
    tree.heading('#5', text='Destaque')
    tree.heading('#6', text='Foto')

    tree.column("#1", width=10)
    tree.column("#2", width=170)
    tree.column("#3", width=100, anchor=CENTER)
    tree.column("#4", width=60, anchor=CENTER)
    tree.column("#5", width=20, anchor=CENTER)
    tree.column("#6", width=130,anchor=W)
    #total de espacamento = 490

    def limpar_tela():
        for i in tree.get_children():
            tree.delete(i)


    def adicionar_dados(tree):
        atualizar_lista()
        for cao in caes:
            destaque = "*" if cao["destaque"] else ""
            tree.insert('', END, values=(cao["id"], cao["nome"], cao["raca"],cao["idade"],destaque, cao["foto"],))

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
            #destaque == record[4]
            nome.set(record[1])
            racas_cb.set(record[2])
            idade.set(record[3])
            foto.set(record[5])

            
            global cao_id
            cao_id = record[0]

            return cao_id




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
        ttk.Radiobutton(orderframe, text='Idade', variable=order, value='idade').grid(column=2, row=1, sticky=W)
        ttk.Radiobutton(orderframe, text='Destaque', variable=order, value='destaque').grid(column=3, row=1, sticky=W)
        
        def ordenar():
            global caes2
            if order.get() == "id":
                caes2 = sorted(caes, key=lambda x: x['id'], reverse=True) 
            elif order.get() == "nome":
                caes2 = sorted(caes, key=lambda x: x['nome']) 
            elif order.get() == "idade":  
                caes2 = sorted(caes, key=lambda x: x['idade']) 
            elif order.get() == "destaque":  
                caes2 = sorted(caes, key=lambda x: x['destaque'], reverse=True) 

            
            limpar_tela()
            for cao in caes2:        
                destaque = "*" if cao["destaque"] else ""
                tree.insert('', END, values=(cao["id"], cao["nome"], cao["raca"],cao["idade"],destaque, cao["foto"],))

        ttk.Button(orderframe, text="Ordenar", command=ordenar).grid(column=3, row=2, sticky=W)
    
    ordem()

    return rootframe
