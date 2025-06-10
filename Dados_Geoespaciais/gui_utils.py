import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

def exibir_tabela_dados(df_dados, master_window):
    if df_dados is None or df_dados.empty:
        messagebox.showinfo("Informação", "Não há dados para exibir na tabela.", parent=master_window)
        return

    janela_tabela = tk.Toplevel(master_window)
    janela_tabela.title("Tabela de Dados Geoespaciais")
    janela_tabela.geometry("800x400")

    frame_tabela = ttk.Frame(janela_tabela)
    frame_tabela.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)


    tree = ttk.Treeview(frame_tabela, show="headings")

    if not isinstance(df_dados, pd.DataFrame):
        messagebox.showerror("Erro de Dados", "Os dados fornecidos não são um DataFrame Pandas válido.", parent=master_window)
        janela_tabela.destroy()
        return
        
    colunas = list(df_dados.columns)
    tree["columns"] = colunas
    for coluna in colunas:
        tree.column(coluna, anchor=tk.W, width=100)
        tree.heading(coluna, text=coluna, anchor=tk.W)


    for index, row in df_dados.iterrows():
        tree.insert("", tk.END, values=list(row))

    scrollbar_y = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tree.yview)
    scrollbar_x = ttk.Scrollbar(frame_tabela, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    
    janela_tabela.transient(master_window)
