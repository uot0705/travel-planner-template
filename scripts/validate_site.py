from __future__ import annotations

import argparse
from html import unescape
from pathlib import Path

from site_builder import DOCS_PATH, FORBIDDEN_PATTERNS, load_public_site, resolve_source_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the generated public summary site.")
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


def assert_contains(text: str, needle: str, context: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing '{needle}' in {context}")


def main() -> None:
    args = parse_args()
    site = load_public_site(resolve_source_path(args.source))
    output_dir = Path(args.output)
    index_path = output_dir / "index.html"
    style_path = output_dir / "assets" / "styles.css"
    nojekyll_path = output_dir / ".nojekyll"

    if not index_path.exists():
        raise AssertionError("docs/index.html was not generated")
    if not style_path.exists():
        raise AssertionError("docs/assets/styles.css was not generated")
    if not nojekyll_path.exists():
        raise AssertionError("docs/.nojekyll was not generated")

    text = unescape(index_path.read_text(encoding="utf-8"))
    assert_contains(text, site.title, str(index_path))
    assert_contains(text, site.tagline, str(index_path))
    assert_contains(text, site.description, str(index_path))
    assert_contains(text, site.footer_note, str(index_path))

    for fact in site.hero_facts:
        assert_contains(text, fact, str(index_path))
    for card in site.cards:
        assert_contains(text, card.label, str(index_path))
        assert_contains(text, card.title, str(index_path))
        assert_contains(text, card.text, str(index_path))
    for section in site.sections:
        assert_contains(text, section.title, str(index_path))
        for item in section.items:
            assert_contains(text, item, str(index_path))

    forbidden_html_tokens = [
        "airport-guide.html",
        "budget.html",
        "places/",
        "data-time-range",
        "予約番号",
        "航空券番号",
    ]
    for token in forbidden_html_tokens:
        if token in text:
            raise AssertionError(f"Forbidden token leaked into public HTML: {token}")

    for pattern, label in FORBIDDEN_PATTERNS:
        if pattern.search(text):
            raise AssertionError(f"Forbidden {label} leaked into public HTML")

    generated_files = sorted(path.relative_to(output_dir).as_posix() for path in output_dir.rglob("*") if path.is_file())
    expected_files = [".nojekyll", "assets/styles.css", "index.html"]
    if generated_files != expected_files:
        raise AssertionError(f"Unexpected files in public output: {generated_files}")

    print(f"Validated public summary site in {output_dir}")


if __name__ == "__main__":
    main()
