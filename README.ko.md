<p align="center">
  <img src="assets/logo.svg" width="180" alt="grounded-expert 로고: 옆모습의 벌꿀오소리 머리">
</p>

# grounded-expert

[![Release](https://img.shields.io/github/v/release/pko89403/grounded-expert)](https://github.com/pko89403/grounded-expert/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | **한국어** | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

> 이 번역은 grounded-expert로 직접 검수하고 개선했습니다(standard 레벨). 자세한 내용은 문서 끝의 [번역 검수](#번역-검수)를 참고하세요.

도메인 질문에 답할 때 기억에 의존해 전문가 페르소나를 연기하는 대신, 1차 출처(공식 스펙, 문서, 논문, 표준)를 실시간으로 직접 찾아보고 자신의 주장을 그 출처와 대조하는 서브에이전트를 생성하는 Claude Code 플러그인입니다.

## 왜 필요한가

서브에이전트에게 페르소나("너는 X 분야 전문가야")를 주면, 서브에이전트는 그 역할을 연기하면서 파라메트릭 메모리(parametric memory)로 답합니다. 그래서 틀린 사실도 맞는 사실만큼 확신 있게 말합니다. 이 플러그인은 실제 전문가가 따르는 절차를 강제합니다. 찾아보고, 찾은 것을 인용하고, 틀렸으면 스스로 교정합니다.

## 설치

```
/plugin install grounded-expert --marketplace pko89403/grounded-expert
```

(Claude Code 2.1.275 이상에서는 이 저장소를 마켓플레이스 소스로 추가하기 전에 확인을 요청하고, 추가가 끝나면 설치 범위를 선택하게 합니다. 확인 없이 한 번에 설치되지는 않습니다. 세션 안의 `/plugin install` 대신 셸에서 `claude plugin install grounded-expert --marketplace pko89403/grounded-expert`를 실행하려면 Claude Code 2.1.292 이상이 필요합니다.)

로컬 개발용: `claude plugin marketplace add <이 저장소 경로>`를 실행한 뒤 `claude plugin install grounded-expert@grounded-expert`를 실행합니다.

## Google Antigravity에서 사용하기 (실험적)

Antigravity 지원은 커뮤니티가 관리하며 Claude Code eval suite로 검증하지 않습니다. 스킬이 실행하는 `self` subagent가 web search와 URL-fetch tool을 갖는지는 아직 검증하지 않았습니다. 갖지 않으면 기억으로 답하지 말고 답이 외부 출처로 검증되지 않았다고 알리도록 스킬에 지시되어 있습니다.

```
git clone https://github.com/pko89403/grounded-expert.git
cd grounded-expert
git checkout <release-tag>   # 릴리스를 고정해 링크가 바뀌는 작업 트리를 따라가지 않게 함
scripts/install-antigravity.sh --global          # Antigravity App/IDE: ~/.gemini/config/skills/
scripts/install-antigravity.sh --global --cli    # Antigravity CLI: ~/.gemini/antigravity-cli/skills/
cd <your-project> && <clone>/scripts/install-antigravity.sh --workspace   # <project>/.agents/skills/
```

`v0.1.1` 이상의 릴리스 태그를 쓰세요. `v0.1.0`에는 `hosts/antigravity/`가 없습니다.

스크립트는 `plugin/`이 아니라 `hosts/antigravity/`를 심볼릭 링크로 연결합니다. 같은 모드에 `--uninstall`을 붙이면 그 링크만 제거합니다. 실제 디렉터리나 다른 곳을 가리키는 링크는 건드리지 않습니다. 스킬 경로는 [Antigravity skills 문서](https://antigravity.google/docs/skills)를 따릅니다.

## 사용법

도메인 지식의 사실 정확성이 중요한 질문이거나, 전문가 의견·리뷰를 명시적으로 요청하면 스킬이 자동으로 실행됩니다. 직접 호출할 수도 있습니다.

```
/grounded-expert <질문>
```

**비용 참고:** 호출할 때마다 실제 서브에이전트가 생성되어 WebSearch/WebFetch를 실시간으로 호출하고, `standard`/`thorough`에서는 반증 검색 단계도 거칩니다. 캐시나 로컬 조회가 아니라 실제 API 사용입니다. `thorough`는 여기에 병렬 서브에이전트를 추가로 생성합니다. eval suite(`claude plugin eval`) 실행도 매번 실제 비용이 듭니다(judge 모델과 agent 모델 모두 과금).

### 레벨

세션 단위가 아니라 질문마다 레벨 하나를 고릅니다(지정하지 않으면 자동으로 추론합니다).

| 레벨 | 동작 |
|---|---|
| **quick** | 출처 1개, 반증 검색 없음, 검토 1회. |
| **standard** (기본) | 독립 출처 2개 이상, EXTRACTED/INFERRED 태깅, 반증 검색 1회를 포함해 최대 2회 검토. |
| **thorough** | standard에 더해, 후보 출처 유형마다 서브에이전트를 하나씩 병렬로 추가하고 교차 검증. 안전·법률·금전이 걸린 질문용. |

트리거 표현: "대충/빨리" → quick, "꼼꼼히/전부 확인해서" 또는 법률·안전이 걸린 질문 → thorough, 지정 없음 → standard.

### 예시

```
/grounded-expert HTTP 301로 리다이렉트되면 POST를 GET으로 바꿔도 되는지
RFC 기준으로 확인해줘.
```

서브에이전트가 RFC 9110/7231을 찾아 해당 구절을 인용하고, 주장마다 EXTRACTED 또는 INFERRED 태그를 붙이고, 아직 불확실한 부분을 보고합니다.

## 플러그인 구조

```
.claude-plugin/marketplace.json  마켓플레이스 매니페스트 (플러그인을 ./plugin으로 등록)
plugin/                          플러그인 본체 (사용자가 설치하는 부분)
  .claude-plugin/plugin.json     플러그인 매니페스트 (name, version, description, author, homepage, repository)
  SKILL.md                       grounded-expert 스킬 정의 (절차, 레벨, 주의사항)
  evals/                         `claude plugin eval`용 eval case (case마다 prompt.md + graders/*.md)
  README.md, LICENSE             플러그인용 짧은 README와 라이선스
README.md                        영어 README
CONTRIBUTING.md                  PR용 eval 게이트 절차
CHANGELOG.md                     릴리스 이력
assets/                          로고 (SVG + PNG 512/128/32) 및 소셜 미리보기 이미지
```

## 기여하기

[CONTRIBUTING.md](CONTRIBUTING.md)를 참고하세요. `claude plugin validate --strict` 통과가 곧 변경이 동작상 안전하다는 뜻은 아닙니다. 그 이유와 대신 무엇을 실행해야 하는지가 해당 문서에 정리되어 있습니다.

## 라이선스

MIT. [LICENSE](LICENSE)를 참고하세요.

## 버전 정책

SemVer를 따르며, 스킬 절차와 eval suite가 아직 자리 잡는 중이라 `0.x` 범위에 머뭅니다. `0.x`는 minor 버전 사이에도 API·동작이 바뀔 수 있음을 나타내므로, 아직 뒷받침할 수 없는 `1.0.0` 수준의 안정성을 약속하지 않아도 됩니다. eval suite가 안정되고 프로덕션 환경에서 일정 기간 운영되면 `1.0.0`으로 올립니다.

## 번역 검수

이 번역은 `/grounded-expert` 스킬을 호출해 standard 레벨로 검수했습니다. 스킬이 생성한 서브에이전트가 아래 출처를 실제로 열어 영어 원문과 대조해 수정안을 냈고, 근거마다 EXTRACTED 또는 INFERRED 태그를 붙였으며, 반증 검색을 거쳤습니다. 그 결과를 반영해 다음을 고쳤습니다.

- 원문과 뜻이 어긋난 곳: "production" 누락, 설치 흐름 순서(공식 문서 기준으로 마켓플레이스 추가 **전에** 확인), 주어 불일치
- 조사 띄어쓰기
- 공식 한국어 문서 기준의 용어: 서브에이전트, 스킬, 마켓플레이스, 매니페스트, 범위, 저장소
- 구어체·번역투 표현, "파라메트릭 메모리(parametric memory)" 표기

검수는 두 번 했습니다. 1차는 스킬 절차를 수동으로 옮긴 서브에이전트로 진행했고, 2차는 스킬을 정식으로 호출해 1차 수정 결과까지 다시 검증했습니다.

- [국립국어원 한글 맞춤법](https://korean.go.kr/kornorms/regltn/regltnView.do?regltn_code=0001&regltn_no=270)
- [Claude Code 플러그인 개요 (ko)](https://code.claude.com/docs/ko/plugins)
- [Claude Code 명령 (ko)](https://code.claude.com/docs/ko/commands)
- [Claude Code 플러그인 설치 및 관리 (ko)](https://code.claude.com/docs/ko/discover-plugins)
- [Microsoft Korean Localization Style Guide](https://download.microsoft.com/download/5/b/6/5b62389f-4e3b-4c77-bc18-94efba2fa7bb/kor-kor-StyleGuide.pdf)
- [CommonMark Spec 0.31.2](https://spec.commonmark.org/0.31.2/#soft-line-breaks)
