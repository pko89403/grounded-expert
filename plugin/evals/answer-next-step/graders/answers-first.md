---
type: llm
focus: last_message
weight: 1
---

The conclusion is the text before the `Level:` line, after skipping a leading label line (for example `direct answer — no independent subagent`) and at most one session-mode footer line. Skip nothing else: a note, caveat or summary there counts as the first sentence. PASS only if its first sentence answers whether the user's sentence "대응은 각자 구현할 때 정함. test data 사용 금지." should change (keep it, change it, or add to it).
FAIL if the first sentence only describes what the Rust RFC, Kubernetes KEP or Python PEP templates contain, or does not say whether the user's sentence should change.
