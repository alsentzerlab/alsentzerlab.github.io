#!/usr/bin/env python3
"""Refresh _bibliography/papers.bib from Emily Alsentzer's Google Scholar page."""

from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


AUTHOR_ID = "wKcw9Y8AAAAJ"
ROOT = Path(__file__).resolve().parents[1]
BIB_PATH = ROOT / "_bibliography" / "papers.bib"
OVERRIDES_PATH = ROOT / "_data" / "paper_overrides.yml"
SCHOLAR_URL = (
    "https://scholar.google.com/citations?"
    + urllib.parse.urlencode(
        {
            "hl": "en",
            "user": AUTHOR_ID,
            "view_op": "list_works",
            "sortby": "pubdate",
            "pagesize": "100",
        }
    )
)


@dataclass
class Paper:
    title: str
    authors: str
    venue: str
    year: str
    scholar: str
    google_scholar_id: str
    html: str = ""
    doi: str = ""
    key: str = ""


class ScholarHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.papers: list[Paper] = []
        self._in_row = False
        self._row: dict[str, str] = {}
        self._field: str | None = None
        self._gray_count = 0
        self._capture_depth = 0
        self._chunks: list[str] = []
        self._link_href = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        classes = set((attr.get("class") or "").split())

        if tag == "tr" and "gsc_a_tr" in classes:
            self._in_row = True
            self._row = {}
            self._gray_count = 0
            return

        if not self._in_row:
            return

        if tag == "a" and "gsc_a_at" in classes:
            self._begin_capture("title")
            self._link_href = attr.get("href") or ""
        elif tag == "div" and "gs_gray" in classes:
            self._gray_count += 1
            self._begin_capture("authors" if self._gray_count == 1 else "venue")
        elif tag == "span" and "gsc_a_h" in classes:
            self._begin_capture("year")
        elif self._field:
            self._capture_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self._field:
            self._capture_depth -= 1
            if self._capture_depth <= 0:
                text = html.unescape("".join(self._chunks))
                text = re.sub(r"\s+", " ", text).strip()
                self._row[self._field] = text
                if self._field == "title":
                    self._row["href"] = self._link_href
                self._field = None
                self._chunks = []
                self._capture_depth = 0
            return

        if tag == "tr" and self._in_row:
            paper = self._paper_from_row(self._row)
            if paper:
                self.papers.append(paper)
            self._in_row = False

    def handle_data(self, data: str) -> None:
        if self._field:
            self._chunks.append(data)

    def _begin_capture(self, field: str) -> None:
        self._field = field
        self._capture_depth = 1
        self._chunks = []

    @staticmethod
    def _paper_from_row(row: dict[str, str]) -> Paper | None:
        title = row.get("title", "").strip()
        if not title:
            return None

        href = row.get("href", "")
        scholar = urllib.parse.urljoin("https://scholar.google.com", href)
        parsed = urllib.parse.parse_qs(urllib.parse.urlparse(scholar).query)
        citation = parsed.get("citation_for_view", [""])[0]
        google_scholar_id = citation.split(":", 1)[1] if ":" in citation else ""

        venue = cleanup_venue(row.get("venue", ""))
        year = normalize_year(row.get("year", ""), venue)

        return Paper(
            title=title,
            authors=row.get("authors", "").strip(),
            venue=venue,
            year=year,
            scholar=scholar,
            google_scholar_id=google_scholar_id,
        )


def cleanup_venue(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r",\s*0$", "", value)
    return re.sub(r"\s+", " ", value).strip(" ,")


def normalize_year(value: str, venue: str) -> str:
    match = re.search(r"(19|20)\d{2}", value) or re.search(r"(19|20)\d{2}", venue)
    return match.group(0) if match else ""


def slugify(value: str) -> str:
    value = html.unescape(value).lower()
    value = re.sub(r"[^a-z0-9]+", " ", value).strip()
    words = value.split()
    stop = {"a", "an", "and", "for", "from", "in", "of", "on", "the", "to", "using", "with"}
    words = [word for word in words if word not in stop]
    return "".join(words[:3]) or "paper"


def first_author_last_name(authors: str) -> str:
    first = authors.split(",", 1)[0].strip()
    parts = re.findall(r"[A-Za-z]+", first)
    return (parts[-1] if parts else "paper").lower()


