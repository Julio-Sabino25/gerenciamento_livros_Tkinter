#Importando Bibliotecas:

import pandas as pd
from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk
from tkinter import tix
import os 
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.pdfgen import canvas
import webbrowser

pd.set_option('display.max_columns', None)

#lendo o banco de dados:
#arquivos em Excel

try:
    biblioteca = pd.read_excel(r"C:\Users\julio\Documents\Pasta GIT\Poo Estudos\biblioteca.xlsx")
    clientes = pd.read_excel(r'C:\Users\julio\Documents\Pasta GIT\Poo Estudos\Clientes_cadastrados.xlsx')
    opcao = 1
    
except FileNotFoundError:
    print("Arquivos não encontrados no primeiro caminho, tentando o segundo...")
    biblioteca = pd.read_excel(r'C:\Users\julio\Documents\Pasta GIT\Biblioteca\biblioteca.xlsx')
    clientes = pd.read_excel(r'C:\Users\julio\Documents\Pasta GIT\Biblioteca\Clientes_cadastrados.xlsx')
    opcao = 2
    
except Exception as e:
    opcao = f"Ocorreu um erro ao tentar ler os arquivos: {str(e)}"
    
finally:
    print(f"Resultado: consegui ler na opção {opcao}")
    
    
#Funções para atualizar o locador:

def atualizar_usuario(nome_do_livro, locador):
    print(f"Atualizando locador para o livro: {nome_do_livro}")
    biblioteca['Nome do livro'] = biblioteca['Nome do livro'].str.strip().str.lower()
    nome_do_livro = nome_do_livro.strip().lower()
    biblioteca.loc[biblioteca['Nome do livro'] == nome_do_livro, 'locador'] = locador


def atualizar_cpf(nome_do_livro, cpf):
    biblioteca['Nome do livro'] = biblioteca['Nome do livro'].str.strip().str.lower()
    nome_do_livro = nome_do_livro.strip().lower()
    biblioteca.loc[biblioteca['Nome do livro'] == nome_do_livro, 'CPF'] = cpf


def atualizar_data_retirada(nome_do_livro, data_locada):
    biblioteca['Nome do livro'] = biblioteca['Nome do livro'].str.strip().str.lower()
    nome_do_livro = nome_do_livro.strip().lower()
    biblioteca.loc[biblioteca['Nome do livro'] == nome_do_livro, 'data da locação'] = data_locada
    data_locada = datetime.strptime(data_locada,'%d/%m/%Y')
    data_devolver = data_locada + timedelta(days=5)
    data_devolver = data_devolver.strftime('%d/%m/%Y')
    biblioteca.loc[biblioteca['Nome do livro'] == nome_do_livro, 'Previsão de devolutiva'] = data_devolver


def Multa(nome_do_livro,devolveu):
    devolveu= datetime.strptime(devolveu,'%d/%m/%Y')
    biblioteca.loc[biblioteca['Nome do livro'] == nome_do_livro, 'Data devolvida'] = devolveu
            
    previsto= biblioteca.loc[biblioteca['Nome do livro'] == nome_do_livro, 'Previsão de devolutiva'].values 
    previsto =previsto[0]
    previsto = datetime.strptime(previsto,'%d/%m/%Y') 
    
    if previsto< devolveu:
        biblioteca.loc[biblioteca['Nome do livro'] == nome_do_livro, 'Multa'] = "SIM"
        dif = (devolveu - previsto).days
        biblioteca.loc[biblioteca['Nome do livro'] == nome_do_livro, 'Valor'] = dif * 5.00
        
    else:
        biblioteca.loc[biblioteca['Nome do livro'] == nome_do_livro, 'Multa'] = "NÂO"
        biblioteca.loc[biblioteca['Nome do livro'] == nome_do_livro, 'Valor'] = 0

## Cadastrando Clientes:

def Salva_Cadastro():
    clientes.to_excel(r'C:\Users\julio\Documents\Pasta GIT\Poo Estudos\Clientes_cadastrados.xlsx', index=False)

