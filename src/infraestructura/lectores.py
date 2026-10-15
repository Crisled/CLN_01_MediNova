from collections import Counter
from src.dominio.cita import EstadoCita
class LectoresMemoria:
    """CQRS de lectura: proyecciones directas, sin cambiar Aggregates."""
    def __init__(self,almacen):self.almacen=almacen
    def disponibilidad(self,medico_id,fecha):
        agenda=self.almacen.agendas.get((medico_id,fecha))
        return {'medico_id':medico_id,'fecha':fecha.isoformat(),'jornadas':[
            {'sucursal':j.sucursal_id,'inicio':j.franja.inicio.isoformat(),'fin':j.franja.fin.isoformat(),'cancelada':j.cancelada}
            for j in (agenda.jornadas if agenda else [])],
            'citas':[{'franja':c.franja.inicio.isoformat(),'sucursal':c.sucursal_id,'estado':c.estado.value}
                     for c in (agenda.citas if agenda else []) if c.bloquea_franja]}
    def citas_afectadas(self,medico_id,fecha,sucursal_id):
        agenda=self.almacen.agendas.get((medico_id,fecha))
        if not agenda:return []
        resultado=[]
        for c in agenda.citas:
            if c.sucursal_id==sucursal_id and c.estado==EstadoCita.AFECTADA:
                paciente=self.almacen.pacientes.get(c.expediente)
                vinculadas=any(n.cita_origen_id==c.id for a in self.almacen.agendas.values() for n in a.citas)
                resultado.append({'cita_id':c.id,'nombre':paciente.nombre if paciente else '',
                    'telefono':paciente.contacto.telefono if paciente else '',
                    'correo':paciente.contacto.correo if paciente else '',
                    'hora_original':c.franja.inicio.isoformat(),'reagendado':'reagendada' if vinculadas else 'pendiente'})
        return resultado
    def historial_no_shows(self,expediente):
        fechas=[c.franja.inicio.isoformat() for a in self.almacen.agendas.values() for c in a.citas
                if c.expediente==expediente and c.estado==EstadoCita.NO_SHOW]
        paciente=self.almacen.pacientes.get(expediente)
        return {'expediente':expediente,'nombre':paciente.nombre if paciente else '', 'total':len(fechas),'fechas':fechas}
    def reporte(self,desde,hasta):
        conteos=Counter()
        for a in self.almacen.agendas.values():
            if desde<=a.fecha<=hasta:
                for c in a.citas:conteos[(c.sucursal_id,a.medico_id,c.estado.value)]+=1
        return [{'sucursal':s,'medico':m,'estatus':e,'total':n} for (s,m,e),n in sorted(conteos.items())]
class LectoresSql:
    def __init__(self,conexion):self.conexion=conexion
    def __getattr__(self,nombre):
        if nombre in ('disponibilidad','citas_afectadas','historial_no_shows','reporte'):
            raise NotImplementedError('Proyección SQL pendiente de integración')
        raise AttributeError(nombre)
