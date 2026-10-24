---
name: grounded-expert
description: >-
  Use when expert-level answers or reviews need domain-specific factual accuracy, or the user asks to verify external facts against specs/docs instead of guessing from memory. Retrieve primary sources, label EXTRACTED/INFERRED claims, self-critique, and request an independent subagent when the host supports it. Trigger on expert opinions, domain reviews, and requests such as "스펙/문서 찾아서 확인해줘" or "기억으로 추측하지 말고". Skip only questions fully answerable from the current conversation or codebase with nothing external to verify. "대충/빨리/꼼꼼할 필요 없어" and quick/rough phrasing select quick level, not skipping an external-fact question.
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

## OpenAI runtime checks

Use only delegation tools and parameters actually exposed in the session. Request a fresh/no-history child when supported, supplying only the question, relevant constraints and source types; otherwise disclose the weaker isolation. Do not change models, permissions or host configuration to satisfy this skill.

A successful spawn response must identify a real child before waiting; use its ID when required, or correlate mailbox results for an ID-less wait API. A wait response is not proof of creation or research. If delegation is unavailable or fails, follow step 4's `direct answer — no independent subagent` branch. Do not attribute work to a child before its answer and evidence receipt return. If retrieval is unavailable, follow the `not externally verified` branch and report no completed research level.

The source floor is mandatory, not a target. Mirrors, translations and several pages repeating one authority are not independently originated sources. If standard's floor is not met but one source supports a quick answer, explicitly report quick, not standard. Parent orchestration must respect the host's concurrency limit and step 4's partial-cross-check label.

Keep direct quotes at or below 25 words per source unless the host expressly permits more, and obey stricter quotation/attribution limits. INFERRED retains the canonical multiple-source synthesis meaning; it is not a fallback tag for a single-source paraphrase. An EXTRACTED claim without a matching quote can become INFERRED only if that definition is independently met; otherwise drop it or mark it `not confirmed`.

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

### 3. Attempt to start a grounded subagent with the host's delegation tool

Before calling the host's delegation tool, tell the user in one line that you're about to start a subagent that does real web lookups and a self-critique pass, not a quick memory answer — so the cost/scope is visible before it runs, not discovered after. Don't wait for a reply, just say it and proceed; this is disclosure, not a confirmation gate (gating every call would defeat the point of a skill that fires on its own).

Use the available delegation tool's actual schema and the runtime checks above to request an independent child. The prompt must include:

1. No persona framing. Don't write "you are an expert in X." Instead: "Actually look up the following sources, and answer based only on what you find."
2. State the level (quick/standard/thorough) and its source-count floor: quick = 1 source, standard/thorough = at least 2 independent sources, of the types decided in step 2, via the host's web search and page-opening tools. No conclusions before that floor is met. For a long source (a paper, a spec): search within it for the terms/sections the question actually needs, don't read it start-to-finish — that's what burns tokens, not the source count. Fetch a given URL once; don't re-fetch the same URL again just to double-check it answers the same way. If the search or fetch tools are unavailable, or every fetch fails, say so at the top of the answer instead of answering from memory. If the floor still can't be met, say so and report the level the evidence actually supports, not the requested one.
3. An inline citation (title + URL) on every substantive claim, tagged EXTRACTED or INFERRED. EXTRACTED means a source states this near-verbatim — quote the exact matching sentence or phrase next to the citation, so the tag is mechanically checkable later. Narrow exception: if the source renders a footnote marker (a number, *, or †) directly attached to the quoted text, strip the trailing footnote marker before the character match — this does not relax the match for anything else. INFERRED means you connected or synthesized this from multiple sources with no single source stating it directly — say which sources and how. An EXTRACTED tag with no quoted matching text is invalid: downgrade it to INFERRED or drop it. Drop any claim that is neither, or mark it "not confirmed."
4. A self-refinement loop with two parts in the critique step: (a) check every claim against the material just retrieved, and (b) check whether everything found so far points the same direction / comes from the same type of source — if so, and the level is standard or thorough, **run at least one additional search aimed at finding disconfirming evidence or the opposing position** (re-reading the same sources you already have isn't critique, it's self-confirmation). On quick, skip (b) and stop after one pass. On standard/thorough, revise and repeat up to 2 times, or until the critique finds nothing left to fix.
5. Final output format: conclusion → evidence (per source) → what remains uncertain. Say which level ran, so the user can tell a quick answer from a thorough one.

