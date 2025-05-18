import pandas as pd
from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk
from tkinter import tix



clientes = pd.read_excel(r'C:\Users\julio\Documents\Pasta GIT\Biblioteca\Clientes_cadastrados.xlsx')




class funcs_internas():
    
    def Limpar_tela(self):
        if self.Lista is not None:
            # Verifica se Lista é um widget e tem o método 'get_children'
            for item in self.Lista.get_children():
                self.Lista.delete(item)
        
        self.população()
        self.id_livro_entry.delete(0, END)
        self.nome_livro_entry.delete(0, END)
        self.retirada_entry.delete(0, END)
        self.Genero_entry.delete(0, END)

    def pop_cli(self):
        for i, row in clientes.iterrows():
            self.lista.insert("", "end", text=i, values=(row['Nome '], row['CPF'], row['Telefone'], row['Idade']))
            
    def Clique_duplo(self,event):  
        self.id_livro_entry.delete(0,END)
        self.nome_entry.delete(0,END)
        self.Autor_entry.delete(0,END)
        self.Genero_entry.delete(0,END)
        
        for n in self.lista.selection():
            id_livro = self.lista.item(n, 'text')
            col1,col2,col3,col4=self.lista.item(n,'values')
            self.id_livro_entry.insert(END,id_livro)
            self.nome_livro_entry.insert(END,col1)
            self.dt_retirada_entry.insert(END,col2)
            self.CPF_entry.insert(END,col3)
         
  
 

