from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates" / "trip-template"
TRIPS_DIR = ROOT / "trips"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "new-trip"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new private trip workspace from the template.")
    parser.add_argument("trip_id", help="Trip id such as fukuoka-2026-09")
    parser.add_argument("--force", action="store_true", help="Replace the destination if it already exists.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    trip_id = slugify(args.trip_id)
    destination = TRIPS_DIR / trip_id

    if destination.exists():
        if not args.force:
            raise SystemExit(f"{destination} already exists. Use --force to replace it.")
        shutil.rmtree(destination)

    shutil.copytree(TEMPLATE_DIR, destination)
    print(destination)


if __name__ == "__main__":
    main()
