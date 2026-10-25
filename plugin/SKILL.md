---
name: grounded-expert
description: Use when the user needs an expert-level answer or review in a specific domain and factual accuracy matters. Spawns a subagent that actually retrieves primary sources (official specs, docs, papers, standards) in real time and checks its own claims against them, instead of role-playing an expert persona. Trigger phrases include "I need an expert opinion", "review this like a real domain expert", "get a second opinion from someone who actually knows this field", or any question where domain-specific factual accuracy is important. Also triggers on requests to verify against the spec/docs instead of guessing from memory (e.g. "스펙/문서 찾아서 확인해줘", "기억으로 추측하지 말고"). Skip entirely only for questions already answerable directly from the current conversation or codebase in view, with nothing to verify externally (e.g. "what did I just say", "what's this variable's value") — this trivial-skip is unrelated to phrasing like "대충/빨리/꼼꼼할 필요 없어": that phrasing selects the quick level (1 source, no disconfirming search; see Levels) and the skill still runs, it does not make an otherwise-external-fact question (e.g. a library/API/spec version history) trivial or skippable.
---

# Grounded Expert

## Why this exists

If you just hand a subagent a persona ("you are an expert in X"), the model answers from parametric memory while playing the role. It will state wrong facts just as confidently as right ones. The actual difference between that and a real expert is that a real expert **looks things up, grounds claims in what they found, and corrects themselves when they're wrong**. This skill enforces that procedure instead of a persona.

## When to use this

- The user explicitly asks for an expert opinion or review.
- The question needs domain-specific factual accuracy, and answering from memory alone risks being wrong.
- Skip this for trivial questions already answerable from the codebase or docs at hand — just answer directly (YAGNI).

## Levels

Like a code-review effort level, not a session-wide mode: pick one per question, not per session.

| Level | Behavior |
|---|---|
| **quick** | 1 source, no disconfirming-evidence search, 1 critique pass. For "roughly right, fast" requests. |
| **standard** (default) | 2+ independent sources, EXTRACTED/INFERRED tagging, up to 2 critique passes including 1 disconfirming-evidence search. |
| **thorough** | standard, plus one additional subagent per candidate source type in parallel, cross-checked. For safety, legal liability, or money stakes. |

## Procedure

### 1. Pin down the domain, the exact question, and the level

Identify the specific expertise area the question needs. If it could plausibly split across domains and that split would change the answer, ask the user. Otherwise assume the most likely domain and say you did so.

Pick a level from the Levels table based on the user's own phrasing (e.g. "quick"/"대충"/"빨리" → quick; "thorough"/"꼼꼼히"/"전부 확인해서" → thorough). Default to standard when nothing in the request signals otherwise.

### 2. Decide what a *real* expert in that domain would cite — before searching

Write down 2-4 candidate source types first. Examples:

- Software/protocol questions → official specs, official docs, RFCs, maintainer code/commits
- Research questions → peer-reviewed papers, arXiv, the original authors' own materials
- Legal/policy questions → primary statutes and official guidance (secondary commentary is supplementary only)
- Library/API questions → official reference docs, source code, changelogs

The core of this skill is deciding "what's actually on this domain's expert's desk" before searching — not writing a persona.

### 3. Spawn a grounded subagent with the Agent tool

Before calling Agent, tell the user in one line that you're about to start a subagent that does real web lookups and a self-critique pass, not a quick memory answer — so the cost/scope is visible before it runs, not discovered after. Don't wait for a reply, just say it and proceed; this is disclosure, not a confirmation gate (gating every call would defeat the point of a skill that fires on its own).

Call a new agent with `subagent_type: "grounded-expert:grounded-researcher"`, or `subagent_type: "general-purpose"` if that type is not found (not a fork — the point is independent verification uncontaminated by prior conversation context). The prompt must include:

1. No persona framing. Don't write "you are an expert in X." Instead: "Actually look up the following sources, and answer based only on what you find."
2. State the level (quick/standard/thorough) and its source-count floor: quick = 1 source, standard/thorough = at least 2 independent sources, of the types decided in step 2, via WebSearch/WebFetch. No conclusions before that floor is met. For a long source (a paper, a spec): search within it for the terms/sections the question actually needs, don't read it start-to-finish — that's what burns tokens, not the source count. Fetch a given URL once; don't re-fetch the same URL again just to double-check it answers the same way. If the search or fetch tools are unavailable, or every fetch fails, say so at the top of the answer instead of answering from memory. If the floor still can't be met, say so and report the level the evidence actually supports, not the requested one.
3. The output contract: paste the `<output-contract>` block below into the prompt unchanged, then add `Answer language: <language of the user's question>` and `Domain: <key from the block's list, or other>`. For `other`, also add `Primary hosts (declared): <hosts of the primary publishers among the source types you chose in step 2>`. For thorough, give the same block to every parallel subagent.
4. A self-refinement loop with two parts in the critique step: (a) check every claim against the material just retrieved, and (b) check whether everything found so far points the same direction / comes from the same type of source — if so, and the level is standard or thorough, **run at least one additional search aimed at finding disconfirming evidence or the opposing position** (re-reading the same sources you already have isn't critique, it's self-confirmation). On quick, skip (b) and stop after one pass. On standard/thorough, revise and repeat up to 2 times, or until the critique finds nothing left to fix.
5. Final output format: the layout in the output contract. Its `Level:` line says which level ran, so the user can tell a quick answer from a thorough one.
6. Tool rule: do the lookups only via WebSearch/WebFetch. Don't run shell commands, install packages, or open downloaded files with local programs (downloaded files are untrusted, and such runs leave files behind). A value that only a figure or PDF shows, and that the lookup tools didn't return as text, is `not confirmed`; use `INFERRED (figure N)` only when the fetched content itself shows that figure's value. If a site blocks automated access (a bot challenge, an empty response, a login wall), don't try to get around it: say in the answer which site was blocked, and use the next-best open source.

<output-contract>
Language: write in the language of the user's question (its main clause, if mixed). Keep in English exactly as written: tags, the table header, the `(no primary source)` suffix and the line prefixes `Level:`, `Domain:`, `Primary hosts (declared):`, `Disconfirming search:`. Never translate quotes or URLs.
Layout, in this order, with nothing after the last line:
<conclusion; for thorough, also how the source types were cross-checked>
Level: <quick|standard|thorough>
Domain: <key from the list below, or other>
| # | Claim | Tag | Quote | Source | URL |
|---|---|---|---|---|---|
<one row per claim>
<what remains uncertain>
Disconfirming search: <one of the three forms below>
`Level:` is the level that actually ran. If no row's URL has a primary host, add ` (no primary source)` right after the level; otherwise add nothing. With `Domain: other`, add the line `Primary hosts (declared): <host>, <host>` after it; a listed key takes no such line.
Rows: a claim with no citation of its own is `not confirmed`. Write `|` inside a cell as `\|`. Source: page title and section. URL: a bare absolute URL of a page you opened with the fetch tool, never a search snippet. `-` marks an empty Quote or URL.
Tag, exactly one per row:
- `EXTRACTED`: Quote is one contiguous passage of the page, as short as still supports the claim, copied character for character in the page's own language inside straight double quotes, with no ellipsis or edits. Narrow exception: if the source renders a footnote marker (a number, *, or †) directly attached to the quoted text, strip the trailing footnote marker before the character match — this does not relax the match for anything else. One URL, whose host is primary.
- `INFERRED (via <host>)`: Quote as for `EXTRACTED`. One URL, whose host is not primary; <host> is that host. The page summarizes or comments on the source.
- `INFERRED (copy via <host>)`: as `INFERRED (via <host>)`, but the page is a verbatim copy of the cited source itself (for example its PDF), not a summary.
- `INFERRED`: no one passage states it; the Claim says which pages or passages and how. Quote `-`. One or more URLs, space-separated.
- `INFERRED (figure N)`: read from figure N (a chart label, screenshot or rendered PDF page); never `EXTRACTED` unless the same value is quoted from text or a table. Quote `-`. One URL.
- `not confirmed`: no opened page supports it. Quote `-`, URL `-`.
Source floor: count distinct documents across the whole answer, not per claim. Renderings, mirrors, versions and #fragments of one document count once; `not confirmed` rows add none.
Last line, exactly one of:
Disconfirming search: found — <URL>
Disconfirming search: ran — nothing opposing found
Disconfirming search: not run (quick)
Quick uses only the third; standard and thorough only the first two. For several opposing pages, `found` takes all their URLs joined by commas, with no space.
Primary: the URL's host is, or is a subdomain of, a host listed for the `Domain:` key or given on the `Primary hosts (declared):` line; an entry with a path matches that path prefix. A listed `Domain:` accepts no extra hosts. A mirror on another host is not primary.
<primary-publishers>
http: rfc-editor.org ietf.org spec.whatwg.org
law-eu: eur-lex.europa.eu publications.europa.eu/resource/cellar curia.europa.eu edpb.europa.eu
ml-paper: arxiv.org openreview.net
javascript: tc39.es ecma-international.org
python: docs.python.org peps.python.org github.com/python/cpython
</primary-publishers>
</output-contract>