def bib_key(paper: Paper, used: set[str]) -> str:
    if paper.key and paper.key not in used:
        used.add(paper.key)
        return paper.key

    base = f"{first_author_last_name(paper.authors)}{paper.year}{slugify(paper.title)}"
    base = re.sub(r"[^A-Za-z0-9]+", "", base)
    key = base
    suffix = 2
    while key in used:
        key = f"{base}{suffix}"
        suffix += 1
    used.add(key)
    return key


def bibtex_escape(value: str) -> str:
    return (
        html.unescape(value)
        .replace("\\", "\\\\")
        .replace("{", "\\{")
        .replace("}", "\\}")
    )


def bibtex_authors(value: str) -> str:
    authors = value.replace("…", "...")
    authors = re.sub(r",?\s*\.\.\.$", ", others", authors)
    parts = [part.strip() for part in authors.split(",") if part.strip()]
    return " and ".join("others" if part == "others" else part for part in parts)


def venue_field(venue: str) -> tuple[str, str]:
    if re.search(r"\b(arxiv|preprint|proceedings|conference|workshop|symposium|neurips|iclr|ml4h|amia)\b", venue, re.I):
        return "booktitle", venue
    return "journal", venue


def arxiv_id(venue: str) -> str:
    match = re.search(r"arXiv(?: preprint| e-prints)?(?: arXiv:|:)?\s*([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", venue, re.I)
    return match.group(1) if match else ""


def normalize_title(value: str) -> str:
    value = html.unescape(value).lower()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def load_overrides(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}

    overrides: dict[str, dict[str, str]] = {}
    current: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not raw_line.startswith(" ") and line.endswith(":"):
            current = line[:-1].strip().strip('"\'')
            overrides[current] = {}
        elif current and ":" in line:
            field, value = line.split(":", 1)
            overrides[current][field.strip()] = value.strip().strip('"\'')
    return overrides


def fetch_scholar_html() -> str:
    return fetch_url(SCHOLAR_URL)


