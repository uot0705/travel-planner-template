from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS_PATH = ROOT / "docs"
SITE_SRC_PATH = ROOT / "site_src"
DEFAULT_PUBLIC_SITE_PATH = ROOT / "examples" / "public-demo" / "site.json"

FORBIDDEN_PATTERNS = [
    (re.compile(r"\b20\d{2}[-/]\d{1,2}[-/]\d{1,2}\b"), "specific date"),
    (re.compile(r"\b\d{1,2}:\d{2}\b"), "specific time"),
    (re.compile(r"\b\d{2,4}-\d{2,4}-\d{3,4}\b"), "phone number"),
    (re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE), "email"),
    (
        re.compile(
            r"(予約番号|航空券番号|旅券番号|booking number|booking ref|ticket number|pnr|e-ticket|passport number)",
            re.IGNORECASE,
        ),
        "sensitive travel identifier",
    ),
]


@dataclass(frozen=True)
class SiteCard:
    label: str
    title: str
    text: str


@dataclass(frozen=True)
class SiteSection:
    id: str
    title: str
    items: list[str]


@dataclass(frozen=True)
class PublicSite:
    title: str
    badge: str
    tagline: str
    description: str
    hero_facts: list[str]
    cards: list[SiteCard]
    sections: list[SiteSection]
    footer_note: str


def resolve_source_path(raw_path: str | None) -> Path:
    if not raw_path:
        return DEFAULT_PUBLIC_SITE_PATH

    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate

    if candidate.is_dir():
        direct = candidate / "site.json"
        nested = candidate / "public" / "site.json"
        if direct.exists():
            return direct
        if nested.exists():
            return nested
        raise FileNotFoundError(f"Could not find site.json under {candidate}")

    return candidate


def load_public_site(source_path: str | Path | None = None) -> PublicSite:
    path = resolve_source_path(str(source_path) if source_path else None)
    payload = json.loads(path.read_text(encoding="utf-8"))
    site = payload.get("site")
    if not isinstance(site, dict):
        raise ValueError("site.json must contain a 'site' object")

    public_site = PublicSite(
        title=require_string(site, "title"),
        badge=optional_string(site, "badge", default="Travel Summary"),
        tagline=require_string(site, "tagline"),
        description=require_string(site, "description"),
        hero_facts=require_string_list(payload, "hero_facts", min_items=1, max_items=6),
        cards=load_cards(payload),
        sections=load_sections(payload),
        footer_note=require_string(payload, "footer_note"),
    )

    validate_public_site(public_site)
    return public_site


def require_string(container: dict[str, Any], key: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"'{key}' must be a non-empty string")
    return value.strip()


def optional_string(container: dict[str, Any], key: str, *, default: str) -> str:
    value = container.get(key, default)
    if not isinstance(value, str):
        raise ValueError(f"'{key}' must be a string")
    return value.strip() or default


def require_string_list(
    container: dict[str, Any],
    key: str,
    *,
    min_items: int = 1,
    max_items: int | None = None,
) -> list[str]:
    value = container.get(key)
    if not isinstance(value, list):
        raise ValueError(f"'{key}' must be a list")

    cleaned: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"'{key}' must contain non-empty strings only")
        cleaned.append(item.strip())

    if len(cleaned) < min_items:
        raise ValueError(f"'{key}' must contain at least {min_items} item(s)")
    if max_items is not None and len(cleaned) > max_items:
        raise ValueError(f"'{key}' must contain at most {max_items} item(s)")
    return cleaned


def load_cards(payload: dict[str, Any]) -> list[SiteCard]:
    raw_cards = payload.get("cards")
    if not isinstance(raw_cards, list) or not raw_cards:
        raise ValueError("'cards' must be a non-empty list")
    if not 3 <= len(raw_cards) <= 6:
        raise ValueError("'cards' must contain between 3 and 6 items")

    cards: list[SiteCard] = []
    for index, raw_card in enumerate(raw_cards, start=1):
        if not isinstance(raw_card, dict):
            raise ValueError(f"cards[{index}] must be an object")
        cards.append(
            SiteCard(
                label=require_string(raw_card, "label"),
                title=require_string(raw_card, "title"),
                text=require_string(raw_card, "text"),
            )
        )
    return cards


