---
type: llm
focus: last_message
weight: 1
arm: both
---

Listed facts:
(M1) GET, HEAD, OPTIONS and TRACE are the safe methods; PUT is not safe.
(M2) PUT is idempotent.
(M3) A client SHOULD NOT automatically retry a non-idempotent request, except when it knows the request semantics are idempotent or can detect that the request was never applied.
Wording may differ; the meaning must match.
PASS if M1-M3 are stated. FAIL if any is missing or contradicted, or if the conclusion says a POST retry is always allowed or always forbidden with no exception.
Ignore format, citations, tags and tables. Judge only the listed facts: the answer passes when it states them and says nothing that contradicts them. Do not judge any other statement: you cannot check it without the sources, and an answer must not fail because it says more.