class cadastro:
    def __init__(self,nome,cpf,nascimento,telefone,endereco,bairro,cidade,cep,obs):
        self.nome=nome
        self.cpf=cpf
        self.nascimento=nascimento
        self.telefone=telefone
        self.Endereco= endereco 
        self.Bairro=bairro
        self.Cidade=cidade
        self.cep=cep
        self.obs=obs
        
    def linha_vazia(self,coluna):
        return clientes[clientes[coluna].isna()].index[0]
            
                
    def CPF_cadastro(self):
        if self.cpf not in clientes['CPF'].values: 
            clientes.at[self.linha_vazia('CPF'), 'CPF'] = self.cpf 
            return True
        else:
            return  False
        
    def cadastrar_atributo(self):
        if self.CPF_cadastro(): 
            clientes.at[self.linha_vazia('Nome'), 'Nome'] = self.nome
            clientes.at[self.linha_vazia('Data de nascimento'), 'Data de nascimento'] = self.nascimento
            clientes.at[self.linha_vazia('Telefone'), 'Telefone'] = self.telefone
            clientes.at[self.linha_vazia('Endereço'), 'Endereço'] = self.Endereco
            clientes.at[self.linha_vazia('Bairro'), 'Bairro'] = self.Bairro
            clientes.at[self.linha_vazia('Cidade'), 'Cidade'] = self.Cidade
            clientes.at[self.linha_vazia('CEP'), 'CEP'] = self.cep
            clientes.at[self.linha_vazia('Observações'), 'Observações'] = self.obs
        else:
            return "CPF já cadastrado"
        
    
    
#Definindo a Tela:    
    
root=tix.Tk()


class funcoes():
    
    def Limpar_tela(self):
        for item in self.lista.get_children():
            self.lista.delete(item)
        self.população()
        self.id_livro_entry.delete(0,END)
        self.nome_entry.delete(0,END)
        self.Autor_entry.delete(0,END)
        self.Genero_entry.delete(0,END)
        
        
        
    def Clique_duplo(self,event):  
        self.id_livro_entry.delete(0,END)
        self.nome_entry.delete(0,END)
        self.Autor_entry.delete(0,END)
        self.Genero_entry.delete(0,END)
        
        for n in self.lista.selection():
            id_livro = self.lista.item(n, 'text')
            col1,col2,col3,col4=self.lista.item(n,'values')
            self.id_livro_entry.insert(END,id_livro)
            self.nome_entry.insert(END,col1)
            self.Autor_entry.insert(END,col2)
            self.Genero_entry.insert(END,col3)



    def população(self):
        for i, row in biblioteca.iterrows():
            self.lista.insert("", "end", text=i, values=(row['Nome do livro'], row['Autor'], row['Genero'], row['data da locação']))
            
      
      
    def filtrar_lista(self,event):
        filtro = self.nome_entry.get().lower()
        opcoes_filtradas = [livro for livro in biblioteca['Nome do livro'] if filtro in livro.lower()]
        
        self.combo_nome['values'] = opcoes_filtradas
        if opcoes_filtradas:
            self.combo_nome.current(0) 
        else:
            self.combo_nome.set('')
                
                
                
    def mostrar_selecao(self):
        selecionado = self.nome_entry.get()

        for item in self.lista.get_children():
            self.lista.delete(item)
        
        df_filtrado = biblioteca[biblioteca['Nome do livro'].str.contains(selecionado)]
        
        # Reinsere os dados filtrados no Treeview
        for index, row in df_filtrado.iterrows():
            self.lista.insert("", "end", text=row['ID_do_livro'], values=(row['Nome do livro'], row['Autor'], row['Genero'], row['data da locação']))

    
    def aluga_livro(self):
        from Aluga_Livro import Aluguel  
        Aluguel(self.root) 
        
    
                
