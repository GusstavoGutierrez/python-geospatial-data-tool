import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import pandas as pd
import os
import webbrowser
from processamento import carregar_arquivo, salvar_arquivo
from visualizacao import gerar_mapa_plotly
from gui_utils import exibir_tabela_dados

class NovoLocalDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.transient(parent) 
        self.grab_set() 
        self.parent = parent
        self.title("Adicionar Locais e Salvar Arquivo")
        self.geometry("500x550") # Ajuste conforme necessário
        self.result = None
        self.dados_locais = [] 

        # --- Widgets ---
        main_frame = ttk.Frame(self, padding="10 10 10 10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame para entrada de dados do local
        local_frame = ttk.LabelFrame(main_frame, text="Dados do Local", padding="10 10 10 10")
        local_frame.pack(fill=tk.X, expand=True, pady=5)
        
        ttk.Label(local_frame, text="Nome do Local:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nome_local_entry = ttk.Entry(local_frame, width=40)
        self.nome_local_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        self.metodo_var = tk.StringVar(value="coordenadas") 
        ttk.Label(local_frame, text="Método de Entrada:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(local_frame, text="Coordenadas", variable=self.metodo_var, value="coordenadas", command=self.atualizar_campos_entrada).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(local_frame, text="Endereço", variable=self.metodo_var, value="endereco", command=self.atualizar_campos_entrada).grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.coords_frame = ttk.Frame(local_frame) # Não é LabelFrame para melhor aninhamento visual
        ttk.Label(self.coords_frame, text="Latitude:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.lat_entry = ttk.Entry(self.coords_frame, width=15)
        self.lat_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(self.coords_frame, text="Longitude:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.lon_entry = ttk.Entry(self.coords_frame, width=15)
        self.lon_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        self.endereco_frame = ttk.Frame(local_frame) # Não é LabelFrame
        ttk.Label(self.endereco_frame, text="Endereço Completo:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.endereco_entry = ttk.Entry(self.endereco_frame, width=38)
        self.endereco_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        self.coords_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew") # Mostra por padrão
        self.endereco_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew") # Será ocultado inicialmente


        # Botão Adicionar Local à Lista
        self.adicionar_btn = ttk.Button(local_frame, text="Adicionar Local à Lista", command=self.adicionar_local_lista)
        self.adicionar_btn.grid(row=3, column=0, columnspan=3, padx=5, pady=10)

        # Lista para exibir locais adicionados
        list_frame = ttk.LabelFrame(main_frame, text="Locais Adicionados", padding="10 10 10 10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.locais_listbox = tk.Listbox(list_frame, height=6)
        self.locais_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.locais_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.locais_listbox.config(yscrollcommand=scrollbar.set)

        # Frame para salvar arquivo
        salvar_frame = ttk.LabelFrame(main_frame, text="Salvar Arquivo", padding="10 10 10 10")
        salvar_frame.pack(fill=tk.X, expand=True, pady=5)

        ttk.Label(salvar_frame, text="Nome do Arquivo (sem extensão):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nome_arquivo_entry = ttk.Entry(salvar_frame, width=30)
        self.nome_arquivo_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.formato_var = tk.StringVar(value="csv") 
        ttk.Label(salvar_frame, text="Formato:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        format_options_frame = ttk.Frame(salvar_frame)
        format_options_frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(format_options_frame, text="CSV", variable=self.formato_var, value="csv").pack(side=tk.LEFT)
        ttk.Radiobutton(format_options_frame, text="JSON", variable=self.formato_var, value="json").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_options_frame, text="XML", variable=self.formato_var, value="xml").pack(side=tk.LEFT)


        # Botões de Ação Finais
        action_buttons_frame = ttk.Frame(main_frame, padding="10 0 0 0")
        action_buttons_frame.pack(fill=tk.X, expand=True)

        self.salvar_btn = ttk.Button(action_buttons_frame, text="Salvar Arquivo e Gerar Mapa", command=self.aplicar_e_salvar)
        self.salvar_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        self.cancelar_btn = ttk.Button(action_buttons_frame, text="Cancelar", command=self.destroy)
        self.cancelar_btn.pack(side=tk.RIGHT, padx=5, pady=10)

        self.atualizar_campos_entrada() 
        self.nome_local_entry.focus_set()
        
        # Ajustar tamanho da janela ao conteúdo
        self.update_idletasks() 
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        self.geometry(f"{width+20}x{height+20}")
        self.resizable(False,False)


    def atualizar_campos_entrada(self):
        metodo = self.metodo_var.get()
        if metodo == "coordenadas":
            self.coords_frame.grid()
            self.endereco_frame.grid_remove()
            self.lat_entry.focus_set()
        elif metodo == "endereco":
            self.endereco_frame.grid()
            self.coords_frame.grid_remove()
            self.endereco_entry.focus_set()

    def adicionar_local_lista(self):
        nome = self.nome_local_entry.get().strip()
        if not nome:
            messagebox.showerror("Erro de Entrada", "Nome do local não pode ser vazio.", parent=self)
            return

        metodo = self.metodo_var.get()
        latitude, longitude = None, None

        if metodo == "coordenadas":
            try:
                lat_str = self.lat_entry.get().strip()
                lon_str = self.lon_entry.get().strip()
                if not lat_str or not lon_str:
                    messagebox.showerror("Erro de Entrada", "Latitude e Longitude não podem ser vazias.", parent=self)
                    return
                latitude = float(lat_str)
                longitude = float(lon_str)
            except ValueError:
                messagebox.showerror("Erro de Entrada", "Latitude e Longitude devem ser números válidos.", parent=self)
                return
        elif metodo == "endereco":
            endereco = self.endereco_entry.get().strip()
            if not endereco:
                messagebox.showerror("Erro de Entrada", "Endereço não pode ser vazio.", parent=self)
                return
            try:
                geolocator = Nominatim(user_agent="geo_app_dialog_v2") 
                location = geolocator.geocode(endereco, timeout=10)
                if location:
                    latitude = location.latitude
                    longitude = location.longitude
                    messagebox.showinfo("Endereço Convertido", f"Coordenadas encontradas:\nLat: {latitude:.6f}, Lon: {longitude:.6f}", parent=self)
                else:
                    messagebox.showwarning("Aviso", "Endereço não encontrado. Verifique o endereço e tente novamente.", parent=self)
                    return
            except GeocoderTimedOut:
                messagebox.showerror("Erro de Geocodificação", "Tempo limite excedido ao tentar buscar o endereço.", parent=self)
                return
            except GeocoderUnavailable:
                messagebox.showerror("Erro de Geocodificação", "Serviço de geocodificação indisponível. Verifique sua conexão ou tente mais tarde.", parent=self)
                return
            except Exception as e:
                messagebox.showerror("Erro de Geocodificação", f"Ocorreu um erro: {str(e)}", parent=self)
                return
        
        if latitude is not None and longitude is not None:
            self.dados_locais.append({"nome": nome, "latitude": latitude, "longitude": longitude})
            self.locais_listbox.insert(tk.END, f"{nome} (Lat: {latitude:.4f}, Lon: {longitude:.4f})")
            
            # Limpar campos para próxima entrada
            self.nome_local_entry.delete(0, tk.END)
            self.lat_entry.delete(0, tk.END)
            self.lon_entry.delete(0, tk.END)
            self.endereco_entry.delete(0, tk.END)
            self.nome_local_entry.focus_set()


    def aplicar_e_salvar(self):
        if not self.dados_locais:
            messagebox.showerror("Erro", "Nenhum local foi adicionado à lista. Adicione pelo menos um local antes de salvar.", parent=self)
            return

        nome_arquivo = self.nome_arquivo_entry.get().strip()
        formato = self.formato_var.get()

        if not nome_arquivo:
            messagebox.showerror("Erro de Entrada", "Nome do arquivo não pode ser vazio.", parent=self)
            return

        pasta_destino = "datas" 
        os.makedirs(pasta_destino, exist_ok=True)
        caminho_completo = os.path.join(pasta_destino, f"{nome_arquivo}.{formato}")

        df = pd.DataFrame(self.dados_locais)

        try:
            salvar_arquivo(df, caminho_completo) # (agora com suporte a XML)
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso como:\n{caminho_completo}", parent=self)
            
            if not df.empty:
                gerar_mapa_plotly(df) 
                webbrowser.open("mapa.html")
                exibir_tabela_dados(df, self.parent)
            else:
                messagebox.showinfo("Aviso", "DataFrame está vazio, mapa e tabela não gerado.", parent=self)

            self.destroy() 
        except ValueError as e: 
             messagebox.showerror("Erro ao Salvar", f"{str(e)}", parent=self)
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro durante o salvamento ou geração do mapa: {str(e)}", parent=self)


def processar_arquivo_existente(master_window):
    caminho = filedialog.askopenfilename(
        parent=master_window,
        title="Abrir Arquivo Geoespacial",
        filetypes=[("Arquivos Suportados", "*.csv *.json *.xml"), 
                   ("Arquivos CSV", "*.csv"),
                   ("Arquivos JSON", "*.json"),
                   ("Arquivos XML", "*.xml"),
                   ("Todos os arquivos", "*.*")]
    )

    if not caminho:
        messagebox.showinfo("Aviso", "Nenhum arquivo selecionado.", parent=master_window)
        return

    try:
        df = carregar_arquivo(caminho) #
        if df.empty:
            messagebox.showinfo("Aviso", "O arquivo carregado está vazio ou não contém dados reconhecíveis.", parent=master_window)
            return
        if "latitude" not in df.columns or "longitude" not in df.columns:
            messagebox.showerror("Erro de Formato", "O arquivo não contém as colunas 'latitude' e 'longitude' necessárias.", parent=master_window)
            return
            
        gerar_mapa_plotly(df) #
        webbrowser.open("mapa.html")
        exibir_tabela_dados(df, master_window)
        messagebox.showinfo("Sucesso", "Arquivo processado, mapa gerado e tabela exibida!\nOs dados também foram carregados.", parent=master_window)

    except ValueError as e:
        messagebox.showerror("Erro ao Carregar Arquivo", str(e), parent=master_window)
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao processar o arquivo:\n{str(e)}", parent=master_window)

def processar_novo_arquivo(master_window):
    dialog = NovoLocalDialog(master_window)
    master_window.wait_window(dialog)