---
type: llm
focus: last_message
weight: 1
arm: both
---

The user asked how the Rust RFC, Kubernetes KEP and Python PEP templates record decisions left to the implementer, and whether their own sentence "대응은 각자 구현할 때 정함. test data 사용 금지." should change.
PASS only if the answer (1) says whether that sentence should be kept, changed or extended, and (2) every statement it makes about what the three templates contain is true.
FAIL if the answer gives no position on that sentence, or if any stated fact about a template is wrong.
Ignore format, citations, tags and tables; judge only whether the stated facts are correct and whether any stated fact is wrong.
