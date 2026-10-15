# MediNova — Arquitectura en Python (Unidad 3)

Implementación de referencia para **agendar, atender y cerrar citas médicas** en tres sucursales, siguiendo el informe adjunto de arquitectura (secciones 2–6, 9 y 11).

## Estructura
- `src/dominio/`: Aggregate `AgendaMedica` por médico y fecha, entidades, Value Objects, eventos, políticas y repositorios abstractos.
- `src/aplicacion/`: Commands, servicios de casos de uso, Queries y puertos.
- `src/infraestructura/`: adaptadores en memoria, Unit of Work, reloj, notificador y lectores; contratos SQL preparados como puntos de extensión.
- `tests/`: pruebas T1–T8 de la sección 11.

## Requisitos y pruebas
Python 3.10+ y `pytest`.

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

Ejecutar desde la raíz del proyecto.

## Lectura recomendada
1. Informe de arquitectura (PDF proporcionado por el equipo).
2. Diagramas de las secciones 3 y 8 del informe.
3. ADR-001 a ADR-005 (sección 9).
4. Matriz de trazabilidad (sección 11).
5. Código fuente y pruebas T1–T8.

## Decisiones y límites
- El dominio no importa infraestructura. `AgendaMedica` protege horarios entre sucursales y sobrecupo.
- Auditoría de cancelación/modificación se registra en la misma transacción en memoria; notificaciones ocurren tras confirmar.
- Política de no-show **sin sanciones** mientras la dirección no la defina. Autorización basada en catálogo.
- SQL y API real de WhatsApp **no están implementados**: son adaptadores explícitos pendientes de conexión, sin credenciales ni servidor inventados.
- La implementación en memoria es demostrativa; para concurrencia real multiproceso se necesita SQL con control de versión atómico.
- El informe deja pendientes las reglas de autorización por convenio y ciertos escenarios de cancelación de jornada.

**Integrantes:** pendiente de completar por el equipo.
