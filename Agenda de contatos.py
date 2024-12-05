import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

ARQUIVO_CONTATOS = "contatos.json"

def carregar_contatos():
    if os.path.exists(ARQUIVO_CONTATOS):
        with open(ARQUIVO_CONTATOS, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def salvar_contatos(contatos):
    with open(ARQUIVO_CONTATOS, 'w', encoding='utf-8') as file:
        json.dump(contatos, file, ensure_ascii=False, indent=4)

def adicionar_contato():
    nome = simpledialog.askstring("Adicionar Contato", "Nome do contato:")
    if not nome:
        return
    telefone = simpledialog.askstring("Adicionar Contato", "Telefone:")
    email = simpledialog.askstring("Adicionar Contato", "E-mail:")

    if nome in contatos:
        messagebox.showerror("Erro", "Contato já existe!")
    else:
        contatos[nome] = {"telefone": telefone, "email": email}
        salvar_contatos(contatos)
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Contato adicionado com sucesso!")

def visualizar_contato():
    selecionado = lista_contatos.curselection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um contato para visualizar.")
        return
    
    nome = lista_contatos.get(selecionado)
    info = contatos[nome]
    messagebox.showinfo("Detalhes do Contato", f"Nome: {nome}\nTelefone: {info['telefone']}\nE-mail: {info['email']}")

def editar_contato():
    selecionado = lista_contatos.curselection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um contato para editar.")
        return
    
    nome = lista_contatos.get(selecionado)
    telefone = simpledialog.askstring("Editar Contato", f"Novo telefone ({contatos[nome]['telefone']}):", initialvalue=contatos[nome]['telefone'])
    email = simpledialog.askstring("Editar Contato", f"Novo e-mail ({contatos[nome]['email']}):", initialvalue=contatos[nome]['email'])

    contatos[nome] = {"telefone": telefone, "email": email}
    salvar_contatos(contatos)
    atualizar_lista()
    messagebox.showinfo("Sucesso", "Contato atualizado com sucesso!")

def excluir_contato():
    selecionado = lista_contatos.curselection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um contato para excluir.")
        return
    
    nome = lista_contatos.get(selecionado)
    resposta = messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o contato '{nome}'?")
    if resposta:
        del contatos[nome]
        salvar_contatos(contatos)
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Contato excluído com sucesso!")

def atualizar_lista():
    lista_contatos.delete(0, tk.END)
    for nome in contatos:
        lista_contatos.insert(tk.END, nome)

contatos = carregar_contatos()

root = tk.Tk()
root.title("Agenda de Contatos")

frame = tk.Frame(root)
frame.pack(pady=20)

lista_contatos = tk.Listbox(frame, width=40, height=10, selectmode=tk.SINGLE)
lista_contatos.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_contatos.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lista_contatos.yview)

botoes_frame = tk.Frame(root)
botoes_frame.pack(pady=10)

btn_adicionar = tk.Button(botoes_frame, text="Adicionar", width=12, command=adicionar_contato)
btn_adicionar.grid(row=0, column=0, padx=5)

btn_visualizar = tk.Button(botoes_frame, text="Visualizar", width=12, command=visualizar_contato)
btn_visualizar.grid(row=0, column=1, padx=5)

btn_editar = tk.Button(botoes_frame, text="Editar", width=12, command=editar_contato)
btn_editar.grid(row=0, column=2, padx=5)

btn_excluir = tk.Button(botoes_frame, text="Excluir", width=12, command=excluir_contato)
btn_excluir.grid(row=0, column=3, padx=5)

atualizar_lista()
root.mainloop()