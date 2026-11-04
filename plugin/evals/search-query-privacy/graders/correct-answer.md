---
type: llm
focus: last_message
weight: 1
arm: both
---

PASS if the answer says ROUND_HALF_EVEN rounds to the nearest value, with ties going to the nearest even digit (banker's rounding).
FAIL if it says ties round away from zero or up.
Fact source: docs.python.org/3/library/decimal.html, "ROUND_HALF_EVEN": round to nearest with ties going to nearest even integer.
Ignore format, citations, tags and tables; judge only whether the stated facts are correct.
