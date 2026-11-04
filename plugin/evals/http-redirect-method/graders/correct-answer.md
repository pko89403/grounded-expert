---
type: llm
focus: last_message
weight: 1
arm: both
---

PASS only if the answer states both facts: (1) for 301 and 302 the client may change the request method from POST to GET (historically common; not forbidden by the specification); (2) for 307 and 308 the client must not change the method.
FAIL if the answer says 301 or 302 forbid the method change, says 307 or 308 allow it, or states any other wrong fact.
Ignore format, citations, tags and tables; judge only whether the stated facts are correct and whether any stated fact is wrong.
