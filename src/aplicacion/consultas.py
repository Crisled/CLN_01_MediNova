from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class ConsultarDisponibilidadDelMedico:
    medico_id: str; fecha: date
@dataclass(frozen=True)
class ConsultarCitasAfectadas:
    medico_id: str; fecha: date; sucursal_id: str
@dataclass(frozen=True)
class ConsultarHistorialDeNoShows:
    expediente: str
@dataclass(frozen=True)
class ObtenerReporteConsolidado:
    desde: date; hasta: date
class QueryHandlers:
    def __init__(self,lector):self.lector=lector
    def consultar_disponibilidad(self,query):return self.lector.disponibilidad(query.medico_id,query.fecha)
    def consultar_citas_afectadas(self,query):return self.lector.citas_afectadas(query.medico_id,query.fecha,query.sucursal_id)
    def consultar_historial_no_shows(self,query):return self.lector.historial_no_shows(query.expediente)
    def obtener_reporte_consolidado(self,query):return self.lector.reporte(query.desde,query.hasta)
