from datetime import datetime,timezone
from src.aplicacion.puertos import Reloj
class RelojSistema(Reloj):
    def ahora(self):return datetime.now(timezone.utc)
