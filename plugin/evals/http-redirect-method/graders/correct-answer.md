---
type: llm
focus: last_message
weight: 1
arm: both
---

Listed facts:
(1) For 301 and 302 the client may change the request method from POST to GET (historically common; not forbidden by the specification).
(2) For 307 and 308 the client must not change the method.
PASS if both are stated. FAIL if either is missing or contradicted (301 or 302 forbid the change; 307 or 308 allow it).
Ignore format, citations, tags and tables. Judge only the listed facts: the answer passes when it states them and says nothing that contradicts them. Do not judge any other statement: you cannot check it without the sources, and an answer must not fail because it says more.