class Aluguel(funcs_internas):
        
    def __init__(self, root):
        self.root = root
        self.tela_loca()  # Cria a nova janela (Toplevel)
        self.subtelas()  # Cria as subtelas
        self.descricao_texto()
        self.Caixa_texto()
        self.botao()
        self.Lista()
        self.pop_cli()
        self.descricao_texto()  # Depois, adiciona os textos e widgets nas subtelas
   
    def tela_loca(self):
        # Cria uma nova janela (Toplevel) filha de self.root
        self.nova_janela = Toplevel(self.root)
        self.nova_janela.configure(background="#000000")  # Fundo preto
        self.nova_janela.geometry("600x400")
        self.nova_janela.resizable(True, True)
        self.nova_janela.maxsize(width=1020, height=800)
        self.nova_janela.minsize(width=800, height=500)  
    
    def subtelas(self):
        # Título
        self.label_titulo = Label(self.nova_janela, text="Locação de livros", bg="#dfe3ee", font=("Arial", 14, "bold"))
        self.label_titulo.place(relx=0.02, rely=0.01, relwidth=0.96, relheight=0.05)

        # Primeira Subtela
        self.subtela_loca_1 = Frame(self.nova_janela, bd=4, bg="#dfe3ee", highlightbackground="#759fe6", highlightthickness=2)
        self.subtela_loca_1.place(relx=0.02, rely=0.07, relwidth=0.96, relheight=0.36)

        # Segunda Subtela
        self.subtela_2 = Frame(self.nova_janela, bd=4, bg="#dfe3ee", highlightbackground="#759fe6", highlightthickness=2)
        self.subtela_2.place(relx=0.02, rely=0.443, relwidth=0.96, relheight=0.54)
    
    def descricao_texto(self):
        # Adiciona os campos de texto e widgets nas subtelas
        self.lb_codigo = Label(self.subtela_loca_1, text="ID Livro", bg="#dfe3ee")
        self.lb_codigo.place(relx=0.001, rely=0.01, relheight=0.09, relwidth=0.09)

        self.lb_nome_livro = Label(self.subtela_loca_1, text="Nome do Livro", bg="#dfe3ee")
        self.lb_nome_livro.place(relx=0.001, rely=0.30, relheight=0.1, relwidth=0.12)
        
        self.lb_retirada = Label(self.subtela_loca_1, text="Data de Retirada", bg="#dfe3ee")
        self.lb_retirada.place(relx=0.33, rely=0.30, relheight=0.1, relwidth=0.12)
        
        self.lb_devolucao = Label(self.subtela_loca_1, text="Data de Devolucao", bg="#dfe3ee")
        self.lb_devolucao.place(relx=0.66, rely=0.30, relheight=0.1, relwidth=0.14)
        
        self.lb_Locador =Label(self.subtela_loca_1,text="Locador",bg="#dfe3ee")
        self.lb_Locador.place(relx=0.001,rely=0.55,relheight=0.15,relwidth=0.07)
        
        self.lb_Locador_Cpf =Label(self.subtela_loca_1,text="CPF",bg="#dfe3ee")
        self.lb_Locador_Cpf.place(relx=0.33,rely=0.55,relheight=0.15,relwidth=0.05) 
        
        self.data_retirada = Label(self.subtela_loca_1,text="Loca")
            
    def Caixa_texto(self):
        self.id_livro_entry= Entry(self.subtela_loca_1)#"ID Livro"
        self.id_livro_entry.place(relx=0.001,rely=0.1, relheight=0.15,relwidth=0.13)
        
        self.nome_livro_entry=Entry(self.subtela_loca_1)#"Nome do Livro"
        self.nome_livro_entry.place(relx=0.001, rely=0.40, relheight=0.15,relwidth=0.3)
              
        self.dt_retirada_entry=Entry(self.subtela_loca_1)#"Data de Retirada"
        self.dt_retirada_entry.place(relx=0.33, rely=0.40, relheight=0.15,relwidth=0.3)
        
        self.dt_devolucao_entry=Entry(self.subtela_loca_1)#"Data de Devolucao"
        self.dt_devolucao_entry.place(relx=0.66, rely=0.40, relheight=0.15,relwidth=0.2)
                        
        self.Locador_entry=Entry(self.subtela_loca_1)#"Locador"
        self.Locador_entry.place(relx=0.001,rely=0.70,relheight=0.15,relwidth=0.3)    
        
        self.CPF_entry=Entry(self.subtela_loca_1)#"CPF"
        self.CPF_entry.place(relx=0.33,rely=0.70,relheight=0.15,relwidth=0.3)  
    
    def botao(self):
        self.bt_salvar = Button(self.subtela_loca_1, text="Registrar", command=self.teste)
        self.bt_salvar.place(relx=0.85, rely=0.72, relheight=0.15, relwidth=0.15)
        
        self.bt_Limpar = Button(self.subtela_loca_1, text="Limpar", command=self.Limpar_tela)
        self.bt_Limpar.place(relx=0.70, rely=0.72, relheight=0.15, relwidth=0.15)

    def teste(self):
        print("Algo aconteceu")
    
    def Lista(self):
        self.lista=ttk.Treeview(self.subtela_2,height=7,columns=("col 1","col 2","col 3","col 4"))
        
        self.lista.heading("#0",text="ID")
        self.lista.column("#0",width=1)
        
        self.lista.heading("#1",text="Nome")
        self.lista.column("#1",width=50)
        
        self.lista.heading("#2",text="CPF")
        self.lista.column("#2",width=200)
        
        self.lista.heading("#3",text="Telefone")
        self.lista.column("#3",width=125)
        
        self.lista.heading("#4",text="Idade")
        self.lista.column("#4",width=125)
               
        self.lista.place(relx=0.01,rely=0.01,relwidth=0.97,relheight=0.98)
        
        self.scroollista=Scrollbar(self.subtela_2,orient="vertical")
        self.scroollista.configure(command=self.scroollista.set)
        self.scroollista.place(relx=0.98,rely=0.01,relwidth=0.02,relheight=0.97)
                
        self.scroollista = Scrollbar(self.subtela_2, orient="vertical")
        self.scroollista.configure(command=self.lista.view)
        self.lista.configure(yscrollcommand=self.scroollista.set)
        self.scroollista.place(relx=0.98, rely=0.01, relwidth=0.02, relheight=0.97)
    
        self.lista.bind("<Double-1>",self.Clique_duplo)
        
    
