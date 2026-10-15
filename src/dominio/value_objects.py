from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

class ErrorDeDominio(Exception): pass
class HorarioNoDisponible(ErrorDeDominio): pass
class SobrecupoExcedido(ErrorDeDominio): pass
class FranjaFueraDeJornada(ErrorDeDominio): pass
class TransicionDeEstatusInvalida(ErrorDeDominio): pass
class CitaNoEncontrada(ErrorDeDominio): pass
class PacienteNoEncontrado(ErrorDeDominio): pass
class ConflictoDeVersion(ErrorDeDominio): pass

@dataclass(frozen=True)
class FranjaHoraria:
    inicio: datetime
    fin: datetime
    def __post_init__(self):
        if self.fin <= self.inicio: raise ValueError('La franja debe tener duración positiva')
    def se_solapa(self, otra):
        return self.inicio < otra.fin and otra.inicio < self.fin

@dataclass(frozen=True)
class LimiteDeSobrecupo:
    valor: int = 0
    def __post_init__(self):
        if self.valor < 0: raise ValueError('El límite no puede ser negativo')

class EstadoAutorizacion(str, Enum):
    PENDIENTE='pendiente'; OTORGADA='otorgada'; NO_AUTORIZADA='no_autorizada'
@dataclass(frozen=True)
class Autorizacion:
    estado: EstadoAutorizacion
    numero: str | None = None
@dataclass(frozen=True)
class Confirmacion:
    fecha_envio: datetime
    canal: str
    respuesta: str = 'sin_respuesta'
@dataclass(frozen=True)
class Contacto:
    telefono: str
    correo: str = ''
@dataclass(frozen=True)
class NumeroDeExpediente:
    valor: str
    def __post_init__(self):
        if not self.valor.strip(): raise ValueError('Expediente vacío')
@dataclass(frozen=True)
class Tolerancia:
    minutos: int = 15
    def evaluar(self, programada: datetime, llegada: datetime) -> str:
        retraso = (llegada-programada).total_seconds()/60
        return 'a_tiempo' if retraso <= 0 else ('consultar_medico' if retraso <= self.minutos else 'no_atendida_por_retraso')
