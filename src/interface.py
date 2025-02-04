import customtkinter as ctk
from tkinter import filedialog, messagebox, IntVar
import threading
import os
import sys
from .main import main
from pathlib import Path
import json

# Definindo tema_var como global
tema_var = None

# Função para escolher a pasta de destino
def escolher_pasta():
    global pasta
    pasta = filedialog.askdirectory()
    if pasta:
        pasta_var.set(pasta)

# Função para iniciar o processo
def iniciar_processo():
    try:
        login = login_entry.get()
        senha = senha_entry.get()
        pasta_path = Path(pasta)
        mes_anterior = mes_anterior_var.get() == 1  # Captura o valor da checkbox "Mês Anterior"

        # Definindo Pasta_final como global para ser utilizado em outras partes do código
        global pasta_final
        pasta_final = str(pasta_path)

        if not login or not senha:
            messagebox.showwarning("Campos Incompletos", "Por favor, preencha todos os campos.")
            return

        # Inicia o processo em uma thread separada
        thread = threading.Thread(target=main_thread, args=(login, senha, pasta_final, mes_anterior))
        thread.start()

        # Adiciona uma mensagem de log
        adicionar_log("Processo iniciado...")
        adicionar_log("NÃO FECHE NEM MINIMIZE A JANELA DO CHROME!")
    except Exception:
        adicionar_log("Campos incompletos.")

def main_thread(login, senha, pasta_final, mes_anterior):
    try:
        main(login, senha, pasta_final, mes_anterior)
        adicionar_log("Processo encerrado.")
    except Exception as e:
        adicionar_log(f"Erro: {e}")

# Função para adicionar mensagens de log
def adicionar_log(mensagem):
    log_textbox.configure(state="normal")
    log_textbox.insert("end", mensagem + "\n")
    log_textbox.see("end")
    log_textbox.configure(state="disabled")

# Função para redirecionar a saída para a caixa de texto
class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str)
        self.widget.see("end")
        self.widget.configure(state="disabled")

    def flush(self):
        pass

# Função para alternar entre o frame principal e o frame de configurações
def mostrar_configuracoes():
    frame_principal.pack_forget()
    frame_configuracoes.pack(pady=20, padx=20, fill="both", expand=True)

def voltar_para_principal():
    frame_configuracoes.pack_forget()
    frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

# Função para alterar o tema
def alterar_tema():
    global tema_var
    tema = tema_var.get()
    ctk.set_appearance_mode(tema)
    salvar_configuracoes({"tema": tema})

# Função para salvar ou apagar o login ao marcar ou desmarcar a opção "Lembrar Login"
def salvar_login_senha():
    login = login_entry.get()
    senha = senha_entry.get()
    lembrar = lembrar_login_var.get() == 1

    if lembrar:
        salvar_configuracoes({"login": login, "senha": senha, "lembrar_login": lembrar})
    else:
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
            config.pop("login", None)
            config.pop("senha", None)
            salvar_configuracoes(config)

# Carregar login e senha se existirem
def carregar_login_senha():
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                if config.get("lembrar_login", False):
                    login_entry.insert(0, config.get("login", ""))
                    senha_entry.insert(0, config.get("senha", ""))
                    lembrar_login_var.set(1)
        except Exception as e:
            adicionar_log(f"Erro ao carregar configurações: {e}")

# Função para salvar as configurações
def salvar_configuracoes(config):
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            existing_config = json.load(f)
        existing_config.update(config)
        config = existing_config

    with open("config.json", "w") as f:
        json.dump(config, f)

# Função para carregar as configurações salvas
def carregar_configuracoes():
    try:
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
                if "tema" in config:
                    global tema_var
                    ctk.set_appearance_mode(config["tema"])
                    tema_var.set(config["tema"])
    except Exception as e:
        adicionar_log(f"Erro ao carregar configurações: {e}")

