import csv
from pathlib import Path

import pytest

from src.long_task import row_sums


def test_row_sums_basic(tmp_path: Path) -> None:
    csv_file = tmp_path / "data.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([1, 2, 3])
        writer.writerow([4, 5, 6])

    result = row_sums(csv_file)
    assert result == [6.0, 15.0]


def test_row_sums_empty_file(tmp_path: Path) -> None:
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")

    result = row_sums(csv_file)
    assert result == []


def test_row_sums_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        row_sums("nonexistent.csv")


def test_row_sums_non_numeric(tmp_path: Path) -> None:
    csv_file = tmp_path / "bad.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([1, "abc", 3])

    with pytest.raises(ValueError):
        row_sums(csv_file)
