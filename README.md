# Long Task Utility

A small Python utility for processing CSV files.

## Installation

No external dependencies required. Uses only Python standard library.

## Usage

```python
from src.long_task import row_sums

# Compute row sums from a CSV file
sums = row_sums("data.csv")
print(sums)  # [6.0, 15.0]
```

## Running Tests

```bash
pytest tests/
```

## CSV Format

The CSV file should contain numeric values. Each row is summed independently.

Example `data.csv`:
```csv
1,2,3
4,5,6
```

Result: `[6.0, 15.0]`
