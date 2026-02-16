from __future__ import annotations

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from .models import PreviewResponse, PreviewError, WorkerPreview
from .services.excel_parser import load_weekly_sheet
from .services.validators import (
    REQUIRED_SHEET,
    validate_columns,
    validate_names,
    validate_cells,
    detect_duplicate_names,
)
from .services.shift_counter import count_shifts


app = FastAPI(
    title="Tip Splitter API",
    version="0.1.0",
)

# CORS (útil cuando conectes Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción limitar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/preview", response_model=PreviewResponse)
async def preview(file: UploadFile = File(...)):
    resp = PreviewResponse(ok=False, sheet_name=REQUIRED_SHEET)

    # Validate file type lightly
    if not file.filename.lower().endswith(".xlsx"):
        resp.errors.append(PreviewError(
            code="INVALID_FILE_TYPE",
            message="Formato inválido. Sube un archivo .xlsx",
        ))
        return resp

    file_bytes = await file.read()

    # Load sheet
    try:
        df = load_weekly_sheet(file_bytes)
    except ValueError as e:
        resp.errors.append(PreviewError(
            code="MISSING_SHEET",
            message=str(e),
        ))
        return resp

    # Validate structure + values
    errors = []
    errors += validate_columns(df)
    errors += validate_names(df)
    errors += validate_cells(df)

    for err in errors:
        resp.errors.append(PreviewError(**err))

    resp.warnings = detect_duplicate_names(df)

    # If any errors, stop here (no counting)
    if resp.errors:
        resp.ok = False
        return resp

    # Count shifts
    per_worker, total = count_shifts(df)

    resp.workers = [
        WorkerPreview(nombre=name, turnos=turnos)
        for name, turnos in sorted(per_worker.items(), key=lambda x: (-x[1], x[0]))
    ]
    resp.turnos_totales = total
    resp.ok = True

    # Edge case: no shifts at all
    if total == 0:
        resp.ok = False
        resp.errors.append(PreviewError(
            code="NO_SHIFTS",
            message="No se detectaron turnos para repartir.",
        ))

    return resp
