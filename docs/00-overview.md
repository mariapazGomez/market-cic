# 00 — Overview

## Objetivo
Tip Splitter es una aplicación web para calcular la distribución de propinas semanales en un restaurante a partir de una planilla Excel de turnos. El usuario carga el archivo, ingresa el monto total de propinas acumuladas y el sistema calcula automáticamente cuánto corresponde a cada trabajador según la cantidad de turnos realizados.

## Flujo del usuario (MVP)
1. Cargar archivo Excel (formato definido).
2. La app valida el archivo y genera un **preview** con turnos contados por persona.
3. El usuario ingresa `propina_total`.
4. La app calcula el reparto.
5. El usuario descarga un Excel con los resultados.

## Alcance (MVP)
- Soporta turnos: `AM`, `PM`, `FULL`, `-` (o vacío).
- Cuenta turnos por trabajador según reglas definidas.
- Calcula reparto proporcional por turnos.
- Exporta resultados a Excel.

## Fuera de alcance (por ahora)
- Login / multi-usuario.
- Historial de semanas.
- Gestión de trabajadores desde la app.
- Reglas avanzadas (ponderación por rol, horas, etc.).

## Glosario
- **Turno**: Unidad base de participación en el reparto (según regla).
- **Grilla semanal**: Tabla donde filas son trabajadores y columnas son días.
- **FULL**: Turno completo (definición en reglas de negocio).
