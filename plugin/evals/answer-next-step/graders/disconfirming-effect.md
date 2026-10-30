---
type: llm
focus: last_message
weight: 1
---

Find the `Disconfirming search:` line. If it is `ran — nothing opposing found` or `not run (quick)`, PASS. If it starts with `found —`, PASS only if after the URL(s) it says `changes the conclusion` or `keeps the conclusion` followed by a short reason that matches the answer's own conclusion. FAIL if a `found` line has no such statement, or the statement contradicts the conclusion.
