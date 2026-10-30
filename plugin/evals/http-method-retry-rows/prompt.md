---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Agent]
runs: 3
---

HTTP에서 PUT은 safe한 메서드야, idempotent한 메서드야? 그리고 연결이 끊겨서 응답을 못 받았을 때 클라이언트가 POST 요청을 자동으로 재시도해도 되는지도 같이 알려줘. 실제 RFC 찾아서 확인하고 답해줘, 기억에 의존하지 말고.
Pre-approved: run the subagent now; do not ask for confirmation.
