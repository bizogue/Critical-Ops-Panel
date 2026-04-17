import tkinter as tk
from tkinter import messagebox
import webbrowser
import time

# --- ETAPA 1: Protocolos (Edite os textos aqui) ---
protocolos = {}
for i in range(1, 11):
    protocolos[i] = {
        "v": {"tel": "CCE/CCO", "txt": "Texto para o  CCE:\n"},
        "a": {"tel": f"TEL ATENÇÃO {i}", "txt": f"PROCEDIMENTO DE ALERTA DA LINHA {i}"}
    }

# --- EDIÇÃO DA LINHA 11 (Protocolo Específico) ---
protocolos[11] = {
    "v": {
        "tel": "CE/CO\n(dd) 123 456 / 5678 8918\nCfs\n(dd) 9 999 9999", 
        "txt": "URGÊNCIA LINHA 11: Protocolo de segurança máxima. Ligar imediatamente para os números acima e reportar incidente crítico."
    },
    "a": {
        "tel": "CONTROLO INTERNO\nRAMAL 5050\n(31) 9 8888-8888", 
        "txt": "ATENÇÃO LINHA 11: Verificação de rotina e monitorização. Reportar qualquer anomalia ao CCOP via rádio ou telefone."
    }
}

# --- ETAPA 2: Configuração de Temas ---
temas = {
    "escuro": {"bg": "#000000", "fg": "#FFFFFF", "btn_sys": "#222222", "lbl_cat": "#FFD700"},
    "claro": {"bg": "#F0F0F0", "fg": "#000000", "btn_sys": "#D0D0D0", "lbl_cat": "#0056b3"}
}
tema_atual = "escuro"

# --- ETAPA 3: Funções do Cronômetro e Protocolo ---

def abrir_janela_protocolo(linha_num, tipo_cor):
    """Abre a janela interna com cronômetro e dados do protocolo"""
    dados = protocolos[linha_num][tipo_cor]
    cores = temas[tema_atual]
    cor_destaque = "#FF0000" if tipo_cor == "v" else "#FFD700"
    
    janela_proto = tk.Toplevel(janela)
    janela_proto.attributes('-fullscreen', True)
    janela_proto.configure(bg=cores["bg"])
    
    inicio_tempo = time.time()

    def atualizar_timer():
        if not janela_proto.winfo_exists(): return
        
        tempo_passado = int(time.time() - inicio_tempo)
        minutos = tempo_passado // 60
        segundos = tempo_passado % 60
        
        # Lógica de cores baseada em 5 minutos (300 segundos)
        if tempo_passado < 150:    cor_timer = "#28a745" # Verde
        elif tempo_passado < 240:  cor_timer = "#ffc107" # Amarelo
        elif tempo_passado < 300:  cor_timer = "#fd7e14" # Laranja
        else:                      cor_timer = "#dc3545" # Vermelho
            
        lbl_timer.config(text=f"TEMPO DE RESPOSTA: {minutos:02d}:{segundos:02d}", fg=cor_timer)
        janela_proto.after(1000, atualizar_timer)

    def finalizar():
        tempo_total = int(time.time() - inicio_tempo)
        minutos = tempo_total // 60
        segundos = tempo_total % 60
        messagebox.showinfo("RESUMO OPERACIONAL", f"Tempo total de execução: {minutos:02d}:{segundos:02d}")
        janela_proto.destroy()

    # Interface da Janela de Protocolo
    lbl_timer = tk.Label(janela_proto, text="TEMPO DE RESPOSTA: 00:00", font=("Arial", 25, "bold"), bg=cores["bg"])
    lbl_timer.pack(pady=20)
    atualizar_timer()

    tk.Label(janela_proto, text="PROTOCOLO OPERACIONAL", font=("Arial", 30, "bold"), bg=cores["bg"], fg=cores["fg"]).pack()

    # Frame Contacto
    frame_tel = tk.Frame(janela_proto, bg=cores["bg"], bd=5, relief="ridge")
    frame_tel.pack(padx=50, pady=10, fill="x")
    tk.Label(frame_tel, text="CONTACTOS:", font=("Arial", 20, "bold"), bg=cores["bg"], fg=cor_destaque).pack()
    tk.Label(frame_tel, text=dados['tel'], font=("Arial", 30, "bold"), bg=cores["bg"], fg=cores["fg"]).pack(pady=10)

    # Frame Texto
    frame_txt = tk.Frame(janela_proto, bg=cores["bg"], bd=5, relief="ridge")
    frame_txt.pack(padx=50, pady=10, fill="both", expand=True)
    tk.Label(frame_txt, text="PROCEDIMENTO:", font=("Arial", 20, "bold"), bg=cores["bg"], fg=cor_destaque).pack()
    tk.Label(frame_txt, text=dados['txt'], font=("Arial", 25), bg=cores["bg"], fg=cores["fg"], wraplength=1100, justify="center").pack(pady=20, expand=True)

    tk.Button(janela_proto, text="CONCLUIR E VOLTAR", command=finalizar, font=("Arial", 20, "bold"), bg=cores["btn_sys"], fg="white", bd=10).pack(side="bottom", fill="x", padx=50, pady=20)

