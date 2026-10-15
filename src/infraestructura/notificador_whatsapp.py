from src.aplicacion.puertos import Notificador,ResultadoDeNotificacion
class NotificadorWhatsApp(Notificador):
    """Puerto sin credenciales: se deja pendiente para recepción, sin inventar envíos."""
    def notificar(self,evento):
        return ResultadoDeNotificacion('pendiente_gestion_manual','Integración WhatsApp no configurada')
