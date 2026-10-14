import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

from DataBase import criar_tabelas
from paciente import cadastrar_paciente, lista_pacientes, buscar_por_cpf
from atendimentos import registrar_atendimento, atendimentos_do_mes
from relatorios import gerar_relatorio_mensal

COR_PRIMARIA   = '#2f5597'
COR_SEGUNDARIA = '#4472C4'
COR_FUNDO      = '#F4F6FA'
COR_BRANCO     = '#FFFFFF'
COR_TEXTO      = '#3F2937'


class AppClinica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clínica Dentista - Sistema de Gestão")
        self.geometry("1000x650")
        self.minsize(900, 600)
        self.configure(bg=COR_FUNDO)

        criar_tabelas()
        self._configurar_estilo()
        self._construir_cabecalho()
        self._construir_abas()

    def _configurar_estilo(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TNotebook", background=COR_FUNDO, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=COR_FUNDO,
            foreground=COR_TEXTO,
            padding=(20, 10),
            font=("Segoe UI", 11),
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", COR_PRIMARIA)],
            foreground=[("selected", COR_BRANCO)],
        )

        style.configure("TFrame", background=COR_FUNDO)
        style.configure("TLabel", background=COR_FUNDO,
                        foreground=COR_TEXTO, font=("Segoe UI", 11))
        style.configure("Titulo.TLabel", font=("Segoe UI", 14, "bold"),
                        foreground=COR_PRIMARIA, background=COR_FUNDO)

        style.configure("TEntry", padding=6, font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11), padding=8)

        style.configure("Primario.TButton",
                        background=COR_PRIMARIA, foreground=COR_BRANCO,
                        borderwidth=0)
        style.map("Primario.TButton",
                  background=[("active", COR_SEGUNDARIA)])

        style.configure("Treeview",
                        font=("Segoe UI", 10), rowheight=26,
                        background=COR_BRANCO, fieldbackground=COR_BRANCO)
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"),
                        background=COR_PRIMARIA, foreground=COR_BRANCO)
        style.map("Treeview.Heading",
                  background=[("active", COR_SEGUNDARIA)])

    def _construir_cabecalho(self):
        header = tk.Frame(self, bg=COR_PRIMARIA, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="🦷 Clínica Dra Elinne Robert 🦷",
            bg=COR_PRIMARIA, fg=COR_BRANCO,
            font=("Segoe UI", 20, "bold"),
        ).pack(side="left", padx=20)

    def _construir_abas(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=15, pady=15)

        self.aba_pacientes    = AbaPacientes(notebook)
        self.aba_atendimentos = AbaAtendimentos(notebook)
        self.aba_relatorios   = AbaRelatorios(notebook)

        notebook.add(self.aba_pacientes,    text="👤 Pacientes")
        notebook.add(self.aba_atendimentos, text="  📅 Atendimentos  ")
        notebook.add(self.aba_relatorios,   text="  📊 Relatórios  ")


