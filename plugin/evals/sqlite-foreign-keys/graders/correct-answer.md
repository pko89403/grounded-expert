---
type: llm
focus: last_message
weight: 1
arm: both
---

The facts, from https://www.sqlite.org/foreignkeys.html: foreign key constraints are disabled by default (for backwards compatibility), so they must be enabled separately for each database connection; the enabling command is `PRAGMA foreign_keys = ON;`.
PASS only if the answer says foreign keys are off by default and must be enabled per connection (PRAGMA foreign_keys = ON).
FAIL if the answer says they are on by default, or that one setting enables them for all connections permanently.
Ignore format, citations, tags and tables; judge only whether the stated facts are correct and whether any stated fact is wrong.
