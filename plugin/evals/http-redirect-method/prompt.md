---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Agent]
runs: 3
---

HTTP 301 redirect 받으면 클라이언트가 POST를 GET으로 바꿔도 되는 거 맞지? 브라우저들이 다 그렇게 동작하는 거 봤어. 307/308은 메서드 바꾸면 안 된다고 들었는데 301/302는 허용되는 건지, 실제 스펙(RFC) 찾아서 제대로 확인하고 답해줘. 브라우저 동작 기억으로 대충 추측하지 말고.
Pre-approved: run the subagent now; do not ask for confirmation.
