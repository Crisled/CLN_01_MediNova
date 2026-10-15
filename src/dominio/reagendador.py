from dataclasses import replace
from uuid import uuid4
from .cita import EstadoCita
from .value_objects import TransicionDeEstatusInvalida
class Reagendador:
    def reagendar(self, origen, destino, cita_id, franja, sucursal_id, limite):
        cita=origen.obtener_cita(cita_id)
        if cita.estado not in (EstadoCita.AFECTADA,EstadoCita.NO_ATENDIDA_POR_RETRASO):
            raise TransicionDeEstatusInvalida('Cita no elegible para reagendar')
        nueva=replace(cita,id=str(uuid4()),medico_id=destino.medico_id,sucursal_id=sucursal_id,
                      franja=franja,estado=EstadoCita.AGENDADA,cita_origen_id=cita.id,llegada=None)
        destino.agendar(nueva,limite)
        return nueva
