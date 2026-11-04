---
type: llm
focus: last_message
weight: 1
arm: both
---

Listed facts, from https://www.sqlite.org/foreignkeys.html: foreign key constraints are disabled by default (for backwards compatibility), so they must be enabled separately for each database connection, with `PRAGMA foreign_keys = ON;`.
PASS if the answer says they are off by default and must be enabled per connection. FAIL if it says they are on by default, or that one setting enables them for all connections permanently.
Ignore format, citations, tags and tables. Judge only the listed facts: the answer passes when it states them and says nothing that contradicts them. Do not judge any other statement: you cannot check it without the sources, and an answer must not fail because it says more.
