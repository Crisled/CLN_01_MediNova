from dataclasses import dataclass, field
from datetime import date, datetime
from .cita import Cita, EstadoCita
from .jornada import Jornada
from .value_objects import (HorarioNoDisponible, SobrecupoExcedido, FranjaFueraDeJornada,
                             CitaNoEncontrada, TransicionDeEstatusInvalida, Tolerancia)
from . import eventos as e
@dataclass
class AgendaMedica:
    medico_id: str
    fecha: date
    jornadas: list[Jornada] = field(default_factory=list)
    citas: list[Cita] = field(default_factory=list)
    version: int = 0
    eventos: list[e.Evento] = field(default_factory=list, repr=False)
    def obtener_cita(self, cita_id):
        for cita in self.citas:
            if cita.id == cita_id: return cita
        raise CitaNoEncontrada(cita_id)
    def agendar(self, cita: Cita, limite_sobrecupo=0):
        if cita.medico_id != self.medico_id or cita.franja.inicio.date() != self.fecha:
            raise FranjaFueraDeJornada('Médico o fecha incorrectos')
        if not any(j.sucursal_id == cita.sucursal_id and j.contiene(cita.franja) for j in self.jornadas):
            raise FranjaFueraDeJornada('Franja fuera de jornada vigente')
        if any(c.id == cita.id for c in self.citas): raise HorarioNoDisponible('Identificador repetido')
        ocupadas = sum(c.bloquea_franja and c.franja.se_solapa(cita.franja) for c in self.citas)
        if ocupadas and limite_sobrecupo == 0: raise HorarioNoDisponible('Horario ocupado en alguna sucursal')
        if ocupadas >= 1 + limite_sobrecupo: raise SobrecupoExcedido('Límite de sobrecupo excedido')
        self.citas.append(cita)
        self.eventos.append(e.CitaAgendada(cita.id))
        return cita
    def cancelar(self, cita_id, usuario, motivo):
        cita=self.obtener_cita(cita_id); cita.transicionar(EstadoCita.CANCELADA)
        self.eventos.append(e.CitaCancelada(cita_id,usuario,motivo))
        return cita
    def modificar(self,cita_id,nueva_franja,nueva_sucursal,limite,usuario,motivo):
        original=self.obtener_cita(cita_id)
        if original.estado != EstadoCita.AGENDADA: raise TransicionDeEstatusInvalida('Solo citas agendadas')
        self.citas.remove(original)
        from dataclasses import replace
        nueva=replace(original,franja=nueva_franja,sucursal_id=nueva_sucursal)
        try: self.agendar(nueva,limite)
        except Exception:
            self.citas.append(original); raise
        self.eventos.pop()  # Se emite modificación, no nueva cita.
        self.eventos.append(e.CitaModificada(cita_id,usuario,motivo))
        return nueva
    def registrar_llegada(self,cita_id,ahora):
        cita=self.obtener_cita(cita_id)
        if cita.estado != EstadoCita.AGENDADA: raise TransicionDeEstatusInvalida('La cita no está agendada')
        resultado=Tolerancia().evaluar(cita.franja.inicio,ahora)
        if resultado == 'no_atendida_por_retraso':
            cita.transicionar(EstadoCita.NO_ATENDIDA_POR_RETRASO)
            self.eventos.append(e.CitaNoAtendidaPorRetraso(cita_id))
        else:
            cita.transicionar(EstadoCita.PRESENTE); cita.llegada=ahora
            self.eventos.append(e.LlegadaRegistrada(cita_id))
        return resultado
    def marcar_no_atendida_por_retraso(self,cita_id):
        cita=self.obtener_cita(cita_id); cita.transicionar(EstadoCita.NO_ATENDIDA_POR_RETRASO)
        self.eventos.append(e.CitaNoAtendidaPorRetraso(cita_id))
    def marcar_no_show(self,cita_id,ahora):
        cita=self.obtener_cita(cita_id)
        if cita.estado != EstadoCita.AGENDADA or ahora <= cita.franja.inicio:
            raise TransicionDeEstatusInvalida('Solo una cita agendada cuya hora pasó')
        cita.transicionar(EstadoCita.NO_SHOW)
        self.eventos.append(e.CitaMarcadaComoNoShow(cita_id))
    def cerrar_consulta(self,cita_id):
        cita=self.obtener_cita(cita_id); cita.transicionar(EstadoCita.ATENDIDA)
        self.eventos.append(e.ConsultaCerrada(cita_id))
    def cancelar_jornada(self,sucursal_id,usuario,motivo):
        jornadas=[j for j in self.jornadas if j.sucursal_id == sucursal_id and not j.cancelada]
        if not jornadas: raise FranjaFueraDeJornada('No hay jornada vigente')
        for j in jornadas: j.cancelada=True
        afectadas=[]
        for c in self.citas:
            if c.sucursal_id == sucursal_id and c.estado == EstadoCita.AGENDADA:
                c.transicionar(EstadoCita.AFECTADA); afectadas.append(c)
        self.eventos.append(e.JornadaCancelada(None,usuario,motivo))
        return afectadas
