from tkinter import *
from tkinter import ttk
from abas import caes_destaque, clientes, usuarios, banho_tosa, agrupados, estatistica

def abre_inclusao_pet():
  remove_frames()
  frame = caes_destaque.monta_formulario(root)
  frame.grid(row=1, column=1, sticky=W)

def abre_inclusao_cliente():
  remove_frames()
  frame = clientes.monta_tela_clientes(root)
  frame.grid(row=1, column=1, sticky=W)

def abre_inclusao_usuario():
  remove_frames()
  frame = usuarios.monta_tela_usuarios(root)
  frame.grid(row=1, column=1, sticky=W)

def abre_inclusao_banho_tosa():
  remove_frames()
  frame = banho_tosa.monta_tela_banho_tosa(root)
  frame.grid(row=1, column=1, sticky=W)

def abre_resumo():
  remove_frames()
  frame = agrupados.monta_tela_agrupados(root)
  frame.grid(row=1, column=1, sticky=W)

def abre_estatistica():
  remove_frames()
  frame = estatistica.monta_tela_estatisticas(root)
  frame.grid(row=1, column=1, sticky=W)

def remove_frames():
  for child in root.winfo_children(): 
    if str(child) != '.!menu':
      child.destroy()

root = Tk()
root.geometry('800x700+60+60')
root.title('Petshop - Controle de Entrada')

# icon = PhotoImage(file = 'fotos/herbie.png') 
# root.iconphoto(False, icon)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Inclusão Pet", command=abre_inclusao_pet)
filemenu.add_command(label="Clientes", command=abre_inclusao_cliente)
filemenu.add_command(label="Usuarios", command=abre_inclusao_usuario)
filemenu.add_command(label="Banho/Tosa", command=abre_inclusao_banho_tosa)
filemenu.add_command(label="Resumo", command=abre_resumo)
filemenu.add_command(label="Estatística", command=abre_estatistica)
filemenu.add_separator()
filemenu.add_command(label="Sair", command=root.quit)
menubar.add_cascade(label="Cadastros", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Localizar")
helpmenu.add_command(label="Sobre...")
menubar.add_cascade(label="Ajuda", menu=helpmenu)

root.config(menu=menubar)
root.mainloop()