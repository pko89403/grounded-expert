---
type: llm
focus: last_message
weight: 1
---

The answer must contain a claim table. PASS only if ALL of M1-M3 hold, each in some table row. M1-M3 rows need a non-empty Quote cell (quotes copied from a page):
(M1) a row stating that GET, HEAD, OPTIONS and TRACE are the safe methods, or that PUT is not safe, citing rfc-editor.org RFC 9110 section 9.2.1;
(M2) a row stating that PUT is idempotent, citing RFC 9110 section 9.2.2;
(M3) a row stating that a client SHOULD NOT automatically retry a non-idempotent request, with the exception (the client knows the semantics are idempotent, or can detect the request was never applied), citing RFC 9110 section 9.2.2.
An extra row (M4) may cite RFC 9112 section 9.3.1 (connections can be closed at any time; automatic retry conditions are defined in RFC 9110 section 9.2.2). M4 is optional and must not be required.
A row may be INFERRED (no quote) when it only says POST is not in the idempotent list. A single row may satisfy more than one item. Wording may differ; the meaning must match. Do not require any row beyond M1-M3.
FAIL if any of M1-M3 is missing, or if the conclusion says a POST retry is always allowed or always forbidden with no exception.
