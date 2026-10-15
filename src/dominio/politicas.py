from abc import ABC,abstractmethod
from .paciente import Aseguradora
class PoliticaDeNoShow(ABC):
    @abstractmethod
    def evaluar(self, historial): ...
class SinSancionPorNoShow(PoliticaDeNoShow):
    def evaluar(self, historial): return None  # Dirección aún no define sanciones.
class PoliticaDeAutorizacion(ABC):
    @abstractmethod
    def requiere(self, aseguradora: Aseguradora | None) -> bool: ...
class AutorizacionPorCatalogo(PoliticaDeAutorizacion):
    def requiere(self, aseguradora): return bool(aseguradora and aseguradora.exige_autorizacion)
