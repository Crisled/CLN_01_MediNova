from dataclasses import dataclass, field
from datetime import datetime, timezone
@dataclass(frozen=True)
class Evento:
    cita_id: str | None = None
    usuario: str = 'sistema'
    motivo: str = ''
    fecha: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
class CitaAgendada(Evento): pass
class CitaCancelada(Evento): pass
class CitaModificada(Evento): pass
class ConfirmacionRegistrada(Evento): pass
class AutorizacionRegistrada(Evento): pass
class LlegadaRegistrada(Evento): pass
class CitaNoAtendidaPorRetraso(Evento): pass
class CitaMarcadaComoNoShow(Evento): pass
class JornadaCancelada(Evento): pass
class ConsultaCerrada(Evento): pass
class PacienteRegistrado(Evento): pass
class DatosDePacienteActualizados(Evento): pass
@dataclass(frozen=True)
class RegistroDeAuditoria:
    cita_id: str
    usuario: str
    fecha: datetime
    motivo: str
    tipo: str
