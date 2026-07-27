from __future__ import annotations
import tkinter as tk

from .database import Database
from .ui import AppUI
from .services import CollaboratorService, ScheduleService

def main() -> None:
    # Inicializa o banco e interface
    db = Database()
    db.init_schema()
    CollaboratorService(db).normalize_shifts()
    ScheduleService(db).normalize_shifts()
    root = tk.Tk()
    AppUI(root, db)
    root.mainloop()

if __name__ == "__main__":
    main()
