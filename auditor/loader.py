"""Read the log one line at a time so large files dont need to fit in
memory. Blank lines are skipped entirely. Broken JSON and non-object
lines are skipped with a warning that includes the line number. A
missing file raises a clear FileNotFoundError instead of failing
somewhere inside open()."""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def load_records(path: str | Path) -> list[dict]:
    """Read a JSONL file and return one dict per valid line.

    - Blank lines are skipped
    - Lines with broken JSON are skipped with a warning (including line number).
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Log file not found: {path.resolve()}")

    records: list[dict] = []

    with path.open(encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip() 

            if not line:
                continue

            try:
                record = json.loads(line)  # loads = load from a String
            except json.JSONDecodeError as err:
                logger.warning(
                    "Skipping line %d: invalid JSON (%s)", line_number, err.msg
                )
                continue

            if not isinstance(record, dict):
                logger.warning(
                    "Skipping line %d: expected a JSON object, got %s",
                    line_number,
                    type(record).__name__,
                )
                continue

            records.append(record)

    logger.info("Loaded %d records from %s", len(records), path.name)
    return records

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    records = load_records("data/sample_usage.jsonl")
    print(f"Loaded {len(records)} records")
