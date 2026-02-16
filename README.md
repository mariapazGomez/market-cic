# 🍽️ Tip Splitter

Aplicación web para calcular la distribución de propinas semanales en un restaurante a partir de una planilla de turnos.

El usuario carga un archivo Excel con la planificación semanal, ingresa el monto total de propinas acumuladas y el sistema calcula automáticamente cuánto corresponde a cada trabajador según la cantidad de turnos realizados.

---

## ✨ Flujo principal

1. Subir archivo Excel con la grilla semanal.
2. Validar formato y detectar turnos.
3. Mostrar resumen de turnos por trabajador.
4. Ingresar propina total.
5. Calcular distribución.
6. Exportar resultados a Excel.

---

## 🧠 Regla principal del negocio

- Cada celda con `AM` = **1 turno**
- Cada celda con `PM` = **1 turno**
- Cada celda con `FULL` = **2 turnos**
- `-` o vacío = no se considera

---

## 📂 Formato esperado del Excel (resumen)

La hoja debe contener una grilla tipo calendario:

| Nombre | Lun | Mar | Mié | Jue | Vie | Sáb | Dom |
|--------|-----|-----|-----|-----|-----|-----|-----|
| Ana    | AM  | AM  | -   | PM  | PM  | -   | -   |

Más detalles en 👉 `/docs/01-excel-format.md`

---

## 🧩 Stack tecnológico

### Frontend
- Next.js
- React
- TypeScript

### Backend
- Python
- FastAPI
- pandas / openpyxl

---

## 🚀 Levantar el proyecto en local

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
### Frontend
```bash
cd frontend
npm install
npm run dev
```
