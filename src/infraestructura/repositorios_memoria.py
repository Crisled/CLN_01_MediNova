import copy
from src.dominio.agenda_medica import AgendaMedica
from src.dominio.value_objects import CitaNoEncontrada, ConflictoDeVersion
from src.dominio.repositorios import (AgendaMedicaRepository,PacienteRepository,MedicoRepository,
                                       AseguradoraRepository,RegistroDeAuditoriaRepository)
class AlmacenMemoria:
    def __init__(self):
        self.agendas={};self.pacientes={};self.medicos={};self.aseguradoras={};self.auditoria=[]
class AgendaMedicaRepositoryMemoria(AgendaMedicaRepository):
    def __init__(self,almacen): self.almacen=almacen;self.pendientes={}
    def obtener_por_medico_y_fecha(self,medico_id,fecha):
        key=(medico_id,fecha)
        if key in self.pendientes: return self.pendientes[key]
        agenda=copy.deepcopy(self.almacen.agendas.get(key,AgendaMedica(medico_id,fecha)))
        self.pendientes[key]=agenda
        return agenda
    def obtener_por_cita(self,cita_id):
        for (medico,fecha),agenda in {**self.almacen.agendas,**self.pendientes}.items():
            if any(c.id==cita_id for c in agenda.citas): return self.obtener_por_medico_y_fecha(medico,fecha)
        raise CitaNoEncontrada(cita_id)
    def guardar(self,agenda): self.pendientes[(agenda.medico_id,agenda.fecha)]=agenda
    def validar_versiones(self):
        for key,agenda in self.pendientes.items():
            actual=self.almacen.agendas.get(key)
            if (actual.version if actual else 0)!=agenda.version: raise ConflictoDeVersion(str(key))
    def aplicar(self):
        for key,agenda in self.pendientes.items():
            guardada=copy.deepcopy(agenda);guardada.version+=1;guardada.eventos.clear()
            self.almacen.agendas[key]=guardada
class PacienteRepositoryMemoria(PacienteRepository):
    def __init__(self,almacen):self.almacen=almacen
    def obtener_por_expediente(self,numero):return self.almacen.pacientes.get(numero)
    def buscar_por_telefono(self,telefono):return next((p for p in self.almacen.pacientes.values() if p.contacto.telefono==telefono),None)
    def agregar(self,paciente):
        if paciente.expediente in self.almacen.pacientes:raise ValueError('Expediente duplicado')
        self.almacen.pacientes[paciente.expediente]=paciente
    def siguiente_numero_de_expediente(self):return f'MN-{len(self.almacen.pacientes)+1:06d}'
class MedicoRepositoryMemoria(MedicoRepository):
    def __init__(self,almacen):self.almacen=almacen
    def obtener(self,medico_id):return self.almacen.medicos.get(medico_id)
class AseguradoraRepositoryMemoria(AseguradoraRepository):
    def __init__(self,almacen):self.almacen=almacen
    def obtener(self,aseguradora_id):return self.almacen.aseguradoras.get(aseguradora_id)
class RegistroDeAuditoriaRepositoryMemoria(RegistroDeAuditoriaRepository):
    def __init__(self,almacen,fallar=False):self.almacen=almacen;self.fallar=fallar
    def agregar(self,registro):
        if self.fallar:raise RuntimeError('Error simulado de auditoría')
        self.almacen.auditoria.append(registro)
