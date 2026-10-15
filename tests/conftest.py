import pytest
from datetime import datetime,date,timedelta
from src.dominio.value_objects import FranjaHoraria,Contacto
from src.dominio.paciente import Medico,Paciente,Aseguradora
from src.dominio.jornada import Jornada
from src.dominio.agenda_medica import AgendaMedica
from src.infraestructura.repositorios_memoria import AlmacenMemoria
from src.infraestructura.unit_of_work import UnitOfWorkMemoria
from src.dominio.politicas import AutorizacionPorCatalogo
from src.aplicacion.agendamiento_service import AgendamientoService
from src.aplicacion.comandos import AgendarCitaCommand
BASE=datetime(2026,11,10,10,0)
@pytest.fixture
def entorno():
    a=AlmacenMemoria();a.medicos['m1']=Medico('m1','Dra. Uno',0)
    a.pacientes['p1']=Paciente('p1','Paciente Uno',Contacto('8111111111'))
    a.aseguradoras['aseg']=Aseguradora('aseg','Aseguradora',True)
    a.agendas[('m1',BASE.date())]=AgendaMedica('m1',BASE.date(),[
        Jornada('j1','s1',FranjaHoraria(BASE-timedelta(hours=1),BASE+timedelta(hours=8))),
        Jornada('j2','s2',FranjaHoraria(BASE-timedelta(hours=1),BASE+timedelta(hours=8)))])
    factory=lambda:UnitOfWorkMemoria(a)
    service=AgendamientoService(factory,AutorizacionPorCatalogo())
    def comando(sucursal='s1',hora=BASE,aseguradora=None):
        return AgendarCitaCommand('m1',BASE.date(),FranjaHoraria(hora,hora+timedelta(minutes=30)),sucursal,'p1',aseguradora_id=aseguradora)
    return a,factory,service,comando
