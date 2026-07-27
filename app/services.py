from __future__ import annotations
import datetime as dt
from typing import List, Optional, Iterable
import pandas as pd

from .database import Database
from .models import Collaborator, ScheduleEntry

WEEKDAY_PT = [
    "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"
]

class CollaboratorService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def list_all(self) -> List[Collaborator]:
        cur = self.db.connect().cursor()
        cur.execute("SELECT * FROM collaborators ORDER BY name ASC")
        rows = cur.fetchall()
        result: List[Collaborator] = []
        for r in rows:
            days_off = [int(x) for x in (r["days_off"] or "").split(",") if x != ""]
            result.append(Collaborator(
                id=r["id"], name=r["name"], role=r["role"], shift=r["shift"],
                days_off=days_off, status=r["status"]
            ))
        return result

    def get(self, collaborator_id: int) -> Optional[Collaborator]:
        cur = self.db.connect().cursor()
        cur.execute("SELECT * FROM collaborators WHERE id=?", (collaborator_id,))
        r = cur.fetchone()
        if not r:
            return None
        days_off = [int(x) for x in (r["days_off"] or "").split(",") if x != ""]
        return Collaborator(
            id=r["id"], name=r["name"], role=r["role"], shift=r["shift"],
            days_off=days_off, status=r["status"]
        )

    def create(self, c: Collaborator) -> int:
        cur = self.db.connect().cursor()
        days_off_csv = ",".join(str(d) for d in c.days_off)
        cur.execute(
            """
            INSERT INTO collaborators(name, role, shift, days_off, status)
            VALUES(?,?,?,?,?)
            """,
            (c.name, c.role, c.shift, days_off_csv, c.status)
        )
        self.db.connect().commit()
        return cur.lastrowid

    def update(self, c: Collaborator) -> None:
        if c.id is None:
            raise ValueError("Collaborator.id is required for update")
        cur = self.db.connect().cursor()
        days_off_csv = ",".join(str(d) for d in c.days_off)
        cur.execute(
            """
            UPDATE collaborators
            SET name=?, role=?, shift=?, days_off=?, status=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
            """,
            (c.name, c.role, c.shift, days_off_csv, c.status, c.id)
        )
        self.db.connect().commit()

    def delete(self, collaborator_id: int) -> None:
        cur = self.db.connect().cursor()
        # Remove schedule entries bound to collaborator (optional cleanup)
        cur.execute("DELETE FROM schedule_entries WHERE collaborator_id=?", (collaborator_id,))
        cur.execute("DELETE FROM collaborators WHERE id=?", (collaborator_id,))
        self.db.connect().commit()

    def normalize_shifts(self) -> None:
        """Converte qualquer turno 'Noite' para 'Tarde' (compatibilidade)."""
        cur = self.db.connect().cursor()
        cur.execute("UPDATE collaborators SET shift='Tarde' WHERE lower(shift) LIKE '%noite%'")
        self.db.connect().commit()

