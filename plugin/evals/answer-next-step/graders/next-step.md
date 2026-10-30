---
type: llm
focus: last_message
weight: 1
---

Look at the last line of the answer. PASS only if it starts with `Next step:` and either (a) says what to do with the user's own sentence "대응은 각자 구현할 때 정함. test data 사용 금지." (keep it as it is, or a concrete change such as replacement wording or a named edit), or (b) is `Next step: none — <reason>`.
FAIL if the last line is not a `Next step:` line, if the answer ends on a question or a URL, or if the line gives only general advice that names neither the user's sentence nor a concrete edit.
