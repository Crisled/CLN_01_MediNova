from uuid import uuid4
from src.dominio.cita import Cita
from src.dominio.eventos import CitaCancelada,CitaModificada
from src.dominio.value_objects import (Autorizacion,EstadoAutorizacion,PacienteNoEncontrado,
                                        HorarioNoDisponible,ConflictoDeVersion)
class AgendamientoService:
    def __init__(self,uow_factory,politica_autorizacion,notificador=None):
        self.uow_factory=uow_factory; self.politica=politica_autorizacion; self.notificador=notificador
    def agendar_cita(self,cmd):
        with self.uow_factory() as u:
            if not u.pacientes.obtener_por_expediente(cmd.expediente): raise PacienteNoEncontrado(cmd.expediente)
            medico=u.medicos.obtener(cmd.medico_id)
            if medico is None: raise ValueError('Médico no encontrado')
            aseguradora=u.aseguradoras.obtener(cmd.aseguradora_id) if cmd.aseguradora_id else None
            requiere=self.politica.requiere(aseguradora)
            autorizacion=Autorizacion(EstadoAutorizacion.OTORGADA if cmd.numero_autorizacion else EstadoAutorizacion.PENDIENTE,cmd.numero_autorizacion) if requiere else None
            agenda=u.agendas.obtener_por_medico_y_fecha(cmd.medico_id,cmd.fecha)
            cita=Cita(str(uuid4()),cmd.expediente,cmd.medico_id,cmd.sucursal_id,cmd.franja,
                      cmd.especialidad,cmd.motivo,cmd.canal,cmd.aseguradora_id,autorizacion)
            agenda.agendar(cita,medico.limite_sobrecupo);u.agendas.guardar(agenda)
            try: u.confirmar()
            except ConflictoDeVersion as ex: raise HorarioNoDisponible('Otro usuario reservó el horario') from ex
            eventos=list(agenda.eventos)
        if self.notificador:
            for evento in eventos: self.notificador.notificar(evento)
        return {'cita_id':cita.id,'estatus':cita.estado.value,'autorizacion':autorizacion.estado.value if autorizacion else None}
    def cancelar_cita(self,cmd):
        with self.uow_factory() as u:
            agenda=u.agendas.obtener_por_cita(cmd.cita_id)
            agenda.cancelar(cmd.cita_id,cmd.usuario,cmd.motivo)
            u.agendas.guardar(agenda);u.confirmar()
        return {'cita_id':cmd.cita_id,'estatus':'cancelada'}
    def modificar_cita(self,cmd):
        with self.uow_factory() as u:
            agenda=u.agendas.obtener_por_cita(cmd.cita_id)
            medico=u.medicos.obtener(agenda.medico_id)
            agenda.modificar(cmd.cita_id,cmd.franja,cmd.sucursal_id,medico.limite_sobrecupo,cmd.usuario,cmd.motivo)
            u.agendas.guardar(agenda);u.confirmar()
        return {'cita_id':cmd.cita_id,'estatus':'modificada'}
