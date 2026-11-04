---
type: llm
focus: last_message
weight: 1
arm: both
---

Listed fact: dict insertion-order preservation was a CPython implementation detail in 3.6 and became a language guarantee in 3.7.
PASS if the answer states it. FAIL if it is missing or contradicted (3.6 guaranteed it in the language, or 3.6 and 3.7 are not distinguished).
Ignore format, citations, tags and tables. Judge only the listed facts: the answer passes when it states them and says nothing that contradicts them. Do not judge any other statement: you cannot check it without the sources, and an answer must not fail because it says more.
