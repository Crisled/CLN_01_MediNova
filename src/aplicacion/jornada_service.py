from src.dominio.reagendador import Reagendador
class JornadaService:
    def __init__(self,uow_factory,reagendador=None):
        self.uow_factory=uow_factory;self.reagendador=reagendador or Reagendador()
    def cancelar_jornada(self,cmd):
        with self.uow_factory() as u:
            agenda=u.agendas.obtener_por_medico_y_fecha(cmd.medico_id,cmd.fecha)
            afectadas=agenda.cancelar_jornada(cmd.sucursal_id,cmd.usuario,cmd.motivo)
            u.agendas.guardar(agenda);u.confirmar()
        return [{'cita_id':c.id,'expediente':c.expediente,'estado':'pendiente'} for c in afectadas]
    def reagendar_cita_afectada(self,cmd):
        with self.uow_factory() as u:
            origen=u.agendas.obtener_por_cita(cmd.cita_id)
            destino=u.agendas.obtener_por_medico_y_fecha(cmd.medico_id,cmd.fecha)
            medico=u.medicos.obtener(cmd.medico_id)
            nueva=self.reagendador.reagendar(origen,destino,cmd.cita_id,cmd.franja,cmd.sucursal_id,medico.limite_sobrecupo)
            u.agendas.guardar(destino);u.confirmar()
        return {'cita_id':nueva.id,'cita_origen_id':cmd.cita_id}
