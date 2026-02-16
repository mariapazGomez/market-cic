from __future__ import annotations

from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field


DayCol = Literal["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]


class PreviewError(BaseModel):
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    row: Optional[int] = Field(None, description="1-based row number in the sheet (if applicable)")
    column: Optional[str] = Field(None, description="Column name (if applicable)")
    value: Optional[str] = Field(None, description="Offending value (if applicable)")


class WorkerPreview(BaseModel):
    nombre: str
    turnos: int


class PreviewResponse(BaseModel):
    ok: bool
    sheet_name: str = "PLANILLA_SEMANAL"
    turnos_totales: int = 0
    workers: List[WorkerPreview] = Field(default_factory=list)
    errors: List[PreviewError] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
