from __future__ import annotations

from typing import List, Dict, Set, Tuple, Optional
import pandas as pd

REQUIRED_SHEET = "PLANILLA_SEMANAL"
REQUIRED_COLUMNS = ["Nombre", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

ALLOWED_VALUES = {"AM", "PM", "FULL", "-", ""}


def normalize_cell(value) -> str:
    """Normalize cell values to uppercase tokens."""
    if value is None:
        return "-"
    if isinstance(value, float) and pd.isna(value):
        return "-"
    s = str(value).strip()
    if s == "":
        return "-"
    s = s.upper()
    # Normalize some common user variants
    if s in {"—", "–", "NA", "N/A"}:
        return "-"
    return s


def validate_columns(df: pd.DataFrame) -> List[Dict]:
    errors: List[Dict] = []
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            errors.append({
                "code": "MISSING_COLUMN",
                "message": f"Falta la columna: {col}",
                "row": None,
                "column": col,
                "value": None,
            })
    return errors


def validate_names(df: pd.DataFrame) -> List[Dict]:
    errors: List[Dict] = []
    if "Nombre" not in df.columns:
        return errors

    # 1-based row numbers: header is row 1, first data row is row 2
    for i, raw in enumerate(df["Nombre"].tolist()):
        row_num = i + 2
        name = normalize_cell(raw)
        if name == "-" or name == "":
            errors.append({
                "code": "EMPTY_NAME",
                "message": "Nombre vacío",
                "row": row_num,
                "column": "Nombre",
                "value": None,
            })
    return errors


def validate_cells(df: pd.DataFrame) -> List[Dict]:
    errors: List[Dict] = []
    day_cols = [c for c in REQUIRED_COLUMNS if c != "Nombre" and c in df.columns]

    for i in range(len(df)):
        row_num = i + 2
        for col in day_cols:
            v = normalize_cell(df.at[i, col])
            if v not in {"AM", "PM", "FULL", "-"}:
                errors.append({
                    "code": "INVALID_SHIFT_VALUE",
                    "message": f'Valor inválido "{v}" (usa AM/PM/FULL/-)',
                    "row": row_num,
                    "column": col,
                    "value": v,
                })
    return errors


def detect_duplicate_names(df: pd.DataFrame) -> List[str]:
    """Return warnings for duplicated normalized names."""
    if "Nombre" not in df.columns:
        return []
    names = [normalize_cell(x) for x in df["Nombre"].tolist()]
    names = [n for n in names if n not in {"-", ""}]
    duplicates = sorted({n for n in names if names.count(n) > 1})
    if duplicates:
        return [f'Nombre duplicado detectado: "{d}"' for d in duplicates]
    return []