def load_sections(payload: dict[str, Any]) -> list[SiteSection]:
    raw_sections = payload.get("sections")
    if not isinstance(raw_sections, list) or not raw_sections:
        raise ValueError("'sections' must be a non-empty list")
    if not 1 <= len(raw_sections) <= 4:
        raise ValueError("'sections' must contain between 1 and 4 items")

    sections: list[SiteSection] = []
    for index, raw_section in enumerate(raw_sections, start=1):
        if not isinstance(raw_section, dict):
            raise ValueError(f"sections[{index}] must be an object")

        title = require_string(raw_section, "title")
        section_id = optional_string(raw_section, "id", default=slugify(title))
        items = require_string_list(raw_section, "items", min_items=1, max_items=6)
        sections.append(SiteSection(id=slugify(section_id), title=title, items=items))
    return sections


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "section"


def validate_public_site(site: PublicSite) -> None:
    for text in iter_site_strings(site):
        validate_public_text(text)


def iter_site_strings(site: PublicSite) -> list[str]:
    values = [site.title, site.badge, site.tagline, site.description, site.footer_note]
    values.extend(site.hero_facts)
    for card in site.cards:
        values.extend([card.label, card.title, card.text])
    for section in site.sections:
        values.append(section.title)
        values.extend(section.items)
    return values


def validate_public_text(text: str) -> None:
    stripped = text.strip()
    if not stripped:
        raise ValueError("Public text entries must not be empty")
    if len(stripped) > 180:
        raise ValueError(f"Public text is too long for a summary page: {stripped[:40]}...")

    for pattern, label in FORBIDDEN_PATTERNS:
        if pattern.search(stripped):
            raise ValueError(f"Public site text contains a forbidden {label}: {stripped}")


def build_site(site: PublicSite, *, output_dir: Path = DOCS_PATH) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)

    assets_path = output_dir / "assets"
    output_dir.mkdir(parents=True, exist_ok=True)
    assets_path.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SITE_SRC_PATH / "styles.css", assets_path / "styles.css")
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")
    (output_dir / "index.html").write_text(render_index(site), encoding="utf-8")


def render_index(site: PublicSite) -> str:
    section_links = "".join(
        f'<a class="chip" href="#{escape(section.id)}">{escape(section.title)}</a>'
        for section in site.sections
    )
    hero_facts = "".join(f"<li>{escape(item)}</li>" for item in site.hero_facts)
    cards = "".join(
        f"""
        <article class="summary-card">
          <p class="card-label">{escape(card.label)}</p>
          <h2>{escape(card.title)}</h2>
          <p>{escape(card.text)}</p>
        </article>
        """
        for card in site.cards
    )
    sections = "".join(render_section(section) for section in site.sections)

    body = f"""
<main class="site-shell">
  <section class="hero">
    <p class="eyebrow">{escape(site.badge)}</p>
    <h1>{escape(site.title)}</h1>
    <p class="hero-tagline">{escape(site.tagline)}</p>
    <p class="hero-copy">{escape(site.description)}</p>
    <ul class="hero-facts" aria-label="summary facts">
      {hero_facts}
    </ul>
  </section>

  <nav class="chip-row" aria-label="page sections">
    {section_links}
  </nav>

  <section class="card-grid" aria-label="summary cards">
    {cards}
  </section>

  <section class="section-stack">
    {sections}
  </section>

  <section class="note-card" aria-label="publication note">
    <h2>Publication Note</h2>
    <p>{escape(site.footer_note)}</p>
  </section>
</main>
"""

    return wrap_page(site.title, body)


def render_section(section: SiteSection) -> str:
    items = "".join(f"<li>{escape(item)}</li>" for item in section.items)
    return f"""
  <section class="section-card" id="{escape(section.id)}">
    <h2>{escape(section.title)}</h2>
    <ul class="bullet-list">
      {items}
    </ul>
  </section>
"""


def wrap_page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{escape(title)}</title>
    <meta
      name="description"
      content="Public-safe travel summary template. No personal details, booking data, or timed itinerary."
    />
    <link rel="stylesheet" href="assets/styles.css" />
  </head>
  <body>
    {body}
  </body>
</html>
"""