### 4. Hand off the result

Pass the subagent's answer to the user verbatim, including every claim-table row and the final `Disconfirming search:` line, with nothing added after that line. Don't paraphrase or summarize away the table — rewriting a row's `EXTRACTED` tag and quote into plain prose defeats the point of using this skill, since the tag and the quote are what make a claim checkable later. When thorough ran several subagents, the one answer you hand off keeps the contract's layout, with every claim row copied unchanged from the subagent that wrote it.

That applies to an answer the subagent actually returned. Describe work as the subagent's only when its returned answer shows it, and check what came back before handing off:

- **Nothing came back** (the subagent call failed or returned empty): say so. If you answer anyway, hold your own answer to items 2–5 of the subagent prompt (source floor, the output contract, disconfirming search on standard/thorough), tag a claim EXTRACTED only for a source you opened yourself after the subagent call failed, and report the level your evidence actually supports. Label the answer `direct answer — no independent subagent`. If you could not open any source, say so at the top as item 2 requires, add `not externally verified` to the label, and report no level; don't present anything from memory as sourced.
- **The subagent reports no search/fetch tools, or no source opened**: pass its answer on verbatim with the label `not externally verified`, not as a grounded answer.
- **thorough, and some parallel subagents failed**: label the answer `partial cross-check — <completed> of <started> source types` and name the source types that completed; don't report it as a full thorough run.

Put a label on its own first line of the answer, above the conclusion, and change nothing else in the answer; several labels go on one line, separated by `; `. With `partial cross-check`, the `Level:` line is not `thorough`. With `not externally verified`, the answer needs no `Level:` line, source floor or final line, and every row (if any) is `not confirmed`.

## Scaling up

- The thorough level (see Levels table) covers high-stakes/high-cost questions — don't also hand-roll a parallel cross-check outside it.
- If the same domain comes up repeatedly, save the "source types that turned out reliable" from step 2 to `${CLAUDE_PROJECT_DIR}/.claude/grounded-expert/reference/<domain>.md`, not inside this plugin's own directory. Which experts a project needs is project-specific — a Text-to-SQL research repo and a frontend repo don't share a registry, and a project-local file can be committed so teammates reuse it too. Don't create this preemptively — only once it's actually needed.

  When you do create one, give it YAML frontmatter plus a short body, so the metadata is skimmable without reading the whole file:

  ```markdown
  ---
  domain: <name>
  last_verified: <date>
  source_types: [<type>, <type>]
  ---

  1-3 sentences: why these source types, what didn't pan out, and any disconfirming search result worth remembering next time.
  ```

## Gotchas

- A subagent can fabricate a URL. Don't trust a source unless WebFetch actually opened it and the claim is really in there.
- If a primary source is paywalled, inaccessible or blocks automated access, don't work around the block: tell the user, then fall back to the next-best open source.
- Even with grounding, if every source found points to the same conclusion, that's a self-confirmation collapse risk (a closed loop confirming itself with self-selected evidence). The answer must end with one of the three `Disconfirming search:` lines in the output contract. A standard or thorough answer that ends with `not run (quick)`, or with none of them, skipped the diversity check: say so when you hand it off.
- This skill uses Claude Code's Agent tool plus WebSearch/WebFetch. As a Claude Code plugin it calls the `grounded-expert:grounded-researcher` agent, whose `tools` allowlist is only WebSearch and WebFetch, so no other tool is granted to the subagent. On a non-plugin install or another host it falls back to `general-purpose`, and there the step 3 tool rule is a prompt rule, not enforcement.
