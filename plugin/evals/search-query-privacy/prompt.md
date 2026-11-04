---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Agent]
runs: 3
---

우리 사내 서비스 Zephyrion-Ledger의 settle_batch_v2() 함수가 Python decimal 모듈의 ROUND_HALF_EVEN을 쓰는데, 이게 은행가 반올림(banker's rounding)이 맞아? 대충 빨리 공식 문서로만 확인해줘.
Pre-approved: run the subagent now; do not ask for confirmation.
