from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import RETRY, showinfo, askyesno
import requests, json
from requests.models import Response


#uma lista de dicionários 
URL_USUARIOS = "http://localhost:3000/usuarios"
usuarios = None
# r = requests.get(url=URL_CAES)
# caes = r.json()



def monta_tela_usuarios(notebook):

    def buscar():
        lista = busca_tk.get()
        limpar_tela()
        for usuario in usuarios:
            if lista.lower() in usuario['nome'].lower():           
                tree.insert('', END, values=(usuario["id"], usuario["nome"], usuario["email"]))
        
    #limpa a tela depois de uma consulta 
    def limpar():
        limpar_tela()
        adicionar_dados(tree)

    def limpar_tela():
        for i in tree.get_children():
            tree.delete(i)

    def atualizar_lista():
        global usuarios
        r = requests.get(url=URL_USUARIOS)
        usuarios = r.json()
    


    def atualizar_usuario():
        pass
      


    def deletar_usuario():
        global cao_id
        cao_id=item_selected(any)
        # print(cao_id)

        response = requests.delete(URL_USUARIOS + "/" + str(cao_id) ) #str(selected[0]   str(cao_id)
        print(response.text)
        print(response.status_code)
        if response.status_code == 200:
            showinfo(title='Usuario Excluido',
                message=f"{response.text}")
        else:
            showinfo(title='Erro...',
                message=f"Usuario não pode ser Excuido")
        limpar_tela()
        adicionar_dados(tree)




# root = Tk()
# root.title("Petshop")
# root.geometry("800x700")

    rootframe = ttk.Frame(notebook, width=800, height=700)

    frame1 = LabelFrame(rootframe, text="Lista de Usuários")
    frame2 = LabelFrame(rootframe, text="Busca")
    frame3 = LabelFrame(rootframe, text="Cadastro de Usuários")

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
    ttk.Label(cadframe, text="Email: ").grid(column=1, row=2, sticky=E)
    ttk.Label(cadframe, text="Senha: ").grid(column=1, row=3, sticky=E)


    #campo de entrada de dados
    nome = StringVar()
    nome_entry = ttk.Entry(cadframe, width=40, textvariable=nome)
    nome_entry.grid(column=2, row=1, sticky=(W))



    email = StringVar()
    #ttk.Entry(cadframe, width=10, textvariable=idade).grid(column=2, row=3, sticky=(W))
    email_entry = ttk.Entry(cadframe, width=40, textvariable=email)
    email_entry.grid(column=2, row=2, sticky=(W))

    senha = StringVar()
    #ttk.Entry(cadframe, width=60, textvariable=foto).grid(column=2, row=4, sticky=(W))
    senha_entry = ttk.Entry(cadframe, width=40, textvariable=senha)
    senha_entry.grid(column=2, row=3, sticky=(W))


    #Acrescenta um expassamento entre as linhas do form
    for child in cadframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    def incluir():
        dados = {
            "nome":nome.get(),
            "email": email.get(),
            "senha":senha.get(),
        }
        # pass
        response = requests.post(URL_USUARIOS, json=dados)
        print(response.text)
        print(response.status_code)
        
        if response.status_code == 201:
            showinfo(title='Usuario Cadastrado',
                message=f"Código do Usuário{response.text}")
        else:
            showinfo(title='Erro...',
                message=f"Usuário não cadastrado")
    
        limpar_tela()
        adicionar_dados(tree)
        atualizar_lista()
        


    #frame para os botões

    botoes_frame = ttk.Frame(cadframe)
    botoes_frame.grid(row=5, column=2, pady=12) # pady=12

    ttk.Button(botoes_frame, text="Incluir Usúario", command=incluir).grid(column=2, row=5, sticky=W,padx=10 )
    ttk.Button(botoes_frame, text="Editar Usuário", command=atualizar_usuario).grid(column=3, row=5, sticky=W)
    ttk.Button(botoes_frame, text="Excluir Usuário", command=deletar_usuario).grid(column=4, row=5,sticky=W, padx=10)

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
    columns = ('#1', '#2', '#3')

    tree = ttk.Treeview(frame1, columns=columns, show='headings')

    # define headings
    tree.heading('#1', text='ID')
    tree.heading('#2', text='Nome')
    tree.heading('#3', text='Email')


    tree.column("#1", width=10)
    tree.column("#2", width=170)
    tree.column("#3", width=100, anchor=CENTER)

    #total de espacamento = 490



    # adding data to the treeview

    def adicionar_dados(tree):
        atualizar_lista()
        for usuario in usuarios:
            
            tree.insert('', END, values=(usuario["id"], usuario["nome"], usuario["email"]))

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
            email.set(record[2])
            

            
            global usuario_id
            usuario_id = record[0]

            return usuario_id




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
        ttk.Radiobutton(orderframe, text='email', variable=order, value='email').grid(column=2, row=1, sticky=W)
        
        
        def ordenar():
            global user
            if order.get() == "id":
                user = sorted(usuarios, key=lambda x: x['id'], reverse=True) 
            elif order.get() == "nome":
                user = sorted(usuarios, key=lambda x: x['nome']) 
            elif order.get() == "email":  
                user = sorted(usuarios, key=lambda x: x['email']) 
                
            limpar_tela()
            for usuario in user:        
                tree.insert('', END, values=(usuario["id"], usuario["nome"], usuario["email"],))

        ttk.Button(orderframe, text="Ordenar", command=ordenar).grid(column=2, row=2, sticky=W)
    
    ordem()
    return rootframe