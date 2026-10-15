from src.dominio.paciente import Paciente
from src.dominio.value_objects import Contacto
class PacienteService:
    def __init__(self,uow_factory): self.uow_factory=uow_factory
    def registrar_paciente(self,cmd):
        with self.uow_factory() as u:
            if u.pacientes.buscar_por_telefono(cmd.telefono): raise ValueError('Paciente posiblemente duplicado')
            expediente=u.pacientes.siguiente_numero_de_expediente()
            u.pacientes.agregar(Paciente(expediente,cmd.nombre,Contacto(cmd.telefono,cmd.correo),cmd.nacimiento,cmd.aseguradora_id))
            u.confirmar()
        return expediente
