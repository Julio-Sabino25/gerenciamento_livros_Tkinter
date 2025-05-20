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

try:
    clientes = pd.read_excel(rf"C:\Users\julio\Documents\Pasta GIT\Projetos Python\gerenciamento_livros_Tkinter\Clientes_cadastrados.xlsx")
    opcao = 1
except FileNotFoundError:
    print("Arquivos não encontrados no primeiro caminho, tentando o segundo...")
    clientes = pd.read_excel(rf"C:\Users\julio\Documents\Pasta GIT\Biblioteca\Clientes_cadastrados.xlsx")
    opcao = 2
    
except Exception as e:
    print(f"Ocorreu um erro ao tentar ler os arquivos: {str(e)}")
    
finally:
    print(f"Resultado: consegui ler na opção {opcao}")
    
    
#Funções para atualizar o locador:


def Salva_Cadastro():
    clientes.to_excel(r'C:\Users\julio\Documents\Pasta GIT\Projetos Python\gerenciamento_livros_Tkinter\Clientes_cadastrados.xlsx', index=False)
    
class CadastroGUI:
    def __init__(self, root):
        self.root = root
        self.janela = Toplevel(self.root)
        self.janela.title("Cadastro de Clientes")
        self.configurar_interface()
        
    def configurar_interface(self):
        self.janela.geometry("800x600")
        self.janela.configure(background="#000000")
        
        self.frame_principal = Frame(self.janela, bg="#dfe3ee")
        self.frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Campos do formulário
        campos = [
            ("Nome", 0),
            ("CPF", 1),
            ("Data Nascimento", 2),
            ("Telefone", 3),
            ("Endereço", 4),
            ("Bairro", 5),
            ("Cidade", 6),
            ("CEP", 7),
            ("Observações", 8)
        ]
        
        self.entries = {}
        for texto, linha in campos:
            Label(self.frame_principal, text=texto+":", bg="#dfe3ee").grid(row=linha, column=0, sticky='w', padx=5, pady=5)
            entry = Entry(self.frame_principal, width=40)
            entry.grid(row=linha, column=1, padx=5, pady=5)
            self.entries[texto.lower().replace(" ", "_")] = entry
        
        # Botão de cadastro
        Button(self.frame_principal, text="Cadastrar", command=self.cadastrar_cliente,
              bg="#759fe6", fg="white").grid(row=9, column=0, columnspan=2, pady=10)

    def cadastrar_cliente(self):
        try:
            # Obter valores dos campos
            dados = {campo: entry.get() for campo, entry in self.entries.items()}
            
            # Criar instância da classe de lógica
            novo_cadastro = cadastro(
                nome=dados['nome'],
                cpf=dados['cpf'],
                nascimento=dados['data_nascimento'],
                telefone=dados['telefone'],
                endereco=dados['endereço'],
                bairro=dados['bairro'],
                cidade=dados['cidade'],
                cep=dados['cep'],
                obs=dados['observações']
            )
            
            # Executar cadastro
            resultado = novo_cadastro.cadastrar_atributo()
            if resultado is None:
                print("Cadastro realizado com sucesso!")
                Salva_Cadastro()  # Salva no Excel
                self.janela.destroy()  # Fecha a janela após cadastro
            else:
                print(resultado)
        except Exception as e:
            print(f"Erro ao cadastrar: {str(e)}")


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


    def pop_cli(self):
        for i, row in clientes.iterrows():
            self.lista.insert("", "end", text=i, values=(row['Nome '], row['CPF'], row['Telefone'], row['Idade']))
            
        
    
                
class Gerencial(funcoes):
    
    def __init__(self):
        self.root=root
        self.tela()
        self.subtelas()
        self.Descrição_Texto()
        self.Caixa_texto()
        self.botoes()
        self.Lista()
        self.pop_cli()
        self.Menus()
        root.mainloop()      
        
        
        
        
    def tela(self):
 
        self.root.title("Gerenciamento de Biblioteca")
        self.root.configure(background="#000000") 
        self.root.geometry("900x700")
        self.root.resizable(True,True)
        self.root.maxsize(width=1020,height=800)
        self.root.minsize(width=800, height=500)
    



    def subtelas(self):

        self.label_titulo = Label(self.janela_cli, text="Cadastro de Clientes", bg="#dfe3ee", font=("Arial", 14, "bold"))
        self.label_titulo.place(relx=0.02, rely=0.01, relwidth=0.96, relheight=0.05)

        # Primeira Subtela
        self.subtela_1 = Frame(self.janela_cli, bd=4, bg="#dfe3ee", highlightbackground="#759fe6", highlightthickness=2)
        self.subtela_1.place(relx=0.02, rely=0.07, relwidth=0.96, relheight=0.36)

        # Segunda Subtela
        self.subtela_2 = Frame(self.janela_cli, bd=4, bg="#dfe3ee", highlightbackground="#759fe6", highlightthickness=2)
        self.subtela_2.place(relx=0.02, rely=0.443, relwidth=0.96, relheight=0.54)
        
        
        
        
    def Descrição_Texto(self):
        self.lb_codigo= Label(self.subtela_1,text="ID Clientes",bg ="#dfe3ee")
        self.lb_codigo.place(relx=0.001,rely=0.01,relheight=0.1,relwidth=0.13)
        
        self.lb_codigo= Label(self.subtela_1,text="Nome Completo",bg ="#dfe3ee")
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
             
        
    def botoes(self):
        self.bt_Limpar= Button(self.subtela_1,text="Limpar",command=self.Limpar_tela)
        self.bt_Limpar.place(relx=0.15,rely=0.1,relheight=0.1,relwidth=0.15)
        
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
        barra_menu = Menu(self.root)
        self.root.config(menu=barra_menu)  
        
        filemenu = Menu(barra_menu, tearoff=0)
        filemenu.add_command(label="Cadastrar novo Cliente", command=self.abrir_cadastro)
        filemenu.add_command(label="Sair", command=self.root.destroy)
        
        barra_menu.add_cascade(label="Opções", menu=filemenu)
    
    def abrir_cadastro(self):
        CadastroGUI(self.root)   
        
Gerencial()