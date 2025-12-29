from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Collaborator:
    id: Optional[int]
    name: str
    role: str
    shift: str  
    days_off: List[int]  
    status: str  

@dataclass
class ScheduleEntry:
    id: Optional[int]
    date: str  
    collaborator_id: int
    name: str
    role: str
    shift: str
