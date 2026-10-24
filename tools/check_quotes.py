#!/usr/bin/env python3
"""Check an answer against the grounded-expert output contract (the <output-contract> block in plugin/SKILL.md).

Usage:
  check_quotes.py ANSWER [--fixtures DIR] [--skill FILE]   (ANSWER: a file with the final answer, or - for stdin)
  check_quotes.py --self-test
Exit: 0 no INVALID (UNVERIFIED is allowed), 1 at least one INVALID, 2 usage or input error. Stdlib only.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
HEADER = "| # | Claim | Tag | Quote | Source | URL |"
FLOOR = {"quick": 1, "standard": 2, "thorough": 2}  # keep in step with step 3 item 2 of SKILL.md
LABELS = ("direct answer — no independent subagent", "not externally verified", "partial cross-check")
LAST = re.compile(r"Disconfirming search: (found — https?://\S+|ran — nothing opposing found|not run \(quick\))")
TAG_VIA = re.compile(r"INFERRED \(via ([^()\s]+)\)")
TAG_FIG = re.compile(r"INFERRED \(figure ([^()\s]+)\)")
URL_RE = re.compile(r"https?://[^\s\\]+")  # no backslash: WHATWG parsers end the host there, urlsplit does not
DELIM = re.compile(r"\|(\s*:?-+:?\s*\|)+")
GLYPHS = str.maketrans({"‘": "'", "’": "'", "‚": "'", "‛": "'", "“": '"', "”": '"', "„": '"'})


class InputError(Exception):
    """Unreadable file, or a malformed fixture or primary-publishers block."""


def fold(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text).translate(GLYPHS)).strip()


def norm_url(url: str) -> str:
    p = urlsplit(url.strip())
    return f"{p.scheme.lower()}://{(p.hostname or '').lower()}{p.path.rstrip('/')}" + (f"?{p.query}" if p.query else "")


def bare_url(u: str) -> bool:
    try:
        urlsplit(u)  # raises ValueError on e.g. an unclosed IPv6 bracket; the later host checks would crash on it
    except ValueError:
        return False
    return bool(URL_RE.fullmatch(u))


def is_primary(url: str, entries: list[str]) -> bool:
    p = urlsplit(url)
    host = (p.hostname or "").lower()
    for entry in entries:
        h, _, prefix = entry.lower().partition("/")
        if (host == h or host.endswith("." + h)) and (not prefix or p.path == f"/{prefix}" or p.path.startswith(f"/{prefix}/")):
            return True
    return False


def load_primary(skill: Path) -> dict[str, list[str]]:
    try:
        text = skill.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise InputError(f"cannot read {skill}: {e}") from e
    m = re.search(r"<primary-publishers>\n(.*?)\n</primary-publishers>", text, re.S)
    if not m:
        raise InputError(f"no <primary-publishers> block in {skill}")
    out: dict[str, list[str]] = {}
    for line in m.group(1).splitlines():
        key, sep, rest = line.partition(":")
        if not sep or not rest.split():
            raise InputError(f"bad primary-publishers line: {line!r}")
        out[key.strip()] = rest.split()
    return out


@dataclass
class Fixture:
    name: str
    urls: list[str]  # normalised; the first is the canonical one
    scope: str  # excerpt: proves presence only; full: the whole page text, so absence is INVALID
    text: str


def load_fixtures(directory: Path) -> list[Fixture]:
    if not directory.is_dir():  # glob() on a missing directory is silently empty, which would turn every quote UNVERIFIED
        raise InputError(f"fixtures directory not found: {directory}")
    out: list[Fixture] = []
    for f in sorted(directory.glob("*.txt")):
        try:
            head, sep, body = f.read_text(encoding="utf-8").partition("\n---\n")
        except (OSError, UnicodeDecodeError) as e:
            raise InputError(f"cannot read {f}: {e}") from e
        try:
            urls = [norm_url(v) for k, _, v in (ln.partition(": ") for ln in head.splitlines()) if k == "url"]
        except ValueError as e:  # urlsplit rejects e.g. an unclosed IPv6 bracket
            raise InputError(f"{f.name}: bad url: {e}") from e
        scope = next((v.strip() for k, _, v in (ln.partition(": ") for ln in head.splitlines()) if k == "scope"), "")
        if not (sep and urls and scope in ("excerpt", "full") and body.strip()):
            raise InputError(f"{f.name}: needs url:, scope: excerpt|full, a '---' line and a body")
        out.append(Fixture(f.name, urls, scope, fold(body)))
    return out


def quote_in(text: str, quote: str) -> bool:
    q = fold(quote)
    if q in text:
        return True
    stripped = re.sub(r"(?<=[^\s\d])(?:[*†]|\d{1,2})$", "", q)  # the SKILL.md footnote exception, one marker only
    return stripped != q and stripped in text


def split_row(line: str) -> list[str]:
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return []
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", s[1:-1])]


@dataclass
class Result:
    lines: list[str] = field(default_factory=list)
    ok: int = 0
    unverified: int = 0
    invalid: int = 0

    def add(self, verdict: str, where: str, msg: str) -> None:
        self.lines.append(f"{verdict:<10} {where}: {msg}")
        setattr(self, verdict.lower(), getattr(self, verdict.lower()) + 1)


def check_row(cells: list[str], entries: list[str], fixtures: list[Fixture]) -> tuple[str, str, list[str]]:
    """Return (verdict, message, urls). shortcut: a document is identified by URL (plus fixture aliases), so two renderings
    without an alias count twice, upgrade by adding the alias to the fixture header."""
    _, _, tag, quote, _, url_cell = cells
    urls = url_cell.split()
    via, fig = TAG_VIA.fullmatch(tag), TAG_FIG.fullmatch(tag)
    if tag not in ("EXTRACTED", "INFERRED", "not confirmed") and not via and not fig:
        return "INVALID", f"unknown tag {tag!r}", []
    if urls != ["-"] and not all(bare_url(u) for u in urls):
        return "INVALID", "URL cell must hold bare absolute URLs", []
    if tag == "not confirmed":
        return ("OK", "not confirmed", []) if (quote, urls) == ("-", ["-"]) else ("INVALID", "not confirmed needs Quote - and URL -", [])
    if urls == ["-"] or not urls:
        return "INVALID", "URL missing", []
    if tag == "EXTRACTED" or via:
        if len(urls) != 1:
            return "INVALID", "exactly one URL", urls
        if not (len(quote) > 2 and quote[0] == quote[-1] == '"'):
            return "INVALID", "Quote must be inside straight double quotes", urls
        if "..." in quote or "…" in quote:
            return "INVALID", "ellipsis in Quote", urls
        primary = is_primary(urls[0], entries)
        host = (urlsplit(urls[0]).hostname or "").lower()
        if tag == "EXTRACTED" and not primary:
            return "INVALID", f"{host} is not a primary host", urls
        if via and primary:
            return "INVALID", f"{host} is primary, use EXTRACTED", urls
        if via and not (host == via[1].lower() or host.endswith("." + via[1].lower())):
            return "INVALID", f"via {via[1]} does not match URL host {host}", urls
        fx = next((f for f in fixtures if norm_url(urls[0]) in f.urls), None)
        if fx is None:
            return "UNVERIFIED", "no fixture for this URL", urls
        if quote_in(fx.text, quote[1:-1]):
            return "OK", f"quote found in {fx.name}", urls
        if fx.scope == "full":
            return "INVALID", f"quote not in {fx.name} (full text)", urls
        return "UNVERIFIED", f"quote not in the excerpt {fx.name}", urls
    if quote != "-":
        return "INVALID", f"{tag} needs Quote -", urls
    if fig and len(urls) != 1:
        return "INVALID", "figure tag takes exactly one URL", urls
    return "OK", tag, urls


def check(answer: str, primary: dict[str, list[str]], fixtures: list[Fixture]) -> Result:
    r = Result()
    lines = [ln.rstrip() for ln in answer.strip().splitlines()]
    if not lines:
        r.add("INVALID", "answer", "empty")
        return r
    labels = [x for x in LABELS if x in lines[0].lower()]
    nev = "not externally verified" in labels
    get = lambda p: next((ln[len(p):].strip() for ln in lines if ln.startswith(p)), None)  # noqa: E731
    level, domain, hosts = get("Level: "), get("Domain: "), get("Primary hosts (declared): ")
    entries: list[str] = []
    if not nev:
        if level not in FLOOR:
            r.add("INVALID", "Level", f"missing or unknown: {level!r}")
        if "partial cross-check" in labels and level == "thorough":
            r.add("INVALID", "Level", "partial cross-check cannot report thorough")
        if domain in primary:
            entries = primary[domain]
            if hosts is not None:
                r.add("INVALID", "Primary hosts", "a listed Domain accepts no extra hosts")
        elif domain == "other" and hosts:
            entries = [h for h in re.split(r"[,\s]+", hosts) if h]
        else:
            r.add("INVALID", "Domain", f"missing, unknown or 'other' without Primary hosts: {domain!r}")
    heads = [i for i, ln in enumerate(lines) if re.sub(r"\s+", " ", ln.strip()) == HEADER]
    docs: set[str] = set()
    if len(heads) > 1 or (not heads and not nev):
        r.add("INVALID", "table", "need exactly one claim table with the exact header")
    elif heads:
        i = heads[0] + 1
        if i >= len(lines) or not DELIM.fullmatch(lines[i].strip()):
            r.add("INVALID", "table", "delimiter row missing")
        for n, ln in enumerate(lines[i + 1:], 1):
            if not ln.strip().startswith("|"):
                break
            cells = split_row(ln)
            if len(cells) != 6:
                r.add("INVALID", f"row {n}", f"{len(cells)} cells, need 6")
                continue
            verdict, msg, urls = check_row(cells, entries, fixtures)
            if nev and cells[2] != "not confirmed":
                verdict, msg = "INVALID", "not externally verified allows only not confirmed rows"
            r.add(verdict, f"row {cells[0] or n} [{cells[2]}]", msg)
            for u in urls if verdict != "INVALID" else []:
                docs.add(next((f.urls[0] for f in fixtures if norm_url(u) in f.urls), norm_url(u)))
    if not nev:
        if level in FLOOR and len(docs) < FLOOR[level]:
            r.add("INVALID", "floor", f"{len(docs)} distinct documents, {level} needs {FLOOR[level]}")
        m = LAST.fullmatch(lines[-1].strip())
        form = m.group(1).split()[0] if m else None
        if form is None:
            r.add("INVALID", "last line", "not one of the three Disconfirming search forms")
        elif level in FLOOR and (form == "not") != (level == "quick"):
            r.add("INVALID", "last line", f"{form} does not fit Level: {level}")
    r.lines.append(f"SUMMARY ok={r.ok} unverified={r.unverified} invalid={r.invalid} documents={len(docs)} labels={labels or '-'}")
    return r


def self_test() -> int:
    skill, fx_dir = ROOT / "plugin" / "SKILL.md", ROOT / "tools" / "fixtures"
    primary, fixtures = load_primary(skill), load_fixtures(fx_dir)
    assert set(primary) >= {"http", "law-eu", "ml-paper", "javascript", "python"}, primary
    text = skill.read_text(encoding="utf-8")  # the checker constants must still appear in the contract
    block = text.partition("<output-contract>")[2].partition("</output-contract>")[0]
    for s in (HEADER, "Level: <quick|standard|thorough>", "Domain: <key", "Primary hosts (declared): <host>", "Disconfirming search: found — <URL>",
              "Disconfirming search: ran — nothing opposing found", "Disconfirming search: not run (quick)", "INFERRED (via <host>)", "INFERRED (figure N)"):
        assert s in block, f"{s!r} missing from the <output-contract> block"
    for s in (*LABELS, "quick = 1 source", "at least 2 independent sources"):
        assert s in text, f"{s!r} missing from {skill.name}"
    rfc = "https://www.rfc-editor.org/rfc/rfc9110.html"
    q301 = "For historical reasons, a user agent MAY change the request method from POST to GET for the subsequent request."
    gdpr = "https://publications.europa.eu/resource/cellar/3e485e15-11bd-11e6-ba9a-01aa75ed71a1.0006.03/DOC_1"
    gq = "'pseudonymisation' means the processing of personal data in such a manner that the personal data can no longer be attributed to a specific data subject"

    def ans(rows: list[str], level: str = "standard", domain: str = "http", last: str | None = "Disconfirming search: ran — nothing opposing found", label: str = "", extra: str = "") -> str:
        body = [label] if label else []
        body += ["Conclusion.", f"Level: {level}", f"Domain: {domain}", extra, HEADER, "|---|---|---|---|---|---|", *rows, "Uncertain: none."]
        return "\n".join(x for x in body + ([last] if last else []) if x != "")

    def row(tag: str, quote: str, url: str, n: int = 1) -> str:
        return f"| {n} | claim | {tag} | {quote} | Title, section | {url} |"

    def run(a: str, fx: list[Fixture] | None = None) -> Result:
        return check(a, primary, fixtures if fx is None else fx)

    good = [row("EXTRACTED", f'"{q301}"', rfc + "#name-301-moved-permanently"), row("EXTRACTED", f'"{gq}"', gdpr, 2)]
    r = run(ans(good, domain="http"))
    assert "not a primary host" in "\n".join(r.lines), r.lines  # gdpr host under Domain: http
    r = run(ans([good[0], row("EXTRACTED", f'"{gq}"', gdpr, 2)], domain="law-eu"))
    assert r.invalid >= 1  # rfc host under law-eu
    r = run(ans([row("EXTRACTED", f'"{gq}"', gdpr)], level="quick", domain="law-eu", last="Disconfirming search: not run (quick)"))
    assert (r.invalid, r.ok) == (0, 1), r.lines  # straight quotes in the answer, curly quotes in the page
    r = run(ans([good[0], row("INFERRED", "-", f"{rfc} https://datatracker.ietf.org/doc/html/rfc9110", 2)]))
    assert r.invalid == 1 and "floor" in "\n".join(r.lines), r.lines  # alias URLs are one document
    r = run(ans([good[0], row("INFERRED", "-", "https://www.rfc-editor.org/rfc/rfc9111.html", 2)]))
    assert (r.invalid, r.ok) == (0, 2), r.lines
    r = run(ans([row("EXTRACTED", '"clients MUST NOT change POST to GET on 301"', rfc), good[0].replace("| 1 |", "| 2 |")], level="quick", last="Disconfirming search: not run (quick)"))
    assert r.invalid == 0 and r.unverified == 1, r.lines  # excerpt fixture cannot prove absence
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "page.txt").write_text(f"url: {rfc}\nscope: full\nsource: t\nlicence: t\n---\nA 301 response is cacheable. {q301}\n", encoding="utf-8")
        full = load_fixtures(Path(d))
        r = run(ans([row("EXTRACTED", '"clients MUST NOT change POST to GET on 301"', rfc), row("INFERRED", "-", "https://x.example/a https://y.example/b", 2)]), full)
        assert r.invalid == 1 and "full text" in "\n".join(r.lines), r.lines
        try:
            load_fixtures(Path(d) / "missing")
        except InputError:
            pass
        else:
            raise AssertionError("a missing fixtures directory must be an InputError")
        (Path(d) / "page.txt").write_text("url: http://[bad\nscope: full\n---\nx\n", encoding="utf-8")
        try:
            load_fixtures(Path(d))
        except InputError:
            pass
        else:
            raise AssertionError("a malformed fixture url must be an InputError")
    r = run(ans([row("EXTRACTED", f'"{q301.replace(", ", ",  ")}"', rfc), row("INFERRED (via www.gdpr-info.eu)", f'"{gq}"', "https://www.gdpr-info.eu/art-4-gdpr/", 2)], domain="http"))
    assert r.invalid == 0 and r.ok == 1 and r.unverified == 1, r.lines  # whitespace folding; via on a non-primary host
    r = run(ans([good[0], row("INFERRED (via gdpr-info.eu)", f'"{gq}"', "https://www.gdpr-info.eu/art-4-gdpr/", 2)]))
    assert r.invalid == 0, r.lines  # the tag may name a parent domain of the URL host
    r = run(ans([good[0], row("INFERRED", "-", "http://[bad", 2)]))
    assert r.invalid >= 1 and "bare absolute" in "\n".join(r.lines), r.lines  # a malformed URL is a row verdict, not a crash
    r = run(ans([row("INFERRED (via spec.whatwg.org)", f'"{q301}"', "https://fetch.spec.whatwg.org/", 1), good[0].replace("| 1 |", "| 2 |")], level="quick", last="Disconfirming search: not run (quick)"))
    assert r.invalid == 1 and "is primary" in "\n".join(r.lines), r.lines
    r = run(ans([row("INFERRED (via a.example)", '"x"', "https://b.example/p"), row("EXTRACTED", '"a ... b"', rfc, 2)]))
    assert r.invalid >= 2 and "ellipsis" in "\n".join(r.lines), r.lines  # via host mismatch, ellipsis
    r = run(ans([row("EXTRACTED", f'"{q301}"', rfc), row("not confirmed", "-", "-", 2), row("INFERRED (figure 1)", "-", "https://arxiv.org/abs/2505.22954", 3)]))
    assert r.invalid == 0 and "documents=2" in r.lines[-1], r.lines
    r = run(ans(good[:1], level="quick", last="Disconfirming search: ran — nothing opposing found"))
    assert r.invalid == 1 and "last line" in "\n".join(r.lines), r.lines
    r = run(ans(good[:1], level="standard", last="Disconfirming search: not run (quick)"))
    assert r.invalid == 2, r.lines  # floor and last line
    r = run(ans([good[0]], level="quick", last="Disconfirming search: not run (quick)"))
    assert r.invalid == 0, r.lines
    r = run(ans([good[0], good[0].replace("| 1 |", "| 2 |")], last=None))
    assert any("last line" in x for x in r.lines)
    r = run(ans([good[0]], level="quick", last="Disconfirming search: not run (quick)").replace(HEADER, HEADER.replace("Source | ", "")))
    assert r.invalid >= 1  # exact header
    r = run(ans(["| 1 | claim | EXTRACTED | \"q\" | URL |"], level="quick", last="Disconfirming search: not run (quick)"))
    assert r.invalid >= 1 and "cells" in "\n".join(r.lines), r.lines
    r = run(ans([row("EXTRACTED", '"a \\| b"', "https://docs.example.org/x")], level="quick", domain="other", extra="Primary hosts (declared): docs.example.org, example.net", last="Disconfirming search: not run (quick)"))
    assert r.invalid == 0 and r.unverified == 1, r.lines  # \| unescaped, declared host primary
    r = run(ans([row("EXTRACTED", '"q"', "https://docs.example.org/x")], level="quick", domain="python", extra="Primary hosts (declared): docs.example.org", last="Disconfirming search: not run (quick)"))
    assert r.invalid >= 1  # a listed Domain accepts no extra hosts
    r = run(ans([row("EXTRACTED", '"x"', "https://github.com/python/cpython-fork/x")], level="quick", domain="python", last="Disconfirming search: not run (quick)"))
    assert r.invalid >= 1 and "not a primary host" in "\n".join(r.lines)  # path prefix matches whole segments only
    r = run(ans([row("EXTRACTED", '"x"', "https://github.com/python/cpython/blob/main/x")], level="quick", domain="python", last="Disconfirming search: not run (quick)"))
    assert r.invalid == 0
    for u in ("https://evil.example\\@docs.python.org/3/x", "https://evil.example\\.docs.python.org/3/x"):
        r = run(ans([row("EXTRACTED", '"x"', u)], level="quick", domain="python", last="Disconfirming search: not run (quick)"))
        assert "bare absolute" in "\n".join(r.lines), r.lines  # WHATWG parsers read the host as evil.example, urlsplit as docs.python.org
    r = run("not externally verified\nNo fetch tool was available.\n" + "\n".join([HEADER, "|---|---|---|---|---|---|", row("not confirmed", "-", "-")]))
    assert r.invalid == 0, r.lines
    r = run("not externally verified\nsorry\n" + "\n".join([HEADER, "|---|---|---|---|---|---|", row("EXTRACTED", '"x"', rfc)]))
    assert r.invalid == 1, r.lines
    r = run(ans(good[:1], level="thorough", label="partial cross-check — 2 of 3 source types"))
    assert any("partial cross-check cannot" in x for x in r.lines)
    fn = row("EXTRACTED", '"For historical reasons, a user agent MAY change the request method from POST to GET for the subsequent request.1"', rfc)
    assert run(ans([fn], level="quick", last="Disconfirming search: not run (quick)")).invalid == 0  # one trailing footnote marker
    assert run(ans([row("EXTRACTED", '"2022"', rfc)], level="quick", last="Disconfirming search: not run (quick)")).invalid == 0
    for f in fixtures:  # every shipped fixture is readable and its own start is found
        assert f.text and f.urls and quote_in(f.text, f.text[:60]), f.name
    print("self-test OK:", len(fixtures), "fixtures,", len(primary), "domains")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("answer", nargs="?", help="file with the final answer, or - for stdin")
    ap.add_argument("--fixtures", type=Path, default=ROOT / "tools" / "fixtures")
    ap.add_argument("--skill", type=Path, default=ROOT / "plugin" / "SKILL.md")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    try:
        if a.self_test:
            return self_test()
        if not a.answer:
            ap.error("ANSWER or --self-test required")
        text = sys.stdin.read() if a.answer == "-" else Path(a.answer).read_text(encoding="utf-8")
        res = check(text, load_primary(a.skill), load_fixtures(a.fixtures))
    except (InputError, OSError, UnicodeDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print("\n".join(res.lines))
    return 1 if res.invalid else 0


if __name__ == "__main__":
    sys.exit(main())
