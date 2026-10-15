from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from .value_objects import FranjaHoraria, Autorizacion, TransicionDeEstatusInvalida
class EstadoCita(str, Enum):
    AGENDADA='agendada'; PRESENTE='presente'; ATENDIDA='atendida'; NO_SHOW='no_show'; NO_ATENDIDA_POR_RETRASO='no_atendida_por_retraso'; CANCELADA='cancelada'; AFECTADA='afectada'
@dataclass
class Cita:
    id: str
    expediente: str
    medico_id: str
    sucursal_id: str
    franja: FranjaHoraria
    especialidad: str = ''
    motivo: str = ''
    canal: str = 'recepcion'
    aseguradora_id: str | None = None
    autorizacion: Autorizacion | None = None
    estado: EstadoCita = EstadoCita.AGENDADA
    cita_origen_id: str | None = None
    llegada: datetime | None = None
    def transicionar(self, destino: EstadoCita):
        permitidas = {
            EstadoCita.AGENDADA: {EstadoCita.PRESENTE,EstadoCita.NO_SHOW,EstadoCita.NO_ATENDIDA_POR_RETRASO,EstadoCita.CANCELADA,EstadoCita.AFECTADA},
            EstadoCita.PRESENTE: {EstadoCita.ATENDIDA,EstadoCita.CANCELADA,EstadoCita.NO_ATENDIDA_POR_RETRASO},
            EstadoCita.AFECTADA: {EstadoCita.CANCELADA},
        }
        if destino not in permitidas.get(self.estado,set()): raise TransicionDeEstatusInvalida(f'{self.estado} -> {destino}')
        self.estado=destino
    @property
    def bloquea_franja(self):
        return self.estado in (EstadoCita.AGENDADA,EstadoCita.PRESENTE,EstadoCita.ATENDIDA)
