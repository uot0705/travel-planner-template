from __future__ import annotations

import argparse
from pathlib import Path

from site_builder import DOCS_PATH, build_site, load_public_site, resolve_source_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a public-safe travel summary site.")
    parser.add_argument(
        "source",
        nargs="?",
        help="Path to site.json or a trip directory containing public/site.json. Defaults to examples/public-demo/site.json.",
    )
    parser.add_argument(
        "--output",
        default=str(DOCS_PATH),
        help="Output directory. Defaults to docs/.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_path = resolve_source_path(args.source)
    site = load_public_site(source_path)
    build_site(site, output_dir=Path(args.output))
    print(f"Built public summary site from {source_path} into {Path(args.output)}")


if __name__ == "__main__":
    main()
