from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Optional

DB_NAME = "database.db"

class Database:
    def __init__(self) -> None:
        # Localiza a pasta que é base do projeto 
        base_dir = Path(__file__).resolve().parents[1]
        data_dir = base_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = data_dir / DB_NAME
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def init_schema(self) -> None:
        conn = self.connect()
        cur = conn.cursor()
        # Tabela de colaboradores
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS collaborators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                shift TEXT NOT NULL, -- 'Manhã' ou 'Tarde'
                days_off TEXT NOT NULL, -- CSV com índices dos dias da semana 0..6
                status TEXT NOT NULL, -- 'Ativo' ou 'Inativo'
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            )
            """
        )
        # Tabela de registros de escala
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS schedule_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL, -- Formato YYYY-MM-DD
                collaborator_id INTEGER NOT NULL,
                shift TEXT NOT NULL,
                FOREIGN KEY (collaborator_id) REFERENCES collaborators(id)
            )
            """
        )
        conn.commit()

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None