# ==================================================
# ABA PACIENTES
# ==================================================
class AbaPacientes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self._construir_formulario()
        self._construir_tabela()
        self.carregar_pacientes()

    def _construir_formulario(self):
        frame = ttk.LabelFrame(self, text=" Cadastrar novo paciente ", padding=15)
        frame.pack(fill="x", pady=(0, 15))

        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nome = ttk.Entry(frame, width=35)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="CPF:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entry_cpf = ttk.Entry(frame, width=20)
        self.entry_cpf.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame, text="Celular:").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.entry_celular = ttk.Entry(frame, width=20)
        self.entry_celular.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(frame, text="➕ Cadastrar", style="Primario.TButton",
                   command=self.salvar_paciente).grid(row=0, column=6, padx=15, pady=5)

        ttk.Button(frame, text="🔄 Limpar",
                   command=self.limpar_campos).grid(row=0, column=7, padx=5, pady=5)

    def _construir_tabela(self):
        frame = ttk.LabelFrame(self, text=" Pacientes cadastrados", padding=10)
        frame.pack(fill="both", expand=True)

        colunas = ("id", "nome", "cpf", "celular")
        self.tree = ttk.Treeview(frame, columns=colunas, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("celular", text="Celular")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nome", width=350)
        self.tree.column("cpf", width=150, anchor="center")
        self.tree.column("celular", width=150, anchor="center")

        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def salvar_paciente(self):
        nome = self.entry_nome.get().strip()
        cpf  = self.entry_cpf.get().strip()
        cel  = self.entry_celular.get().strip()

        if not nome or not cpf or not cel:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        ok, msg = cadastrar_paciente(nome, cpf, cel)
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.carregar_pacientes()
        else:
            messagebox.showerror("Erro", msg)

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_celular.delete(0, tk.END)
        self.entry_nome.focus()

    def carregar_pacientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in lista_pacientes():
            self.tree.insert("", "end", values=p)


# ==================================================
# ABA ATENDIMENTOS
# ==================================================
class AbaAtendimentos(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self._construir_formulario()
        self._construir_tabela()
        self.carregar_atendimentos_mes_atual()

    def _construir_formulario(self):
        frame = ttk.LabelFrame(self, text="Registrar atendimento ", padding=15)
        frame.pack(fill="x", pady=(0, 15))

        ttk.Label(frame, text="CPF do paciente:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_cpf = ttk.Entry(frame, width=20)
        self.entry_cpf.grid(row=0, column=1, padx=5, pady=5)
        self.entry_cpf.bind("<FocusOut>", self._buscar_nome)

        ttk.Label(frame, text="Nome:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.lbl_nome = ttk.Label(frame, text="-", width=25,
                                  foreground=COR_PRIMARIA,
                                  font=("Segoe UI", 11, "bold"))
        self.lbl_nome.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Data (DD/MM/AAAA):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_data = ttk.Entry(frame, width=15)
        self.entry_data.grid(row=1, column=1, padx=5, pady=5)
        self.entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))

        ttk.Label(frame, text="Valor pago (R$):").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.entry_valor = ttk.Entry(frame, width=15)
        self.entry_valor.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(frame, text="Observação:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_obs = ttk.Entry(frame, width=70)
        self.entry_obs.grid(row=2, column=1, columnspan=5, padx=5, pady=5, sticky="we")

        ttk.Button(frame, text="➕ Registrar", style="Primario.TButton",
                   command=self.salvar_atendimento).grid(
            row=3, column=5, padx=5, pady=10, sticky="e")

    def _construir_tabela(self):
        frame = ttk.LabelFrame(self, text=" Atendimento do mês atual ", padding=10)
        frame.pack(fill="both", expand=True)

        colunas = ("nome", "cpf", "celular", "data", "valor")
        self.tree = ttk.Treeview(frame, columns=colunas, show="headings")

        titulos = ["Nome", "CPF", "Celular", "Data", "Valor (R$)"]
        for c, t in zip(colunas, titulos):
            self.tree.heading(c, text=t)

        self.tree.column("nome", width=250)
        self.tree.column("cpf", width=130, anchor="center")
        self.tree.column("celular", width=130, anchor="center")
        self.tree.column("data", width=110, anchor="center")
        self.tree.column("valor", width=100, anchor="e")

        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.lbl_total = ttk.Label(self, text="Total do mês: R$ 0,00",
                                   font=("Segoe UI", 12, "bold"),
                                   foreground=COR_PRIMARIA)
        self.lbl_total.pack(anchor="e", pady=(10, 0))

    def _buscar_nome(self, event=None):
        cpf = self.entry_cpf.get().strip()
        if not cpf:
            return
        p = buscar_por_cpf(cpf)
        self.lbl_nome.config(text=p[1] if p else "❌ não encontrado")

    def salvar_atendimento(self):
        cpf = self.entry_cpf.get().strip()
        p = buscar_por_cpf(cpf)
        if not p:
            messagebox.showerror("Erro", "Paciente não encontrado pelo CPF.")
            return

        try:
            data_obj = datetime.strptime(self.entry_data.get().strip(), "%d/%m/%Y")
            data_iso = data_obj.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Use DD/MM/AAAA.")
            return

        try:
            valor = float(self.entry_valor.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
            return

        registrar_atendimento(p[0], data_iso, valor,
                              self.entry_obs.get().strip())
        messagebox.showinfo("Sucesso", "Atendimento registrado!")

        self.entry_cpf.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.entry_obs.delete(0, tk.END)
        self.lbl_nome.config(text="-")
        self.carregar_atendimentos_mes_atual()

    def carregar_atendimentos_mes_atual(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        hoje = datetime.now()
        dados = atendimentos_do_mes(hoje.year, hoje.month)
        total = 0.0
        for nome, cpf, cel, data, valor in dados:
            data_br = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
            self.tree.insert("", "end",
                             values=(nome, cpf, cel, data_br, f"{valor:.2f}"))
            total += valor

        self.lbl_total.config(
            text=f"Total do mês ({hoje.month:02d}/{hoje.year}): "
                 f"R$ {total:,.2f}".replace(",", "x").replace(".", ",").replace("x", "."))


# ==================================================
# ABA RELATÓRIOS
# ==================================================
class AbaRelatorios(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self._construir()

    def _construir(self):
        frame = ttk.LabelFrame(self, text=" Gerar relatório mensal (Excel) ", padding=25)
        frame.pack(fill="x")

        hoje = datetime.now()

        ttk.Label(frame, text="Mês:").grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.combo_mes = ttk.Combobox(
            frame, values=[f"{m:02d}" for m in range(1, 13)],
            width=5, state="readonly")
        self.combo_mes.grid(row=0, column=1, padx=5)
        self.combo_mes.set(f"{hoje.month:02d}")

        ttk.Label(frame, text="Ano:").grid(row=0, column=2, padx=5, pady=10, sticky="w")
        self.entry_ano = ttk.Entry(frame, width=8)
        self.entry_ano.insert(0, str(hoje.year))
        self.entry_ano.grid(row=0, column=3, padx=5)

        ttk.Button(frame, text="📊 Gerar planilha Excel",
                   style="Primario.TButton",
                   command=self.gerar).grid(row=0, column=4, padx=25, pady=10)

        self.frame_previa = ttk.LabelFrame(self, text=" Prévia do relatório ", padding=10)
        self.frame_previa.pack(fill="both", expand=True, pady=(20, 0))

        colunas = ("nome", "cpf", "celular", "data", "valor")
        self.tree = ttk.Treeview(self.frame_previa, columns=colunas, show="headings")
        for c, t in zip(colunas, ["Nome", "CPF", "Celular", "Data", "Valor (R$)"]):
            self.tree.heading(c, text=t)
        self.tree.column("nome", width=250)
        self.tree.column("cpf", width=130, anchor="center")
        self.tree.column("celular", width=130, anchor="center")
        self.tree.column("data", width=110, anchor="center")
        self.tree.column("valor", width=100, anchor="e")
        self.tree.pack(fill="both", expand=True)

        self.lbl_total = ttk.Label(self, text="",
                                   font=("Segoe UI", 12, "bold"),
                                   foreground=COR_PRIMARIA)
        self.lbl_total.pack(anchor="e", pady=(10, 0))

    def gerar(self):
        try:
            mes = int(self.combo_mes.get())
            ano = int(self.entry_ano.get())
        except ValueError:
            messagebox.showerror("Erro", "Ano/mês inválidos.")
            return
        except Exception as e:
            import traceback
            traceback.print_exc() 
            messagebox.showerror("Erro inesperado", str(e))
                                 
        for item in self.tree.get_children():
            self.tree.delete(item)

        dados = atendimentos_do_mes(ano, mes)
        print(f"[DEBUG] ano={ano} mes={mes} | dados={dados}")
        if not dados:
            messagebox.showinfo("Aviso", "Nenhum atendimento nesse mês.")
            return
        
        total = 0.0
        for nome, cpf, cel, data, valor in dados:
            data_br = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
            self.tree.insert("", "end",
                             values=(nome, cpf, cel, data_br, f"{valor:.2f}"))
            total += valor

        self.lbl_total.config(text=f"TOTAL: R$ {total:.2f}")

        arquivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile=f"relatorio_{ano}_{mes:02d}.xlsx",
            title="Salvar relatorio como...")

        if not arquivo:
            return
        gerar_relatorio_mensal(ano, mes, arquivo)
        messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{arquivo}")