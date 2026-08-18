"""Long task utility for processing CSV files."""

import csv
from pathlib import Path
from typing import List, Union


def row_sums(csv_path: Union[str, Path]) -> List[float]:
    """Compute the sum of each row in a CSV file.

    Args:
        csv_path: Path to the CSV file.

    Returns:
        A list of floats representing the sum of each row.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If a row contains non-numeric values.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    sums: List[float] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            try:
                values = [float(v) for v in row]
            except ValueError as exc:
                raise ValueError(f"Non-numeric value in row: {row}") from exc
            sums.append(sum(values))
    return sums