class ScheduleService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def _active_collaborators(self) -> List[Collaborator]:
        collab_service = CollaboratorService(self.db)
        return [c for c in collab_service.list_all() if c.status == "Ativo"]

    @staticmethod
    def _parse_date_ddmmyyyy(date_str: str) -> dt.date:
        # Aceita datas feitas  no formato 'DD/MM/AAAA'
        day, month, year = [int(x) for x in date_str.split("/")]
        return dt.date(year, month, day)

    def generate_weekly(self, start_date_ddmmyyyy: str) -> List[ScheduleEntry]:
        start = self._parse_date_ddmmyyyy(start_date_ddmmyyyy)
        active = self._active_collaborators()
        entries: List[ScheduleEntry] = []
        for i in range(7):
            d = start + dt.timedelta(days=i)
            weekday = d.weekday()  # 0=Seg .. 6=Dom
            for c in active:
                if weekday in c.days_off:
                    continue
                entries.append(ScheduleEntry(
                    id=None,
                    date=d.isoformat(),
                    collaborator_id=c.id or 0,
                    name=c.name,
                    role=c.role,
                    shift=c.shift,
                ))
        return entries

    def generate_monthly(self, year: int, month: int) -> List[ScheduleEntry]:
        active = self._active_collaborators()
        entries: List[ScheduleEntry] = []
        d = dt.date(year, month, 1)
        while d.month == month:
            weekday = d.weekday()
            for c in active:
                if weekday in c.days_off:
                    continue
                entries.append(ScheduleEntry(
                    id=None,
                    date=d.isoformat(),
                    collaborator_id=c.id or 0,
                    name=c.name,
                    role=c.role,
                    shift=c.shift,
                ))
            d += dt.timedelta(days=1)
        return entries

    def save_entries(self, entries: Iterable[ScheduleEntry]) -> None:
        cur = self.db.connect().cursor()
        cur.executemany(
            """
            INSERT INTO schedule_entries(date, collaborator_id, shift)
            VALUES(?,?,?)
            """,
            [(e.date, e.collaborator_id, e.shift) for e in entries]
        )
        self.db.connect().commit()

    @staticmethod
    def export_to_excel(entries: List[ScheduleEntry], file_path: str) -> None:
        df = pd.DataFrame([
            {"Data": e.date, "Nome": e.name, "Cargo": e.role, "Turno": e.shift}
            for e in entries
        ])
        df.sort_values(by=["Data", "Nome"], inplace=True)
        df.to_excel(file_path, index=False, engine="openpyxl")

    def normalize_shifts(self) -> None:
        """Converte qualquer turno 'Noite' para 'Tarde' nos registros de escala."""
        cur = self.db.connect().cursor()
        cur.execute("UPDATE schedule_entries SET shift='Tarde' WHERE lower(shift) LIKE '%noite%'")
        self.db.connect().commit()

    # Utilitários
    @staticmethod
    def _weekday_name_to_idx(name: str) -> int:
        name = (name or "").strip().lower()
        mapping = {
            "segunda": 0, "seg": 0,
            "terça": 1, "terca": 1, "ter": 1,
            "quarta": 2, "qua": 2,
            "quinta": 3, "qui": 3,
            "sexta": 4, "sex": 4,
            "sábado": 5, "sabado": 5, "sáb": 5, "sab": 5,
            "domingo": 6, "dom": 6,
        }
        return mapping.get(name, -1)

    def import_collaborators_from_excel(self, file_path: str) -> int:
        """
        Importa colaboradores de um Excel da versão anterior (colunas podem incluir:
        Nome, Folga Fixa, Cargo, Data de Entrada, Salário). Apenas Nome, Cargo e
        Folga Fixa são mapeados. Turno padrão: 'Manhã'; Status padrão: 'Ativo'.
        Retorna o número de linhas importadas.
        """
        df = pd.read_excel(file_path, engine="openpyxl")
        imported = 0
        collab_service = CollaboratorService(self.db)
        for _, row in df.iterrows():
            name = str(row.get("Nome", "")).strip()
            role = str(row.get("Cargo", "")).strip()
            folga = str(row.get("Folga Fixa", "")).strip()
            turno_raw = str(row.get("Turno", "")).strip().lower()
            if not name or not role:
                continue
            days_off: List[int] = []
            if folga:
                parts = [p.strip() for p in str(folga).replace("/", ",").split(",")]
                for p in parts:
                    idx = self._weekday_name_to_idx(p)
                    if idx >= 0:
                        days_off.append(idx)
            # Normaliza turno importado: apenas 'Manhã' e 'Tarde'
            if "tarde" in turno_raw:
                turno = "Tarde"
            elif "noite" in turno_raw:
                turno = "Tarde"  # Noite mapeia para Tarde
            elif "manha" in turno_raw or "manhã" in turno_raw:
                turno = "Manhã"
            else:
                turno = "Manhã"
            c = Collaborator(id=None, name=name, role=role, shift=turno, days_off=days_off, status="Ativo")
            collab_service.create(c)
            imported += 1
        return imported
