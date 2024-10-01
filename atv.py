import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Conectar ao banco de dados (ou criar um novo)
conn = sqlite3.connect('cidades.db')
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS Cidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    estado TEXT NOT NULL,
    pais TEXT NOT NULL
)
''')
conn.commit()


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Cadastro de Cidades")

        self.nome_var = tk.StringVar()
        self.estado_var = tk.StringVar()
        self.pais_var = tk.StringVar()

        # Criação dos widgets
        self.create_widgets()

        # Carregar cidades no TreeView
        self.carregar_cidades()

    def create_widgets(self):
        # Campos de entrada
        tk.Label(self.master, text="Nome").grid(row=0, column=0)
        tk.Entry(self.master, textvariable=self.nome_var).grid(row=0, column=1)

        tk.Label(self.master, text="Estado").grid(row=1, column=0)
        tk.Entry(self.master, textvariable=self.estado_var).grid(row=1, column=1)

        tk.Label(self.master, text="País").grid(row=2, column=0)
        tk.Entry(self.master, textvariable=self.pais_var).grid(row=2, column=1)

        # Botões
        tk.Button(self.master, text="Incluir", command=self.incluir_cidade).grid(row=3, column=0)
        tk.Button(self.master, text="Alterar", command=self.alterar_cidade).grid(row=3, column=1)
        tk.Button(self.master, text="Excluir", command=self.excluir_cidade).grid(row=3, column=2)

        # TreeView
        self.tree = ttk.Treeview(self.master, columns=('Nome', 'Estado', 'País'), show='headings')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Estado', text='Estado')
        self.tree.heading('País', text='País')
        self.tree.grid(row=4, column=0, columnspan=3)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def carregar_cidades(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor.execute("SELECT * FROM Cidades")
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=(row[1], row[2], row[3]), tags=(row[0],))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            self.nome_var.set(item['values'][0])
            self.estado_var.set(item['values'][1])
            self.pais_var.set(item['values'][2])

    def incluir_cidade(self):
        nome = self.nome_var.get()
        estado = self.estado_var.get()
        pais = self.pais_var.get()
        if nome and estado and pais:
            cursor.execute("INSERT INTO Cidades (nome, estado, pais) VALUES (?, ?, ?)", (nome, estado, pais))
            conn.commit()
            self.carregar_cidades()
            self.limpar_campos()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos")

    def alterar_cidade(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_cidade = self.tree.item(selected_item, 'tags')[0]
            nome = self.nome_var.get()
            estado = self.estado_var.get()
            pais = self.pais_var.get()
            cursor.execute("UPDATE Cidades SET nome=?, estado=?, pais=? WHERE id=?", (nome, estado, pais, id_cidade))
            conn.commit()
            self.carregar_cidades()
            self.limpar_campos()
        else:
            messagebox.showwarning("Aviso", "Selecione uma cidade para alterar")

    def excluir_cidade(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_cidade = self.tree.item(selected_item, 'tags')[0]
            cursor.execute("DELETE FROM Cidades WHERE id=?", (id_cidade,))
            conn.commit()
            self.carregar_cidades()
            self.limpar_campos()
        else:
            messagebox.showwarning("Aviso", "Selecione uma cidade para excluir")

    def limpar_campos(self):
        self.nome_var.set("")
        self.estado_var.set("")
        self.pais_var.set("")


# Inicializar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

    # Fechar a conexão ao sair
    conn.close()
