from dataclasses import dataclass
from datetime import date
from .value_objects import Contacto
@dataclass
class Paciente:
    expediente: str
    nombre: str
    contacto: Contacto
    nacimiento: date | None = None
    aseguradora_id: str | None = None
@dataclass(frozen=True)
class Medico:
    id: str
    nombre: str
    limite_sobrecupo: int = 0
@dataclass(frozen=True)
class Aseguradora:
    id: str
    nombre: str
    exige_autorizacion: bool = False
