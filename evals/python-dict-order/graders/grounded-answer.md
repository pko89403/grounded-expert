---
type: llm
focus: last_message
weight: 1
---

PASS if the answer: (1) cites an official Python source (docs, changelog, or PEP 468/PEP 520/the What's New docs) distinguishing that insertion-order preservation was a CPython 3.6 implementation detail versus becoming a 3.7 language-guaranteed feature, (2) states "Level: quick" or an equivalent statement that a quick/1-source check ran, and (3) does not claim a disconfirming-evidence search was run.
FAIL if the answer: conflates 3.6 and 3.7 without distinguishing implementation detail vs. guarantee, has no official-source citation, or claims a disconfirming-evidence search happened despite quick level.
