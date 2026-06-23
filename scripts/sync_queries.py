#!/usr/bin/env python3
"""Pull the SQL of every Dune query listed in queries.yml into queries/<id>.sql.

Dune is the source of truth: queries are authored on dune.com and this script
mirrors their SQL locally for version control. Requires a Dune API key in the
DUNE_API_KEY environment variable. Uses only the Python standard library.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERIES_YML = ROOT / "queries.yml"
OUT_DIR = ROOT / "queries"
API_URL = "https://api.dune.com/api/v1/query/{query_id}"


def load_query_ids(path: Path) -> list[int]:
    """Read the simple `- <id>` YAML list without a yaml dependency."""
    ids: list[int] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-"):
            line = line[1:].strip()
        if line.isdigit():
            ids.append(int(line))
    return ids


def fetch_query(query_id: int, api_key: str) -> dict:
    req = urllib.request.Request(
        API_URL.format(query_id=query_id),
        headers={"X-Dune-API-Key": api_key},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def main() -> int:
    api_key = os.environ.get("DUNE_API_KEY")
    if not api_key:
        print("ERROR: DUNE_API_KEY is not set.", file=sys.stderr)
        return 1

    ids = load_query_ids(QUERIES_YML)
    if not ids:
        print(f"No query IDs found in {QUERIES_YML}", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(exist_ok=True)
    failures = 0

    for query_id in ids:
        try:
            data = fetch_query(query_id, api_key)
        except urllib.error.HTTPError as exc:
            print(f"  {query_id}: HTTP {exc.code} {exc.reason}", file=sys.stderr)
            failures += 1
            continue
        except Exception as exc:  # noqa: BLE001
            print(f"  {query_id}: {exc}", file=sys.stderr)
            failures += 1
            continue

        name = data.get("name", "")
        sql = data.get("query_sql", "")
        header = (
            f"-- name: {name}\n"
            f"-- query_id: {query_id}\n"
            f"-- source: https://dune.com/queries/{query_id}\n"
            "-- Synced from Dune. Edit on Dune, then re-run scripts/sync_queries.py.\n\n"
        )
        out_path = OUT_DIR / f"{query_id}.sql"
        out_path.write_text(header + sql.rstrip() + "\n")
        print(f"  {query_id}: wrote {out_path.relative_to(ROOT)} ({name!r})")

    if failures:
        print(f"Done with {failures} failure(s).", file=sys.stderr)
        return 1
    print("All queries synced.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