# --- ETAPA 4: Interface Principal ---

def alternar_tema():
    global tema_atual
    tema_atual = "claro" if tema_atual == "escuro" else "escuro"
    cores = temas[tema_atual]
    janela.configure(bg=cores["bg"])
    frame_topo.configure(bg=cores["bg"])
    frame_corpo.configure(bg=cores["bg"])
    lbl_titulo.configure(bg=cores["bg"], fg=cores["fg"])
    btn_tema.configure(bg=cores["btn_sys"], fg=cores["fg"] if tema_atual == "escuro" else "black")
    btn_sair.configure(bg=cores["btn_sys"])
    for widget in frame_corpo.winfo_children():
        if isinstance(widget, tk.Label): widget.configure(bg=cores["bg"], fg=cores["lbl_cat"])

def gerenciar_clique(numero, tipo_nome, coluna, linha_num):
    if messagebox.askyesno("CONFIRMAÇÃO", f"EXECUTAR {tipo_nome}:\nAÇÃO {numero}?"):
        tipo_cor = "v" if coluna == 0 else "a"
        
        # ABRE O EMAIL PARA AMBOS (Vermelho e Amarelo)
        webbrowser.open("https://outlook.live.com/")
        
        abrir_janela_protocolo(linha_num, tipo_cor)

# Inicialização TKinter
janela = tk.Tk()
janela.attributes('-fullscreen', True)
janela.configure(bg=temas[tema_atual]["bg"])
janela.bind("<Escape>", lambda e: janela.destroy())

# Topo
frame_topo = tk.Frame(janela, bg=temas[tema_atual]["bg"])
frame_topo.pack(fill="x", pady=10)
lbl_titulo = tk.Label(frame_topo, text="PAINEL DE COMANDO CRÍTICO", font=("Arial", 26, "bold"), bg=temas[tema_atual]["bg"], fg=temas[tema_atual]["fg"])
lbl_titulo.pack(side="left", padx=20)
btn_tema = tk.Button(frame_topo, text="TEMA CLARO/ESCURO", command=alternar_tema, font=("Arial", 12, "bold"), bg=temas[tema_atual]["btn_sys"], fg=temas[tema_atual]["fg"])
btn_tema.pack(side="right", padx=20)

# Corpo
frame_corpo = tk.Frame(janela, bg=temas[tema_atual]["bg"])
frame_corpo.pack(fill="both", expand=True)
frame_corpo.grid_columnconfigure(0, weight=1)
frame_corpo.grid_columnconfigure(1, weight=1)

categorias = ["ENERGIA", "SEGURANÇA", "REDES", "SISTEMAS", "MENSAGENS", "BACKUP", "SUPORTE", "SAÚDE", "BLOQUEIO", "CRISE", "EXTRAS"]

linha_grid = 0
for i in range(1, 12):
    lbl = tk.Label(frame_corpo, text=categorias[i-1], font=("Arial", 14, "bold"), bg=temas[tema_atual]["bg"], fg=temas[tema_atual]["lbl_cat"])
    lbl.grid(row=linha_grid, column=0, columnspan=2, sticky="s", pady=(5,0))
    frame_corpo.grid_rowconfigure(linha_grid, weight=1)
    linha_grid += 1
    for col in range(2):
        num_btn = ((i-1) * 2) + col + 1
        cor_btn = "#FF0000" if col == 0 else "#FFD700"
        btn = tk.Button(frame_corpo, text=f"AÇÃO {num_btn}\n{'URGÊNCIA' if col == 0 else 'ATENÇÃO'}", command=lambda n=num_btn, t="URGÊNCIA" if col == 0 else "ATENÇÃO", c=col, ln=i: gerenciar_clique(n, t, c, ln), font=("Arial", 14, "bold"), bg=cor_btn, fg="black", relief="raised", bd=6, wraplength=400)
        btn.grid(row=linha_grid, column=col, padx=10, pady=2, sticky="nsew")
    frame_corpo.grid_rowconfigure(linha_grid, weight=4)
    linha_grid += 1

# Sair
btn_sair = tk.Button(janela, text="SAIR (ESC)", command=janela.destroy, bg=temas[tema_atual]["btn_sys"], fg="#FF4444", font=("Arial", 16, "bold"), bd=10)
btn_sair.pack(fill="x", padx=15, pady=15)

janela.mainloop()