---
type: llm
focus: last_message
weight: 1
arm: both
---

PASS only if ALL of M1-M3 are stated:
(M1) GET, HEAD, OPTIONS and TRACE are the safe methods; PUT is not safe.
(M2) PUT is idempotent.
(M3) A client SHOULD NOT automatically retry a non-idempotent request, with the exception that it may retry when it knows the request semantics are idempotent or can detect that the request was never applied.
Wording may differ; the meaning must match.
FAIL if any of M1-M3 is missing or wrong, or if the conclusion says a POST retry is always allowed or always forbidden with no exception.
Ignore format, citations, tags and tables; judge only whether the stated facts are correct and whether any stated fact is wrong.
