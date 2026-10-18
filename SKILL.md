---
name: grounded-expert
description: Use when the user needs an expert-level answer or review in a specific domain and factual accuracy matters. Spawns a subagent that actually retrieves primary sources (official specs, docs, papers, standards) in real time and checks its own claims against them, instead of role-playing an expert persona. Trigger phrases include "I need an expert opinion", "review this like a real domain expert", "get a second opinion from someone who actually knows this field", or any question where domain-specific factual accuracy is important.
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

Before calling Agent, say one line to the user: this spawns a subagent that does real web lookups and a self-critique pass, not a quick memory answer — so the cost/scope is visible before it runs, not discovered after. Don't wait for a reply, just say it and proceed; this is disclosure, not a confirmation gate (gating every call would defeat the point of a skill that fires on its own).

Call a new agent with `subagent_type: "general-purpose"` (not a fork — the point is independent verification uncontaminated by prior conversation context). The prompt must include:

1. No persona framing. Don't write "you are an expert in X." Instead: "Actually look up the following sources, and answer based only on what you find."
2. State the level (quick/standard/thorough) and its source-count floor: quick = 1 source, standard/thorough = at least 2 independent sources, of the types decided in step 2, via WebSearch/WebFetch. No conclusions before that floor is met. For a long source (a paper, a spec): search within it for the terms/sections the question actually needs, don't read it start-to-finish — that's what burns tokens, not the source count. Fetch a given URL once; don't re-fetch the same URL again just to double-check it answers the same way.
3. An inline citation (title + URL) on every substantive claim, tagged EXTRACTED or INFERRED. EXTRACTED means a source states this near-verbatim — quote the exact matching sentence or phrase next to the citation, so the tag is mechanically checkable later. INFERRED means you connected or synthesized this from multiple sources with no single source stating it directly — say which sources and how. An EXTRACTED tag with no quoted matching text is invalid: downgrade it to INFERRED or drop it. Drop any claim that is neither, or mark it "not confirmed."
4. A self-refinement loop with two parts in the critique step: (a) check every claim against the material just retrieved, and (b) check whether everything found so far points the same direction / comes from the same type of source — if so, and the level is standard or thorough, **run at least one additional search aimed at finding disconfirming evidence or the opposing position** (re-reading the same sources you already have isn't critique, it's self-confirmation). On quick, skip (b) and stop after one pass. On standard/thorough, revise and repeat up to 2 times, or until the critique finds nothing left to fix.
5. Final output format: conclusion → evidence (per source) → what remains uncertain. Say which level ran, so the user can tell a quick answer from a thorough one.

### 4. Hand off the result

Pass the subagent's answer to the user verbatim, including the EXTRACTED/INFERRED tag on every citation. Don't paraphrase or summarize away the citations or their tags — rewriting "EXTRACTED: ..." into plain prose defeats the point of using this skill, since the tag is what makes a claim checkable later.

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
- If a primary source is paywalled/inaccessible, fall back to the next-best open source and say so explicitly.
- Even with grounding, if every source found points to the same conclusion, that's a self-confirmation collapse risk (a closed loop confirming itself with self-selected evidence). The final output must state "disconfirming search attempted / found nothing" or "couldn't find an opposing position." If that's missing, treat the diversity check as skipped.
- This skill only uses Claude Code's Agent tool plus WebSearch/WebFetch. No separate MCP server or plugin component is needed at this scope.
