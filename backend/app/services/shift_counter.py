from __future__ import annotations

from typing import Dict, List, Tuple
import pandas as pd
from .validators import normalize_cell

SHIFT_WEIGHTS = {
    "AM": 1,
    "PM": 1,
    "FULL": 2,
    "-": 0,
}


def count_shifts(df: pd.DataFrame) -> Tuple[Dict[str, int], int]:
    """
    Count shifts per worker from the weekly grid.

    Expects columns: Nombre, Lun..Dom
    """
    day_cols = [c for c in ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"] if c in df.columns]

    per_worker: Dict[str, int] = {}
    total = 0

    for i in range(len(df)):
        name = normalize_cell(df.at[i, "Nombre"])
        if name in {"-", ""}:
            continue

        count = 0
        for col in day_cols:
            token = normalize_cell(df.at[i, col])
            count += SHIFT_WEIGHTS.get(token, 0)

        per_worker[name] = per_worker.get(name, 0) + count
        total += count

    return per_worker, total
