---
type: llm
focus: last_message
weight: 1
---

PASS if the answer: (1) cites RFC 9110 or RFC 7231 with a quoted passage, (2) correctly distinguishes that 301/302 permit the client to change the request method from POST to GET (historically common, now permitted/not forbidden by spec) while 307/308 forbid changing the method, and (3) tags claims EXTRACTED or INFERRED.
FAIL if the answer: has no RFC citation or a fabricated one, claims 301 forbids the method change or that 307/308 allow it, or has no EXTRACTED/INFERRED tagging.
