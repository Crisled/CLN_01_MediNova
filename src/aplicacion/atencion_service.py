class AtencionService:
    def __init__(self,uow_factory,reloj): self.uow_factory=uow_factory;self.reloj=reloj
    def registrar_llegada(self,cmd):
        with self.uow_factory() as u:
            agenda=u.agendas.obtener_por_cita(cmd.cita_id)
            resultado=agenda.registrar_llegada(cmd.cita_id,self.reloj.ahora())
            u.agendas.guardar(agenda);u.confirmar()
            return resultado
    def marcar_no_atendida_por_retraso(self,cmd):
        with self.uow_factory() as u:
            agenda=u.agendas.obtener_por_cita(cmd.cita_id)
            agenda.marcar_no_atendida_por_retraso(cmd.cita_id)
            u.agendas.guardar(agenda);u.confirmar()
        return 'no_atendida_por_retraso'
    def marcar_no_show(self,cmd):
        with self.uow_factory() as u:
            agenda=u.agendas.obtener_por_cita(cmd.cita_id)
            agenda.marcar_no_show(cmd.cita_id,self.reloj.ahora())
            u.agendas.guardar(agenda);u.confirmar()
        return 'no_show'
    def cerrar_consulta(self,cita_id):
        with self.uow_factory() as u:
            agenda=u.agendas.obtener_por_cita(cita_id)
            agenda.cerrar_consulta(cita_id);u.agendas.guardar(agenda);u.confirmar()
        return 'atendida'
