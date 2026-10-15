from dataclasses import dataclass
from datetime import date
from src.dominio.value_objects import FranjaHoraria
@dataclass(frozen=True)
class AgendarCitaCommand:
    medico_id: str; fecha: date; franja: FranjaHoraria; sucursal_id: str; expediente: str
    especialidad: str = ''; motivo: str = ''; canal: str = 'recepcion'
    aseguradora_id: str | None = None; numero_autorizacion: str | None = None
    usuario: str = 'recepcion'
@dataclass(frozen=True)
class CancelarCitaCommand:
    cita_id: str; usuario: str; motivo: str
@dataclass(frozen=True)
class ModificarCitaCommand:
    cita_id: str; franja: FranjaHoraria; sucursal_id: str; usuario: str; motivo: str
@dataclass(frozen=True)
class RegistrarLlegadaCommand:
    cita_id: str; usuario: str = 'recepcion'
@dataclass(frozen=True)
class MarcarNoAtendidaPorRetrasoCommand:
    cita_id: str; usuario: str = 'recepcion'
@dataclass(frozen=True)
class MarcarNoShowCommand:
    cita_id: str; usuario: str = 'recepcion'
@dataclass(frozen=True)
class CancelarJornadaCommand:
    medico_id: str; fecha: date; sucursal_id: str; usuario: str; motivo: str
@dataclass(frozen=True)
class ReagendarCitaCommand:
    cita_id: str; medico_id: str; fecha: date; franja: FranjaHoraria; sucursal_id: str; usuario: str
@dataclass(frozen=True)
class RegistrarPacienteCommand:
    nombre: str; telefono: str; nacimiento: date | None = None; correo: str = ''; aseguradora_id: str | None = None
