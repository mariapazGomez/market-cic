from __future__ import annotations

from typing import Dict
import pandas as pd

from .validators import REQUIRED_SHEET


def load_weekly_sheet(file_bytes: bytes) -> pd.DataFrame:
    """
    Load the PLANILLA_SEMANAL sheet from an uploaded xlsx file.
    Raises ValueError if sheet not found.
    """
    xls = pd.ExcelFile(file_bytes)
    if REQUIRED_SHEET not in xls.sheet_names:
        raise ValueError(f"No se encontró la hoja {REQUIRED_SHEET}")
    df = pd.read_excel(file_bytes, sheet_name=REQUIRED_SHEET, dtype=object)
    # Keep original columns; downstream validators handle missing columns
    return df
