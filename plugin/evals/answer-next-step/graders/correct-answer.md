---
type: llm
focus: last_message
weight: 1
arm: both
---

The user asked how the Rust RFC, Kubernetes KEP and Python PEP templates record decisions left to the implementer, and whether their own sentence "대응은 각자 구현할 때 정함. test data 사용 금지." should change.
Listed facts:
(1) The answer takes a position: keep, change or extend that sentence.
(2) Each template has a place for open or deferred decisions: the Rust RFC template has an "Unresolved questions" section, the Kubernetes KEP template has a "Risks and Mitigations" section (and may mark open parts as unresolved), and the Python PEP template (PEP 12) has an "Open Issues" section. The answer must name this place for at least two of the three templates.
PASS if (1) and (2) hold. FAIL if (1) is missing, if fewer than two templates are covered, or if the answer says a template has no place for open decisions.
Ignore format, citations, tags and tables. Judge only the listed facts: the answer passes when it states them and says nothing that contradicts them. Do not judge any other statement: you cannot check it without the sources, and an answer must not fail because it says more.
