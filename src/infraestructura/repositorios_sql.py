"""Adaptadores SQL: contratos explícitos para una integración SQL futura.
No se simula persistencia real: requieren conexión y mapeadores de Aggregates.
"""
from src.dominio.repositorios import AgendaMedicaRepository,PacienteRepository,MedicoRepository,AseguradoraRepository,RegistroDeAuditoriaRepository
class _SqlPendiente:
    def __init__(self,conexion): self.conexion=conexion
    def _pendiente(self):raise NotImplementedError('Se requiere implementar mapeo SQL y control de versión')
class AgendaMedicaRepositorySql(_SqlPendiente,AgendaMedicaRepository):
    def obtener_por_medico_y_fecha(self,medico_id,fecha):self._pendiente()
    def obtener_por_cita(self,cita_id):self._pendiente()
    def guardar(self,agenda):self._pendiente()
class PacienteRepositorySql(_SqlPendiente,PacienteRepository):
    def obtener_por_expediente(self,numero):self._pendiente()
    def buscar_por_telefono(self,telefono):self._pendiente()
    def agregar(self,paciente):self._pendiente()
    def siguiente_numero_de_expediente(self):self._pendiente()
class MedicoRepositorySql(_SqlPendiente,MedicoRepository):
    def obtener(self,medico_id):self._pendiente()
class AseguradoraRepositorySql(_SqlPendiente,AseguradoraRepository):
    def obtener(self,aseguradora_id):self._pendiente()
class RegistroDeAuditoriaRepositorySql(_SqlPendiente,RegistroDeAuditoriaRepository):
    def agregar(self,registro):self._pendiente()
