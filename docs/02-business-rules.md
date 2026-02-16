# 02 — Reglas de negocio

## Objetivo
Definir exactamente cómo se cuentan turnos y cómo se calcula el reparto de propinas para garantizar consistencia.

---

## Conteo de turnos
Cada celda válida se transforma en “turnos contables”:

- `AM` = 1 turno
- `PM` = 1 turno
- `FULL` = 2 turnos
- `-` o vacío = 0 turnos

> Nota: `FULL = 2` es la configuración base del MVP. Si esto cambia, debe registrarse en un ADR.

---

## Cálculo del reparto
Inputs:
- `propina_total` (número entero, moneda local)
- `turnos_por_trabajador` (resultado del conteo)

Pasos:
1. `turnos_totales = sum(turnos_por_trabajador)`
2. `valor_por_turno = propina_total / turnos_totales`
3. `propina_trabajador = turnos_trabajador * valor_por_turno`

---

## Redondeo (MVP)
En el MVP:
- Se calcula con decimales internamente.
- La salida final se redondea a entero (moneda) usando redondeo estándar.

> Mejora futura: permitir elegir regla de redondeo (a $10, $100, etc.) y ajustar el remanente.

---

## Casos borde
- Si `turnos_totales = 0` → error: no hay turnos para repartir.
- Si `propina_total < 0` → error: no permitido.
- Si existe un trabajador con 0 turnos → aparece con 0 propina (si se decide mostrarlo) o se omite (decisión de UI).

---

## Salidas esperadas (MVP)
Tabla final por trabajador:
- Nombre
- Turnos (contables)
- % del total de turnos (opcional)
- Propina asignada
