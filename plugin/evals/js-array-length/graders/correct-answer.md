---
type: llm
focus: last_message
weight: 1
arm: both
---

Listed fact: the JavaScript array length property is `.length`.
PASS if the answer states it. FAIL if it names a different property. Do not penalize a lookup or citations here.
Ignore format, citations, tags and tables. Judge only the listed facts: the answer passes when it states them and says nothing that contradicts them. Do not judge any other statement: you cannot check it without the sources, and an answer must not fail because it says more.
