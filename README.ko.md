<p align="center">
  <img src="assets/logo.svg" width="180" alt="grounded-expert 로고: 옆모습의 벌꿀오소리 머리">
</p>

# grounded-expert

[![Release](https://img.shields.io/github/v/release/pko89403/grounded-expert)](https://github.com/pko89403/grounded-expert/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | **한국어** | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

도메인 질문에 답할 때 기억에 의존해 전문가 페르소나를 연기하는 대신,
1차 출처(공식 스펙, 문서, 논문, 표준)를 실시간으로 직접 찾아보고 자신의
주장을 그 출처와 대조하는 subagent를 띄우는 Claude Code 플러그인입니다.

## 왜 필요한가

subagent에게 페르소나("너는 X 분야 전문가야")를 주면, 모델은 그 역할을
연기하면서 파라미터 메모리로 답합니다. 그래서 틀린 사실도 맞는 사실만큼
확신 있게 말합니다. 이 플러그인은 실제 전문가가 따르는 절차를 강제합니다.
찾아보고, 찾은 것을 인용하고, 틀렸으면 스스로 교정합니다.

## 설치

```
/plugin install grounded-expert --marketplace pko89403/grounded-expert
```

(Claude Code 2.1.275 이상에서는 이 레포를 marketplace 소스로 추가한 뒤,
확인 단계와 설치 scope 선택을 거칩니다. 확인 없이 한 번에 설치되지는
않습니다. slash command 대신 셸 명령
`claude plugin install grounded-expert --marketplace pko89403/grounded-expert`
를 쓰려면 Claude Code 2.1.292 이상이 필요합니다.)

로컬 개발용: `claude plugin marketplace add <이 레포 경로>` 실행 후
`claude plugin install grounded-expert@grounded-expert`.

## 사용법

도메인 특화 사실 정확도가 필요한 질문이거나, 전문가 의견·리뷰를 명시적으로
요청하면 skill이 자동으로 실행됩니다. 직접 호출할 수도 있습니다.

```
/grounded-expert <질문>
```

**비용 참고:** 호출할 때마다 실제 subagent가 떠서 WebSearch/WebFetch를
실시간으로 호출하고, `standard`/`thorough`에서는 반증 검색도 한 번 더
수행합니다. 캐시나 로컬 조회가 아니라 실제 API 사용입니다. `thorough`는
여기에 병렬 subagent를 추가로 띄웁니다. eval suite(`claude plugin eval`)
실행도 매번 실제 비용이 듭니다(judge 모델과 agent 모델 모두 과금).

### 레벨

세션 단위가 아니라 질문마다 레벨 하나를 고릅니다(자동 추론도 됩니다).

| 레벨 | 동작 |
|---|---|
| **quick** | 출처 1개, 반증 검색 없음, 검토 1회. |
| **standard** (기본) | 독립 출처 2개 이상, EXTRACTED/INFERRED 태깅, 반증 검색 1회를 포함해 최대 2회 검토. |
| **thorough** | standard에 더해, 후보 출처 유형마다 subagent를 하나씩 병렬로 추가하고 교차 검증. 안전·법적 책임·금전이 걸린 질문용. |

트리거 표현: "대충/빨리" → quick, "꼼꼼히/전부 확인해서" 또는 법률·안전
관련 질문 → thorough, 지정 없음 → standard.

### 예시

```
/grounded-expert HTTP 301로 리다이렉트되면 POST를 GET으로 바꿔도 되는지
RFC 기준으로 확인해줘.
```

subagent가 RFC 9110/7231을 찾아 해당 구절을 인용하고, 주장마다
EXTRACTED 또는 INFERRED 태그를 붙이고, 아직 불확실한 부분을 보고합니다.

## 플러그인 구조

```
.claude-plugin/plugin.json       플러그인 manifest (name, version, description, author, homepage, repository)
.claude-plugin/marketplace.json  `/plugin install ... --marketplace`가 이 플러그인을 찾을 수 있게 하는 marketplace manifest
SKILL.md                         grounded-expert skill 정의 (절차, 레벨, 주의사항)
evals/                           `claude plugin eval`용 eval case (case마다 prompt.md + graders/*.md)
README.md                        영어 README
CONTRIBUTING.md                  PR용 eval 게이트 절차
CHANGELOG.md                     릴리스 이력
assets/                          로고 (SVG + PNG 512/128/32) 및 소셜 미리보기 이미지
```

## 기여하기

[CONTRIBUTING.md](CONTRIBUTING.md)를 참고하세요. `claude plugin validate --strict`
통과가 곧 변경이 동작상 안전하다는 뜻은 아닙니다. 그 이유와 대신 무엇을
실행해야 하는지가 거기 정리돼 있습니다.

## 라이선스

MIT. [LICENSE](LICENSE)를 참고하세요.

## 버전 정책

SemVer를 따르며, skill 절차와 eval suite가 아직 자리 잡는 중이라 `0.x`
범위에 머뭅니다. `0.x`는 minor 버전 사이에도 API·동작이 바뀔 수 있다는
뜻으로, 아직 보장할 수 없는 `1.0.0` 수준의 안정성을 약속하지 않기 위함입니다.
eval suite가 안정되고 실제 사용 기간이 쌓이면 `1.0.0`으로 올립니다.