6. OpenAI only: "Do not invoke this skill again or create further agents; perform your assigned lookups yourself. Return a separate compact evidence receipt listing actual opened URLs, supporting section locations, and any disconfirming query and outcome."

### 4. Hand off the result

Pass the subagent's answer to the user verbatim, including the EXTRACTED/INFERRED tag on every citation. Don't paraphrase or summarize away the citations or their tags — rewriting "EXTRACTED: ..." into plain prose defeats the point of using this skill, since the tag is what makes a claim checkable later.

That applies to an answer the subagent actually returned. Describe work as the subagent's only when its returned answer shows it, and check what came back before handing off:

- **Nothing came back** (the subagent call failed or returned empty): say so. If you answer anyway, hold your own answer to items 2–4 of the subagent prompt (source floor, quoted and tagged citations, disconfirming search on standard/thorough), tag a claim EXTRACTED only for a source you opened yourself after the subagent call failed, and report the level your evidence actually supports. Label the answer `direct answer — no independent subagent`. If you could not open any source, say so at the top as item 2 requires, add `not externally verified` to the label, and report no level; don't present anything from memory as sourced.
- **The subagent reports no search/fetch tools, or no source opened**: pass its answer on verbatim with the label `not externally verified`, not as a grounded answer.
- **thorough, and some parallel subagents failed**: label the answer `partial cross-check — <completed> of <started> source types` and name the source types that completed; don't report it as a full thorough run.

OpenAI validation: check the child evidence receipt and available tool records before handoff. Append parent validation findings (invalid/unopened links, missing quotes, quotation-limit failures or unavailable child records) separately; do not silently rewrite the child's citations, tags or prose. If forwarding the original would violate the host's quotation or other limits, request a compliant child revision and pass that returned revision verbatim, stating what failed and that a revision was requested. If no compliant revision is available, withhold the noncompliant material and report the limitation rather than repairing it yourself. A receipt without a visible retrieval record is not independently verified retrieval.

## Scaling up

- The thorough level (see Levels table) covers high-stakes/high-cost questions — don't also hand-roll a parallel cross-check outside it.
- If the same domain comes up repeatedly, save the "source types that turned out reliable" from step 2 to `.agents/grounded-expert/reference/<domain>.md` in the workspace root (shared with the Antigravity host; this does not migrate Claude's existing notes), not inside this plugin's own directory. Which experts a project needs is project-specific — a Text-to-SQL research repo and a frontend repo don't share a registry, and a project-local file can be committed so teammates reuse it too. Don't create this preemptively — only once it's actually needed.

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

- A subagent can fabricate a URL. Don't trust a source unless the host's page-opening tool actually opened it and the claim is really in there.
- If a primary source is paywalled/inaccessible, fall back to the next-best open source and say so explicitly.
- Even with grounding, if every source found points to the same conclusion, that's a self-confirmation collapse risk (a closed loop confirming itself with self-selected evidence). The final output must state "disconfirming search attempted / found nothing" or "couldn't find an opposing position." If that's missing, treat the diversity check as skipped.
- On quick, the diversity-search requirement above does not apply: say "disconfirming search not run: quick mode." On standard/thorough, report the actual search or disclose that it could not run.
- When available, this skill uses the host's delegation, web search and page-opening tools. No separate MCP server or plugin component is needed at this scope; unavailable tools follow the explicit failure branches above.
