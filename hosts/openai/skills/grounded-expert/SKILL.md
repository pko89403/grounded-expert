---
name: grounded-expert
description: >-
  Use when the user needs an expert-level answer or review and factual accuracy matters, or asks to verify an external fact against specs or docs instead of guessing from memory. Retrieve current primary sources such as official specifications, documentation, papers, and standards; delegate an independent subagent; label EXTRACTED and INFERRED claims; and search for disconfirming evidence. Trigger on expert-opinion, domain-review, and external factual-verification requests. Skip only questions fully answerable from the current conversation or codebase. Requests for a quick or rough answer select the quick level rather than skipping the skill.
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
| **standard** (default) | Aim for 2+ independently originated sources, EXTRACTED/INFERRED tagging, and up to 2 critique passes including 1 disconfirming-evidence search. Disclose an unmet source floor. |
| **thorough** | standard, plus one additional subagent per candidate source type in parallel when supported, cross-checked. Report any missing delegation or source coverage. For safety, legal liability, or money stakes. |

## OpenAI runtime checks

Use the tools and parameter names actually exposed in this session. Some hosts expose `spawn_agent`; others expose a namespaced equivalent. Do not assume a namespace, agent type, or context parameter exists. Request a fresh/no-history context if the tool supports it, passing only the question, relevant user constraints, and source types. Otherwise disclose the weaker independence.

Delegation is established only by a successful spawn response identifying a real child, not by a wait response or a claimed child summary. Keep that identity; wait only after successful creation, passing its ID when required or correlating mailbox results when the host uses ID-less waiting. If delegation is unavailable, fails, or returns no child identity, do the research directly and label it **direct research; no independent subagent**. If a child lacks web tools, collect evidence in the parent and disclose that limitation. If this session cannot retrieve sources at all, say **not externally verified**; do not fabricate citations or claim a completed research level.

The parent orchestrates thorough research within the host's concurrency limit. Tell each research child to do its assigned lookup itself without re-invoking this skill or creating further agents. Do not change models, permissions, or host configuration to satisfy the workflow.

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

### 3. Spawn a grounded subagent with the OpenAI host's independent subagent tool

Before calling the independent subagent tool, say one line to the user: this spawns a subagent that does real web lookups and a self-critique pass, not a quick memory answer — so the cost/scope is visible before it runs, not discovered after. Don't wait for a reply, just say it and proceed; this is disclosure, not a confirmation gate (gating every call would defeat the point of a skill that fires on its own).

Call the available subagent tool using its actual schema and the runtime checks above. The goal is independent verification with only the task context supplied by the parent. The prompt must include:

1. No persona framing. Don't write "you are an expert in X." Instead: "Actually look up the following sources, and answer based only on what you find."
2. State the requested level and evidence target: quick = 1 source; standard/thorough aim for at least 2 independently originated sources of the types decided in step 2, using the host's web search and page-opening tools. A mirror, translated copy, or several pages repeating one authority are not independent evidence. If only one controlling primary source is available, answer only the supported part and disclose the source shortfall instead of inventing corroboration. For long sources, open the relevant sections rather than the whole document. Reuse retrieved content; an additional targeted open is allowed when a truncated response lacks the needed passage.
3. Put an inline citation (title + the actual opened URL) on every substantive factual claim, tagged EXTRACTED or INFERRED. EXTRACTED requires a short, contiguous quote present in the retrieved text; omit only an attached trailing footnote marker when matching. Keep direct quotations at or below 25 words per source unless the host expressly permits more, and obey any stricter quotation or total-attribution limit across the whole answer. INFERRED covers a clearly explained paraphrase, interpretation, or synthesis grounded in one or more opened sources; identify the supporting source and reasoning without implying multiple-source confirmation. Prefer this form when further quotes would exceed a source's budget. Drop unsupported claims or mark them "not confirmed."
4. A self-refinement loop with two parts in the critique step: (a) check every claim against the material just retrieved, and (b) check whether everything found so far points the same direction / comes from the same type of source — if so, and the level is standard or thorough, **run at least one additional search aimed at finding disconfirming evidence or the opposing position** (re-reading the same sources you already have isn't critique, it's self-confirmation). On quick, skip (b) and stop after one pass. On standard/thorough, revise and repeat up to 2 times, or until the critique finds nothing left to fix.
5. Final output format: conclusion → evidence (per source) → what remains uncertain. Say which level ran, so the user can tell a quick answer from a thorough one. Include a compact evidence receipt for the parent: actual opened URLs, supporting section locations, and any disconfirming query and outcome.

### 4. Hand off the result

Preserve the citations, EXTRACTED/INFERRED tags, uncertainty, and actual execution mode in the handoff. Check that every cited URL was really opened and that quotes match the retrieved text and remain within aggregate source limits. If child tool records are unavailable or the receipt is insufficient, open the cited passage in the parent and disclose the visibility limit; this is not a second independent source. Correct an invalid link or overlong quote before handing off; an accurate cited paraphrase must be tagged INFERRED. Report searches and delegation only when the tool record supports them.

## Scaling up

- The thorough level (see Levels table) covers high-stakes/high-cost questions — don't also hand-roll a parallel cross-check outside it.
- If the same domain comes up repeatedly, save the "source types that turned out reliable" from step 2 to `.agents/grounded-expert/reference/<domain>.md` in the workspace root, not inside this plugin's own directory. Which experts a project needs is project-specific — a Text-to-SQL research repo and a frontend repo don't share a registry, and a project-local file can be committed so teammates reuse it too. Don't create this preemptively — only once it's actually needed.

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
- On standard/thorough, report the actual disconfirming search and its result; if it could not run, say so. On quick, say "disconfirming search not run: quick mode" instead of implying it ran.
- This skill only uses the OpenAI host's independent subagent tool plus its web search and page-opening tools. No separate MCP server or plugin component is needed at this scope.
