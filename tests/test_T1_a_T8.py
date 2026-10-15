from datetime import timedelta
import pytest
from src.dominio.value_objects import (HorarioNoDisponible,SobrecupoExcedido,TransicionDeEstatusInvalida)
from src.dominio.cita import EstadoCita
from src.dominio.paciente import Medico
from src.dominio.politicas import AutorizacionPorCatalogo
from src.aplicacion.agendamiento_service import AgendamientoService
from src.aplicacion.atencion_service import AtencionService
from src.aplicacion.jornada_service import JornadaService
from src.aplicacion.comandos import (CancelarCitaCommand,RegistrarLlegadaCommand,MarcarNoShowCommand,CancelarJornadaCommand)
from src.infraestructura.unit_of_work import UnitOfWorkMemoria
from src.infraestructura.lectores import LectoresMemoria
from src.dominio.value_objects import ConflictoDeVersion
from tests.conftest import BASE
class RelojFijo:
    def __init__(self,ahora):self.valor=ahora
    def ahora(self):return self.valor

def test_T1_horario_ocupado_entre_sucursales(entorno):
    a,f,s,cmd=entorno;s.agendar_cita(cmd('s1'))
    with pytest.raises(HorarioNoDisponible):s.agendar_cita(cmd('s2'))

def test_T2_sobrecupo_limite(entorno):
    a,f,s,cmd=entorno;a.medicos['m1']=Medico('m1','Dra. Uno',1)
    s.agendar_cita(cmd('s1'));s.agendar_cita(cmd('s2'))
    with pytest.raises(SobrecupoExcedido):s.agendar_cita(cmd('s1'))

def test_T3_llegadas_14_15_16(entorno):
    a,f,s,cmd=entorno
    for indice,minutos in enumerate((14,15,16)):
        hora=BASE+timedelta(hours=indice)
        cita_id=s.agendar_cita(cmd(hora=hora))['cita_id']
        resultado=AtencionService(f,RelojFijo(hora+timedelta(minutes=minutos))).registrar_llegada(RegistrarLlegadaCommand(cita_id))
        assert resultado==('consultar_medico' if minutos<=15 else 'no_atendida_por_retraso')
        assert a.agendas[('m1',BASE.date())].obtener_cita(cita_id).estado == (EstadoCita.PRESENTE if minutos<=15 else EstadoCita.NO_ATENDIDA_POR_RETRASO)

def test_T4_autorizacion_pendiente(entorno):
    a,f,s,cmd=entorno
    assert s.agendar_cita(cmd(aseguradora='aseg'))['autorizacion']=='pendiente'

def test_T5_auditoria_fallida_revierte(entorno):
    a,f,s,cmd=entorno
    cita_id=s.agendar_cita(cmd())['cita_id']
    servicio=AgendamientoService(lambda:UnitOfWorkMemoria(a,fallar_auditoria=True),AutorizacionPorCatalogo())
    with pytest.raises(RuntimeError):servicio.cancelar_cita(CancelarCitaCommand(cita_id,'recepcion','solicitud'))
    assert a.agendas[('m1',BASE.date())].obtener_cita(cita_id).estado==EstadoCita.AGENDADA
    assert not a.auditoria

def test_T6_version_concurrente(entorno):
    a,f,s,cmd=entorno
    u1=f().__enter__();u2=f().__enter__()
    agenda1=u1.agendas.obtener_por_medico_y_fecha('m1',BASE.date())
    agenda2=u2.agendas.obtener_por_medico_y_fecha('m1',BASE.date())
    from src.dominio.cita import Cita
    for agenda,cid in ((agenda1,'c1'),(agenda2,'c2')):
        agenda.agendar(Cita(cid,'p1','m1','s1',cmd().franja));
    u1.agendas.guardar(agenda1);u2.agendas.guardar(agenda2)
    u1.confirmar()
    with pytest.raises(ConflictoDeVersion):u2.confirmar()
    assert len(a.agendas[('m1',BASE.date())].citas)==1

def test_T7_cancelar_jornada_tres_afectadas(entorno):
    a,f,s,cmd=entorno
    for i in range(3):s.agendar_cita(cmd(hora=BASE+timedelta(hours=i)))
    afectados=JornadaService(f).cancelar_jornada(CancelarJornadaCommand('m1',BASE.date(),'s1','recepcion','médico ausente'))
    assert len(afectados)==3
    assert len(LectoresMemoria(a).citas_afectadas('m1',BASE.date(),'s1'))==3

def test_T8_no_show_de_atendida(entorno):
    a,f,s,cmd=entorno
    cita_id=s.agendar_cita(cmd())['cita_id']
    atencion=AtencionService(f,RelojFijo(BASE+timedelta(hours=2)))
    atencion.registrar_llegada(RegistrarLlegadaCommand(cita_id)) if False else None
    # Registrar llegada a tiempo y cerrar consulta antes de intentar no-show.
    AtencionService(f,RelojFijo(BASE)).registrar_llegada(RegistrarLlegadaCommand(cita_id))
    atencion.cerrar_consulta(cita_id)
    with pytest.raises(TransicionDeEstatusInvalida):atencion.marcar_no_show(MarcarNoShowCommand(cita_id))
