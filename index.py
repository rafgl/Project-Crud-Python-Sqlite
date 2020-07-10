from tkinter import ttk
from tkinter import *


import sqlite3

class Usuario:
    # Conexão com o banco
    db_name = 'banco.db'

    def __init__(self, janela):
        # Inicialização
        self.janela = janela
        self.janela.title('Projeto CRUD - Cadastro de Usuarios')


        # Criação da janela do programa
        frame = Frame(self.janela)
        frame.grid(row = 2, column = 0 , columnspan = 10, pady = 1)

        # Entrada do nome
        Label(frame, text = 'Nome: ').grid(row = 1, column = 0)
        self.nome = Entry(frame)
        self.nome.focus()
        self.nome.grid(row = 1, column = 1)

        # Entrada do E-mail
        Label(frame, text = 'Email: ').grid(row = 2, column = 0)
        self.email = Entry(frame)
        self.email.grid(row = 2, column = 1)

        # Botão para adicionar o usuario
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('new3.TButton', background='#3CB371', foreground='white', width=20, borderwidth=1, focuscolor='none')
        style.map('new3.TButton', background=[('active', '#3CB371')])
        ttk.Button(frame, text = 'Salvar usuario', command = self.adicionar_usuario, style = "new3.TButton").grid(row = 3, columnspan = 2, sticky = W + E)

        # Mensagens de saída
        self.texto = Label(text = '', fg = 'green')
        self.texto.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Tabela
        self.tree = ttk.Treeview(height = 5, columns = 2)
        self.tree.heading('#0', anchor= W)
        self.tree.column('#0', stretch=0, width=100)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nome', anchor = SW)
        self.tree.heading('#1', anchor= W)
        self.tree.column('#1', stretch=0, width=150)
        self.tree.heading('#1', text = 'Email', anchor = SW)

        # Botões
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('new.TButton', background='#8B0000', foreground='white', width=1, borderwidth=1,focuscolor='none')
        style.map('TButton', background=[('active', '#8B0000')])
        ttk.Button(text = 'Deletar', command = self.deletar_usuario, style = "new.TButton").grid(row = 5, column = 0, sticky = W + E)
        style.configure('new2.TButton', background='#7B68EE', foreground='white', width=10, borderwidth=1, focuscolor='none')
        style.map('new2.TButton', background=[('active', '#7B68EE')])
        ttk.Button(text = 'Editar', command = self.editar_usuario, style = "new2.TButton").grid( row = 5, column = 1, sticky = W + E)

        # Para preencher as linhas
        self.obter_usuario()

    # Consulta no banco
    def executar_consulta(self, query, parametros = ()):
        with sqlite3.connect(self.db_name) as comando:
            cursor = comando.cursor()
            resultado = cursor.execute(query, parametros)
            comando.commit()
        return resultado

    # Pegar usuarios no banco
    def obter_usuario(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Pegar dados
        query = 'SELECT * FROM usuario ORDER BY name DESC'
        db_rows = self.executar_consulta(query)
        # preenchendo dados
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    # Validação de dados inseridos do usuario
    def validacao(self):
        return len(self.nome.get()) != 0 and len(self.email.get()) != 0

    # Adicionar usuario
    def adicionar_usuario(self):
        if self.validacao():
            query = 'INSERT INTO usuario VALUES(NULL, ?, ?)'
            parametros =  (self.nome.get(), self.email.get())
            self.executar_consulta(query, parametros)
            self.texto['text'] = 'Usuario {} salvo com sucesso'.format(self.nome.get())
            self.nome.delete(0, END)
            self.email.delete(0, END)
        else:
            self.texto['text'] = 'Nome e Email é preciso!'
        self.obter_usuario()

    # Deletar usuario
    def deletar_usuario(self):
        self.texto['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
           # Se não selecionar nenhum registro
        except IndexError as e:
            self.texto['text'] = 'Por favor selecione um registro.'
            return
        self.texto['text'] = ''
        nome = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM usuario WHERE name = ?'
        self.executar_consulta(query, (nome, ))
        self.texto['text'] = 'Registro {} deletado com sucesso.'.format(nome)
        self.obter_usuario()

    # Editar usuario
    def editar_usuario(self):
        self.texto['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
            # Se não selecionar nenhum registro
        except IndexError as e:
            self.texto['text'] = 'Por favor, selecione o registro.'
            return
        nome = self.tree.item(self.tree.selection())['text']
        old_email = self.tree.item(self.tree.selection())['values'][0]
        self.edit_janela = Toplevel()
        self.edit_janela.title = 'Editar usuario'

        # Antigo nome

        # Novo nome
        Label(self.edit_janela, text = 'Nome novo:').grid(row = 1, column = 1)
        new_nome = Entry(self.edit_janela)
        new_nome.grid(row = 1, column = 2)


        # Novo Email
        Label(self.edit_janela, text = 'Novo email:').grid(row = 3, column = 1)
        new_email= Entry(self.edit_janela)
        new_email.grid(row = 3, column = 2)
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('new6.TButton', background='#DAA520', foreground='white', width=10, borderwidth=1,focuscolor='none')
        style.map('new6.TButton', background=[('active', '#DAA520')])
        ttk.Button(self.edit_janela,style= 'new6.TButton', text = 'Atualizar', command = lambda: self.editar_registros(new_nome.get(), nome, new_email.get(), old_email)).grid(row = 4, column = 2, sticky = W)
        self.edit_janela.mainloop()

    # Editar usuario
    def editar_registros(self, new_nome, nome, new_email, old_email):
        query = 'UPDATE usuario SET name = ?, email = ? WHERE name = ? AND email = ?'
        parametros = (new_nome, new_email,nome, old_email)
        self.executar_consulta(query, parametros)
        self.edit_janela.destroy()
        self.texto['text'] = 'Registro {} atualizado com sucesso'.format(nome)
        self.obter_usuario()

if __name__ == '__main__':
    janela = Tk()
    application = Usuario(janela)
    janela.geometry("260x240")
    janela.mainloop()
