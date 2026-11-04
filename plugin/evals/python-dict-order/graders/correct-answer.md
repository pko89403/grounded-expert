---
type: llm
focus: last_message
weight: 1
arm: both
---

PASS only if the answer states that dict insertion-order preservation was a CPython implementation detail in 3.6 and became a language-guaranteed feature in 3.7.
FAIL if the answer says 3.6 guaranteed it in the language, conflates 3.6 and 3.7, or states any other wrong fact.
Ignore format, citations, tags and tables; judge only whether the stated facts are correct and whether any stated fact is wrong.
