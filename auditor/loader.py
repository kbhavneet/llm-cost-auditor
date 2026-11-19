"""Load LLM usage records from a JSONL file."""

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
