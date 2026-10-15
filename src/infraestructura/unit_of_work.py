import copy
from src.aplicacion.puertos import UnitOfWork
from src.dominio.eventos import CitaCancelada,CitaModificada,RegistroDeAuditoria
from .repositorios_memoria import (AgendaMedicaRepositoryMemoria,PacienteRepositoryMemoria,
 MedicoRepositoryMemoria,AseguradoraRepositoryMemoria,RegistroDeAuditoriaRepositoryMemoria)
class UnitOfWorkMemoria(UnitOfWork):
    def __init__(self,almacen,fallar_auditoria=False):
        self.original=almacen;self.fallar_auditoria=fallar_auditoria
    def __enter__(self):
        self.local=copy.deepcopy(self.original)
        self.agendas=AgendaMedicaRepositoryMemoria(self.local)
        self.pacientes=PacienteRepositoryMemoria(self.local)
        self.medicos=MedicoRepositoryMemoria(self.local)
        self.aseguradoras=AseguradoraRepositoryMemoria(self.local)
        self.auditoria=RegistroDeAuditoriaRepositoryMemoria(self.local,self.fallar_auditoria)
        self.confirmada=False
        return self
    def confirmar(self):
        self.agendas.validar_versiones()
        for agenda in self.agendas.pendientes.values():
            for evento in agenda.eventos:
                if isinstance(evento,(CitaCancelada,CitaModificada)):
                    self.auditoria.agregar(RegistroDeAuditoria(evento.cita_id,evento.usuario,evento.fecha,evento.motivo,type(evento).__name__))
        # Validar también contra el almacén compartido antes de aplicar.
        for key,agenda in self.agendas.pendientes.items():
            actual=self.original.agendas.get(key)
            from src.dominio.value_objects import ConflictoDeVersion
            if (actual.version if actual else 0)!=agenda.version:raise ConflictoDeVersion(str(key))
        self.agendas.aplicar()
        self.original.agendas=copy.deepcopy(self.local.agendas)
        self.original.pacientes=copy.deepcopy(self.local.pacientes)
        self.original.auditoria=copy.deepcopy(self.local.auditoria)
        self.confirmada=True
    def deshacer(self):self.confirmada=False
    def __exit__(self,tipo,valor,traza):
        if tipo or not self.confirmada:self.deshacer()
        return False
