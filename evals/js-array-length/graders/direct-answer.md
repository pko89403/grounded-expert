---
type: llm
focus: last_message
weight: 1
---

PASS if the answer directly states that the array length property is `.length` (correct), without evidence of spawning a grounded-expert subagent or sub-review (no persona framing, no "lookup", no citations/EXTRACTED/INFERRED tags, no mention of an expert subagent being consulted) — i.e. it is answered directly from memory as a trivial fact.
FAIL if the answer is wrong about `.length`, or shows signs that a grounded-expert-style subagent was spawned for this trivial question (e.g. citations, EXTRACTED/INFERRED tags, "실제로 찾아보겠습니다" style lookup framing, multi-source justification).