def fetch_url(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_papers() -> list[Paper]:
    parser = ScholarHTMLParser()
    parser.feed(fetch_scholar_html())
    for paper in parser.papers:
        details = fetch_detail_metadata(paper.scholar)
        if details.get("authors") and ("..." in paper.authors or "…" in paper.authors):
            paper.authors = details["authors"]
        if details.get("html"):
            paper.html = details["html"]
        time.sleep(0.2)
    enrich_with_crossref(parser.papers)
    return parser.papers


def fetch_detail_metadata(url: str) -> dict[str, str]:
    try:
        page = fetch_url(url)
    except Exception as error:
        print(f"Warning: could not fetch paper details for {url}: {error}", file=sys.stderr)
        return {}

    details: dict[str, str] = {}

    authors_match = re.search(
        r'<div class="gsc_oci_field">\s*Authors\s*</div>\s*<div class="gsc_oci_value">(.*?)</div>',
        page,
        flags=re.S,
    )
    if authors_match:
        authors = re.sub(r"<[^>]+>", "", authors_match.group(1))
        authors = html.unescape(authors)
        details["authors"] = re.sub(r"\s+", " ", authors).strip()

    title_link_match = re.search(
        r'<div id="gsc_oci_title">\s*<a[^>]+href="([^"]+)"',
        page,
        flags=re.S,
    )
    if title_link_match:
        details["html"] = html.unescape(title_link_match.group(1))

    return details


def enrich_with_crossref(papers: list[Paper]) -> None:
    for paper in papers:
        if paper.doi or paper.html or arxiv_id(paper.venue):
            continue
        metadata = fetch_crossref_metadata(paper.title)
        if not metadata:
            continue
        paper.doi = metadata.get("doi", "")
        paper.html = metadata.get("html", "")
        time.sleep(0.1)


def fetch_crossref_metadata(title: str) -> dict[str, str]:
    params = urllib.parse.urlencode({"query.title": title, "rows": "5"})
    url = f"https://api.crossref.org/works?{params}"
    try:
        data = json.loads(fetch_url(url))
    except Exception as error:
        print(f"Warning: could not query Crossref for {title!r}: {error}", file=sys.stderr)
        return {}

    target = normalize_title(title)
    for item in data.get("message", {}).get("items", []):
        candidate_title = (item.get("title") or [""])[0]
        if normalize_title(candidate_title) != target:
            continue
        doi = item.get("DOI", "").strip()
        if not doi:
            return {}
        return {
            "doi": doi,
            "html": item.get("resource", {}).get("primary", {}).get("URL", "").strip() or f"https://doi.org/{doi}",
        }
    return {}


def parse_existing_bibtex(path: Path) -> list[Paper]:
    if not path.exists():
        return []

    papers: list[Paper] = []
    content = path.read_text(encoding="utf-8")
    for match in re.finditer(r"@(\w+)\{([^,]+),\s*(.*?)\n\}", content, flags=re.S):
        key = match.group(2).strip()
        body = match.group(3)
        fields = dict(re.findall(r"^\s*(\w+)=\{(.*?)\},?\s*$", body, flags=re.M | re.S))
        title = fields.get("title", "").strip()
        if not title:
            continue
        papers.append(
            Paper(
                title=title,
                authors=fields.get("author", "").replace(" and ", ", ").strip(),
                venue=fields.get("journal", fields.get("booktitle", "")).strip(),
                year=fields.get("year", "").strip(),
                scholar=fields.get("scholar", "").strip(),
                google_scholar_id=fields.get("google_scholar_id", "").strip(),
                html=fields.get("html", "").strip(),
                doi=fields.get("doi", "").strip(),
                key=key,
            )
        )
    return papers


def render_bibtex(papers: list[Paper], overrides: dict[str, dict[str, str]]) -> str:
    lines = [
        "---",
        "---",
        "",
        "% This file is generated by scripts/update_papers_from_scholar.py.",
        "% Add site-specific corrections, links, and display metadata in _data/paper_overrides.yml.",
        "",
    ]
    used: set[str] = set()
    for paper in papers:
        if not paper.year:
            continue
        key = bib_key(paper, used)
        override = overrides.get(key, {})
        if override.get("exclude", "").lower() in {"true", "yes", "1"}:
            continue
        entry_type = "inproceedings" if venue_field(paper.venue)[0] == "booktitle" else "article"
        venue_name, venue_value = venue_field(paper.venue)
        fields: list[tuple[str, str]] = [
            ("title", paper.title),
            ("author", bibtex_authors(paper.authors)),
            ("year", paper.year),
        ]
        if venue_value:
            fields.append((venue_name, venue_value))
        fields.append(("scholar", paper.scholar))
        if paper.html:
            fields.append(("html", paper.html))
        if paper.doi:
            fields.append(("doi", paper.doi))
        if paper.google_scholar_id:
            fields.append(("google_scholar_id", paper.google_scholar_id))
        arxiv = arxiv_id(paper.venue)
        if arxiv:
            fields.append(("arxiv", arxiv))
        used_field_names = {name for name, _value in fields}
        for name in (
            "author",
            "journal",
            "booktitle",
            "abbr",
            "pdf",
            "code",
            "website",
            "preview",
            "selected",
            "bibtex_show",
            "doi",
            "html",
            "arxiv",
        ):
            if name in override and override[name] != "":
                if name in used_field_names:
                    fields = [(field, override[name] if field == name else value) for field, value in fields]
                    continue
                fields.append((name, override[name]))

        lines.append(f"@{entry_type}{{{key},")
        for index, (name, value) in enumerate(fields):
            comma = "," if index < len(fields) - 1 else ""
            lines.append(f"  {name}={{{bibtex_escape(value)}}}{comma}")
        lines.append("}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    overrides = load_overrides(OVERRIDES_PATH)
    try:
        papers = fetch_papers()
    except Exception as error:
        print(f"Warning: Google Scholar refresh failed; enriching existing BibTeX instead: {error}", file=sys.stderr)
        papers = parse_existing_bibtex(BIB_PATH)
        enrich_with_crossref(papers)
    if not papers:
        print("No papers found. Google Scholar may have blocked the request.", file=sys.stderr)
        return 1

    dated_papers = [paper for paper in papers if paper.year]
    BIB_PATH.write_text(render_bibtex(dated_papers, overrides), encoding="utf-8")
    skipped = len(papers) - len(dated_papers)
    suffix = f" ({skipped} undated Scholar rows skipped)" if skipped else ""
    print(f"Wrote {len(dated_papers)} papers to {BIB_PATH.relative_to(ROOT)}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
