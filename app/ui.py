from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List

from .database import Database
from .models import Collaborator, ScheduleEntry
from .services import CollaboratorService, ScheduleService

SHIFT_OPTIONS = ["Manhã", "Tarde"]
STATUS_OPTIONS = ["Ativo", "Inativo"]
WEEKDAYS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

class AppUI:
    def __init__(self, root: tk.Tk, db: Database) -> None:
        self.root = root
        self.db = db
        self.collab_service = CollaboratorService(db)
        self.schedule_service = ScheduleService(db)
        self.selected_collab_id = None

        root.title("Workshift Manager")
        root.geometry("980x680")

        self._build_layout()
        self._refresh_collaborators()

    def _build_layout(self) -> None:
        # Container principal da aplicação
        container = ttk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Seção de colaboradores
        collab_frame = ttk.LabelFrame(container, text="Colaboradores")
        collab_frame.pack(fill=tk.X, expand=False, padx=5, pady=5)

        # Formulário de cadastro/edição
        form = ttk.Frame(collab_frame)
        form.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(form, text="Nome").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var, width=28).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form, text="Função/Cargo").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.role_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.role_var, width=22).grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(form, text="Turno").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        self.shift_var = tk.StringVar(value=SHIFT_OPTIONS[0])
        ttk.Combobox(form, values=SHIFT_OPTIONS, textvariable=self.shift_var, width=10, state="readonly").grid(row=0, column=5, padx=5, pady=2)

        ttk.Label(form, text="Status").grid(row=0, column=6, sticky=tk.W, padx=5, pady=2)
        self.status_var = tk.StringVar(value=STATUS_OPTIONS[0])
        ttk.Combobox(form, values=STATUS_OPTIONS, textvariable=self.status_var, width=10, state="readonly").grid(row=0, column=7, padx=5, pady=2)

        # Checkboxes de dias de folga
        days_frame = ttk.Frame(collab_frame)
        days_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(days_frame, text="Dias de folga:").pack(side=tk.LEFT)
        self.days_vars: List[tk.IntVar] = []
        for i, w in enumerate(WEEKDAYS):
            var = tk.IntVar(value=0)
            self.days_vars.append(var)
            cb = ttk.Checkbutton(days_frame, text=w, variable=var)
            cb.pack(side=tk.LEFT, padx=2)

        # Botões para ações
        btns = ttk.Frame(collab_frame)
        btns.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(btns, text="Adicionar", command=self._add_collaborator).pack(side=tk.LEFT, padx=3)
        ttk.Button(btns, text="Atualizar", command=self._update_collaborator).pack(side=tk.LEFT, padx=3)
        ttk.Button(btns, text="Excluir", command=self._delete_collaborator).pack(side=tk.LEFT, padx=3)
        ttk.Button(btns, text="Limpar seleção", command=self._clear_selection).pack(side=tk.LEFT, padx=3)
        ttk.Button(btns, text="Importar Excel (v1)", command=self._import_excel_v1).pack(side=tk.RIGHT, padx=3)

        # Desenvolvendo Lista de colaboradores 
        cols = ("ID", "Nome", "Cargo", "Turno", "Folga", "Status")
        self.collab_tree = ttk.Treeview(collab_frame, columns=cols, show="headings", height=8)
        for c in cols:
            self.collab_tree.heading(c, text=c)
        self.collab_tree.column("ID", width=50, anchor=tk.CENTER)
        self.collab_tree.column("Nome", width=180)
        self.collab_tree.column("Cargo", width=140)
        self.collab_tree.column("Turno", width=90, anchor=tk.CENTER)
        self.collab_tree.column("Folga", width=160)
        self.collab_tree.column("Status", width=90, anchor=tk.CENTER)
        self.collab_tree.pack(fill=tk.X, padx=5, pady=5)
        self.collab_tree.bind("<<TreeviewSelect>>", self._on_collab_selected)

        # Seção da escala de trabalho
        sched_frame = ttk.LabelFrame(container, text="Escala de Trabalho")
        sched_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        controls = ttk.Frame(sched_frame)
        controls.pack(fill=tk.X, padx=5, pady=5)

        self.period_var = tk.StringVar(value="Semanal")
        ttk.Radiobutton(controls, text="Semanal", variable=self.period_var, value="Semanal").pack(side=tk.LEFT)
        ttk.Radiobutton(controls, text="Mensal", variable=self.period_var, value="Mensal").pack(side=tk.LEFT)

        self.week_start_var = tk.StringVar()
        ttk.Label(controls, text="Início (DD/MM/AAAA)").pack(side=tk.LEFT, padx=10)
        ttk.Entry(controls, textvariable=self.week_start_var, width=12).pack(side=tk.LEFT)

        ttk.Label(controls, text="Filtro turno").pack(side=tk.LEFT, padx=10)
        self.filter_shift_var = tk.StringVar(value="Todos")
        ttk.Combobox(controls, values=["Todos"] + SHIFT_OPTIONS, textvariable=self.filter_shift_var, width=10, state="readonly").pack(side=tk.LEFT)

        self.group_by_day_var = tk.IntVar(value=1)
        ttk.Checkbutton(controls, text="Agrupar por dia", variable=self.group_by_day_var).pack(side=tk.LEFT, padx=10)

        ttk.Button(controls, text="Gerar", command=self._generate_schedule).pack(side=tk.LEFT, padx=10)
        ttk.Button(controls, text="Exportar Excel", command=self._export_schedule).pack(side=tk.LEFT)

        cols2 = ("Nome", "Cargo", "Turno")
        self.sched_tree = ttk.Treeview(sched_frame, columns=cols2, show="tree headings")
        for c in cols2:
            self.sched_tree.heading(c, text=c)
        self.sched_tree.column("Nome", width=180)
        self.sched_tree.column("Cargo", width=140)
        self.sched_tree.column("Turno", width=90, anchor=tk.CENTER)
        self.sched_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.sched_tree.tag_configure("shift_manha", background="#FFF9C4")  
        self.sched_tree.tag_configure("shift_tarde", background="#BBDEFB") 

    def _refresh_collaborators(self) -> None:
        for i in self.collab_tree.get_children():
            self.collab_tree.delete(i)
        for c in self.collab_service.list_all():
            folga = ",".join(WEEKDAYS[d] for d in c.days_off)
            self.collab_tree.insert("", tk.END, values=(c.id, c.name, c.role, c.shift, folga, c.status))

    def _days_off_selected(self) -> List[int]:
        return [i for i, v in enumerate(self.days_vars) if v.get() == 1]

    def _add_collaborator(self) -> None:
        name = self.name_var.get().strip()
        role = self.role_var.get().strip()
        shift = self.shift_var.get().strip()
        status = self.status_var.get().strip()
        days_off = self._days_off_selected()
        if not name or not role:
            messagebox.showwarning("Aviso", "Nome e Cargo são obrigatórios")
            return
        collab = Collaborator(id=None, name=name, role=role, shift=shift, days_off=days_off, status=status)
        self.collab_service.create(collab)
        self._clear_form()
        self._refresh_collaborators()

    def _update_collaborator(self) -> None:
        if self.selected_collab_id is None:
            messagebox.showwarning("Aviso", "Selecione um colaborador para atualizar")
            return
        collab = Collaborator(
            id=self.selected_collab_id,
            name=self.name_var.get().strip(),
            role=self.role_var.get().strip(),
            shift=self.shift_var.get().strip(),
            days_off=self._days_off_selected(),
            status=self.status_var.get().strip()
        )
        self.collab_service.update(collab)
        self._clear_form()
        self._refresh_collaborators()

    def _delete_collaborator(self) -> None:
        if self.selected_collab_id is None:
            messagebox.showwarning("Aviso", "Selecione um colaborador para excluir")
            return
        if messagebox.askyesno("Confirmar", "Deseja excluir o colaborador selecionado?"):
            self.collab_service.delete(self.selected_collab_id)
            self._clear_form()
            self._refresh_collaborators()

    def _clear_form(self) -> None:
        self.name_var.set("")
        self.role_var.set("")
        self.shift_var.set(SHIFT_OPTIONS[0])
        self.status_var.set(STATUS_OPTIONS[0])
        for v in self.days_vars:
            v.set(0)
        self.selected_collab_id = None

    def _clear_selection(self) -> None:
        self.collab_tree.selection_remove(self.collab_tree.selection())
        self._clear_form()

    def _on_collab_selected(self, _evt=None) -> None:
        sel = self.collab_tree.selection()
        if not sel:
            return
        values = self.collab_tree.item(sel[0], "values")
        collab_id = int(values[0])
        self.selected_collab_id = collab_id
      
        self.name_var.set(values[1])
        self.role_var.set(values[2])
        self.shift_var.set(values[3])
        self.status_var.set(values[5])
       
        c = self.collab_service.get(collab_id)
        for i, v in enumerate(self.days_vars):
            v.set(1 if (c and i in c.days_off) else 0)

    def _generate_schedule(self) -> None:
        period = self.period_var.get()
        entries: List[ScheduleEntry] = []
        try:
            start = self.week_start_var.get().strip()
            if not start:
                messagebox.showwarning("Aviso", "Informe a data de início (DD/MM/AAAA)")
                return
            if period == "Semanal":
                entries = self.schedule_service.generate_weekly(start)
            else:
         
                d = parse_ddmmyyyy(start)
                entries = self.schedule_service.generate_monthly(d.year, d.month)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar escala: {e}")
            return
        # Aplica filtro de turno
        fshift = self.filter_shift_var.get()
        if fshift and fshift != "Todos":
            entries = [e for e in entries if e.shift == fshift]

        # Preenche a árvore de escala
        self._populate_schedule(entries)
        self.schedule_service.save_entries(entries)

    def _export_schedule(self) -> None:
        data = []
        for parent in self.sched_tree.get_children(""):
            
            date_text = self.sched_tree.item(parent, "text")
            children = self.sched_tree.get_children(parent)
            if not children:
              
                vals = self.sched_tree.item(parent, "values")
                
                if not date_text:
                    
                    continue
                data.append(ScheduleEntry(id=None, date=date_text, collaborator_id=0, name=vals[0], role=vals[1], shift=vals[2]))
            else:
                for ch in children:
                    vals = self.sched_tree.item(ch, "values")
                    data.append(ScheduleEntry(id=None, date=date_text, collaborator_id=0, name=vals[0], role=vals[1], shift=vals[2]))
        if not data:
            messagebox.showwarning("Aviso", "Gere a escala antes de exportar")
            return
        file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[["Excel","*.xlsx"]], initialfile="escala.xlsx")
        if not file:
            return
        try:
            from .services import ScheduleService
            ScheduleService.export_to_excel(data, file)
            messagebox.showinfo("Exportação", "Escala exportada com sucesso")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar: {e}")

    def _populate_schedule(self, entries: List[ScheduleEntry]) -> None:
        
        for i in self.sched_tree.get_children(""):
            self.sched_tree.delete(i)
        
        if self.group_by_day_var.get() == 1:
            # Agrupando por data
            by_date: dict[str, list[ScheduleEntry]] = {}
            for e in entries:
                by_date.setdefault(e.date, []).append(e)
            for date, items in sorted(by_date.items()):
                parent = self.sched_tree.insert("", tk.END, text=date)
                for e in items:
                    tag = self._tag_for_shift(e.shift)
                    self.sched_tree.insert(parent, tk.END, values=(e.name, e.role, e.shift), tags=(tag,))
        else:
        
            for e in entries:
                tag = self._tag_for_shift(e.shift)
                self.sched_tree.insert("", tk.END, text=e.date, values=(e.name, e.role, e.shift), tags=(tag,))

    def _tag_for_shift(self, shift: str) -> str:
        s = (shift or "").lower()
        if "manhã" in s or "manha" in s:
            return "shift_manha"
        if "tarde" in s:
            return "shift_tarde"
        return ""

    def _import_excel_v1(self) -> None:
        file = filedialog.askopenfilename(filetypes=[["Excel","*.xlsx"], ["Excel","*.xls"]])
        if not file:
            return
        try:
            imported = self.schedule_service.import_collaborators_from_excel(file)
            self._refresh_collaborators()
            messagebox.showinfo("Importação", f"{imported} colaborador(es) importado(s)")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao importar: {e}")

# Funções auxiliares para o tratamento de datas
import datetime as _dt

def dt_today():
    return _dt.date.today()

def parse_ddmmyyyy(s: str):
    try:
        day, month, year = [int(x) for x in s.split("/")]
        return _dt.date(year, month, day)
    except Exception:
        raise ValueError("Formato de data inválido. Use DD/MM/AAAA.")