class Gerencial(funcoes):
    
    def __init__(self):
        self.root=root
        self.tela()
        self.subtelas()
        self.Descrição_Texto()
        self.Caixa_texto()
        self.botoes()
        self.Lista()
        self.população()
        self.Menus()
        root.mainloop()      
        
        
        
        
    def tela(self):
        self.root.title("Gerenciamento de Biblioteca")
        self.root.configure(background="#000000") #deixei a cor preta pq eu gosto ;)
        self.root.geometry("900x700")
        self.root.resizable(True,True)
        self.root.maxsize(width=1020,height=800)
        self.root.minsize(width=800, height=500)  
    



    def subtelas(self):

        self.label_titulo = Label(self.root, text="Pesquisa Livro", bg="#dfe3ee", font=("Arial", 14, "bold"))
        self.label_titulo.place(relx=0.02, rely=0.01, relwidth=0.96, relheight=0.05)

        # Primeira Subtela
        self.subtela_1 = Frame(self.root, bd=4, bg="#dfe3ee", highlightbackground="#759fe6", highlightthickness=2)
        self.subtela_1.place(relx=0.02, rely=0.07, relwidth=0.96, relheight=0.36)

        # Segunda Subtela
        self.subtela_2 = Frame(self.root, bd=4, bg="#dfe3ee", highlightbackground="#759fe6", highlightthickness=2)
        self.subtela_2.place(relx=0.02, rely=0.443, relwidth=0.96, relheight=0.54)
        
        
        
        
    def Descrição_Texto(self):
        self.lb_codigo= Label(self.subtela_1,text="ID Livro",bg ="#dfe3ee")
        self.lb_codigo.place(relx=0.001,rely=0.01,relheight=0.1,relwidth=0.13)
        
        self.lb_codigo= Label(self.subtela_1,text="Nome do livro",bg ="#dfe3ee")
        self.lb_codigo.place(relx=0.001,rely=0.25,relheight=0.1,relwidth=0.11)
        
        self.lb_codigo= Label(self.subtela_1,text="Autor",bg ="#dfe3ee")
        self.lb_codigo.place(relx=0.001,rely=0.47,relheight=0.1,relwidth=0.05)       
        self.lb_codigo= Label(self.subtela_1,text="Genero",bg ="#dfe3ee")
        self.lb_codigo.place(relx=0.001,rely=0.7,relheight=0.1,relwidth=0.07)  
        
        
        
        
    def Caixa_texto(self):
        self.id_livro_entry= Entry(self.subtela_1)
        self.id_livro_entry.place(relx=0.005,rely=0.1,relheight=0.1,relwidth=0.13)
        
        self.nome_entry= Entry(self.subtela_1)
        self.nome_entry.place(relx=0.005,rely=0.35,relheight=0.1,relwidth=0.4)
        
        self.Autor_entry = Entry(self.subtela_1)
        self.Autor_entry.place(relx=0.005, rely=0.57, relheight=0.1, relwidth=0.4)
        
        self.Genero_entry = Entry(self.subtela_1)
        self.Genero_entry.place(relx=0.005, rely=0.8, relheight=0.1, relwidth=0.4)
        
        self.combo_nome = ttk.Combobox(self.subtela_1, values=biblioteca['Nome do livro'].tolist())
        self.combo_nome.place(relx=0.5, rely=0.1, relheight=0.1, relwidth=0.4)
        self.nome_entry.bind('<KeyRelease>', self.filtrar_lista)
 
              
        
    def botoes(self):
        self.bt_Limpar= Button(self.subtela_1,text="Limpar",command=self.Limpar_tela)
        self.bt_Limpar.place(relx=0.15,rely=0.1,relheight=0.1,relwidth=0.15)
        
        self.bt_pesquisar= Button(self.subtela_1,text="Pesquisar",command=self.mostrar_selecao)
        self.bt_pesquisar.place(relx=0.31,rely=0.1,relheight=0.1,relwidth=0.15)
        
        self.bt_Alugar= Button(self.subtela_1,text="Alugar",command=self.aluga_livro)
        self.bt_Alugar.place(relx=0.5,rely=0.25,relheight=0.1,relwidth=0.15)
        
    def Lista(self):
        self.lista=ttk.Treeview(self.subtela_2,height=7,columns=("col 1","col 2","col 3","col 4"))
        
        self.lista.heading("#0",text="ID")
        self.lista.column("#0",width=1)
        
        self.lista.heading("#1",text="Nome do livro")
        self.lista.column("#1",width=50)
        
        self.lista.heading("#2",text="Autor")
        self.lista.column("#2",width=200)
        
        self.lista.heading("#3",text="Genero")
        self.lista.column("#3",width=125)
        
        self.lista.heading("#4",text="data da locação")
        self.lista.column("#4",width=125)
               
        self.lista.place(relx=0.01,rely=0.01,relwidth=0.97,relheight=0.98)
        
        self.scroollista=Scrollbar(self.subtela_2,orient="vertical")
        self.scroollista.configure(command=self.scroollista.set)
        self.scroollista.place(relx=0.98,rely=0.01,relwidth=0.02,relheight=0.97)
                
        self.scroollista = Scrollbar(self.subtela_2, orient="vertical")
        self.scroollista.configure(command=self.lista.yview)
        self.lista.configure(yscrollcommand=self.scroollista.set)
        self.scroollista.place(relx=0.98, rely=0.01, relwidth=0.02, relheight=0.97)
    
        self.lista.bind("<Double-1>",self.Clique_duplo)
        
    def Menus(self):
        barra_menu=Menu(self.root)
        self.root.config(menu=barra_menu)  
        
        filemenu=Menu(barra_menu)
       
        def Quit():
            self.root.destroy()
        
        barra_menu.add_cascade(label="Opções",menu=filemenu)
        filemenu.add_command(label="Cadastrar novo Cliente",command=Quit)
        filemenu.add_command(label="Sair",command=Quit)    
        
Gerencial()