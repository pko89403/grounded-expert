---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Agent]
runs: 3
---

스터디 노트의 리스크 표에 이렇게 적었어.

| 리스크 | 대응 |
|---|---|
| 같은 요청이 두 번 처리될 수 있음 | 대응은 각자 구현할 때 정함. test data 사용 금지. |

설계 문서 템플릿(Rust RFC, Kubernetes KEP, Python PEP)은 구현하는 사람에게 맡긴 결정을 어떻게 적게 해? 내 "대응은 각자 구현할 때 정함. test data 사용 금지." 문장은 바꿔야 해? 실제 템플릿을 찾아서 확인하고 답해줘, 기억에 의존하지 말고.
Pre-approved: run the subagent now; do not ask for confirmation.
