import tkinter as tk
from tkinter import ttk
from logica_fluxo import processar_arquivo_existente, processar_novo_arquivo #

def iniciar_interface():
    root = tk.Tk()
    root.title("Análise de Dados Geoespaciais") #
    root.geometry("400x250") #
    root.resizable(False, False) #

    ttk.Label(root, text="Selecione uma opção", font=("Arial", 14)).pack(pady=20) #

    ttk.Button(root, text="📂 Abrir Arquivo Existente", command=lambda: processar_arquivo_existente(root)).pack(pady=10)
    ttk.Button(root, text="➕ Criar Novo Arquivo", command=lambda: processar_novo_arquivo(root)).pack(pady=10)
    ttk.Button(root, text="Sair", command=root.quit).pack(pady=20) #

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()