from dataclasses import dataclass
from .value_objects import FranjaHoraria
@dataclass
class Jornada:
    id: str
    sucursal_id: str
    franja: FranjaHoraria
    cancelada: bool = False
    def contiene(self, franja):
        return not self.cancelada and self.franja.inicio <= franja.inicio and franja.fin <= self.franja.fin
