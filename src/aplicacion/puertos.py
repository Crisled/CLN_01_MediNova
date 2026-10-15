from abc import ABC,abstractmethod
from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True)
class ResultadoDeNotificacion:
    estado: str
    detalle: str = ''
class Notificador(ABC):
    @abstractmethod
    def notificar(self,evento) -> ResultadoDeNotificacion: ...
class Reloj(ABC):
    @abstractmethod
    def ahora(self) -> datetime: ...
class UnitOfWork(ABC):
    @abstractmethod
    def __enter__(self): ...
    @abstractmethod
    def __exit__(self,tipo,valor,traza): ...
    @abstractmethod
    def confirmar(self): ...
    @abstractmethod
    def deshacer(self): ...