# Configuração da janela principal
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("XML AutoFetch")
root.geometry("600x600")
root.resizable(False, True)
root.iconbitmap("./resources/icon.ico")

# Centralizar a janela na tela
def centralizar_janela():
    root.update_idletasks()
    largura = root.winfo_width()
    altura = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f'{largura}x{altura}+{x}+{y}')

centralizar_janela()

# Frame principal
frame_principal = ctk.CTkFrame(root)
frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

# Botão de configurações
config_button = ctk.CTkButton(frame_principal, text="⚙", width=40, command=mostrar_configuracoes)
config_button.pack(anchor="ne", pady=10, padx=10)

# Campo de login
login_label = ctk.CTkLabel(frame_principal, text="Login:")
login_label.pack(pady=5)
login_entry = ctk.CTkEntry(frame_principal, width=400)
login_entry.pack(pady=5)

# Campo de senha
senha_label = ctk.CTkLabel(frame_principal, text="Senha:")
senha_label.pack(pady=5)
senha_entry = ctk.CTkEntry(frame_principal, show="*", width=400)
senha_entry.pack(pady=5)

# Botão para escolher a pasta de destino
pasta_frame = ctk.CTkFrame(frame_principal)
pasta_frame.pack(pady=5, fill="x")

pasta_label = ctk.CTkLabel(pasta_frame, text="Pasta de Destino:")
pasta_label.grid(row=0, column=0, pady=5)

pasta_var = ctk.StringVar()
pasta_entry = ctk.CTkEntry(pasta_frame, textvariable=pasta_var, width=300)
pasta_entry.grid(row=0, column=1, pady=5, padx=5)

pasta_button = ctk.CTkButton(pasta_frame, text="Escolher Pasta", command=escolher_pasta)
pasta_button.grid(row=0, column=2, pady=5)

# Checkbox para lembrar login
lembrar_login_var = IntVar()
lembrar_login_check = ctk.CTkCheckBox(frame_principal, text="Lembrar Login", variable=lembrar_login_var, command=salvar_login_senha)
lembrar_login_check.pack(pady=5)

# Checkbox para mês anterior
mes_anterior_var = IntVar()
mes_anterior_check = ctk.CTkCheckBox(frame_principal, text="Mês Anterior", variable=mes_anterior_var)
mes_anterior_check.pack(pady=5)

# Botão para iniciar o processo
iniciar_button = ctk.CTkButton(frame_principal, text="Iniciar Processo", command=iniciar_processo)
iniciar_button.pack(pady=20)

# Área de log
log_label = ctk.CTkLabel(frame_principal, text="Log de Execução:")
log_label.pack(pady=5)
log_textbox = ctk.CTkTextbox(frame_principal, width=500, height=150)
log_textbox.pack(pady=5, fill="both", expand=True)
log_textbox.configure(state="disabled")

# Redirecionar a saída padrão e a saída de erro para a área de log
sys.stdout = TextRedirector(log_textbox, "stdout")
sys.stderr = TextRedirector(log_textbox, "stderr")

# Frame de configurações
frame_configuracoes = ctk.CTkFrame(root)

# Seção de temas
tema_var = ctk.StringVar(value="dark")
tema_label = ctk.CTkLabel(frame_configuracoes, text="Tema:")
tema_label.pack(pady=5)

tema_options = [("Claro", "light"), ("Escuro", "dark"), ("Sistema", "system")]
for text, mode in tema_options:
    tema_radio = ctk.CTkRadioButton(frame_configuracoes, text=text, variable=tema_var, value=mode, command=alterar_tema)
    tema_radio.pack(anchor="w")

# Botão para voltar à tela principal
voltar_button = ctk.CTkButton(frame_configuracoes, text="Voltar", command=voltar_para_principal)
voltar_button.pack(pady=20)

# Carregar configurações ao iniciar o programa
carregar_configuracoes()
carregar_login_senha()

root.mainloop()
