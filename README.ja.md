<p align="center">
  <img src="assets/logo.svg" width="180" alt="grounded-expert ロゴ：横向きのラーテルの頭">
</p>

# grounded-expert

[![Release](https://img.shields.io/github/v/release/pko89403/grounded-expert)](https://github.com/pko89403/grounded-expert/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | [한국어](README.ko.md) | **日本語** | [简体中文](README.zh-CN.md)

> この翻訳は grounded-expert でレビューし、改善しました（standard レベル）。詳しくは末尾の[翻訳レビュー](#翻訳レビュー)を参照してください。

ドメインの質問に答えるとき、記憶に頼って専門家ペルソナを演じるのではなく、一次情報源（公式仕様、ドキュメント、論文、標準）をリアルタイムで実際に調べ、自分の主張をそれと照合するサブエージェントを起動する Claude Code プラグインです。

## 例

```
/grounded-expert HTTP 301 でリダイレクトされたとき、POST を GET に変えてよいか
RFC に基づいて確認して。
```

**결론:** 현행 RFC 9110에서는 POST 요청이 301 또는 302를 받으면 사용자 에이전트가 리다이렉트된 요청을 GET으로 바꿔도 됩니다(MAY, "역사적인 이유로"라고 명시). 의무는 아니고 허용입니다.

Level: standard
Domain: http

| # | Claim | Tag | Quote | Source | URL |
|---|---|---|---|---|---|
| 1 | RFC 9110은 301 응답 뒤 POST를 GET으로 바꾸는 것을 허용한다(MAY) | EXTRACTED | "For historical reasons, a user agent MAY change the request method from POST to GET for the subsequent request." | RFC 9110 §15.4.2 301 Moved Permanently | https://www.rfc-editor.org/rfc/rfc9110.html |
| 4 | 307에서는 자동 리다이렉트 시 메서드를 바꾸면 안 된다(MUST NOT) | EXTRACTED | "the user agent MUST NOT change the request method if it performs an automatic redirection to that URI." | RFC 9110 §15.4.8 307 Temporary Redirect | https://www.rfc-editor.org/rfc/rfc9110.html |
| 5 | 308은 301과 비슷하지만 POST에서 GET으로의 변경을 허용하지 않는다 | EXTRACTED | "except that it does not allow changing the request method from POST to GET." | RFC 7538 §3 308 Permanent Redirect (Note) | https://www.rfc-editor.org/rfc/rfc7538.html |

Disconfirming search: found — https://www.rfc-editor.org/rfc/rfc2616.html

以下は grounded-expert v0.5.0 の実際の出力です（eval 実行、ケースごとに 1 回）。抜粋には結論、主張 3 行、反証検索のみを残し、回答全文は下に折りたたんであります。

<details>
<summary>回答全文を見る</summary>

**결론:** 현행 RFC 9110에서는 POST 요청이 301 또는 302를 받으면 사용자 에이전트가 리다이렉트된 요청을 GET으로 바꿔도 됩니다(MAY, "역사적인 이유로"라고 명시). 의무는 아니고 허용입니다.

- **307:** RFC 9110 §15.4.8이 "MUST NOT change the request method"라고 명시적으로 금지합니다.
- **308:** 이번에 연 RFC 9110 페이지의 §15.4.9 본문에서는 "MUST NOT" 문장을 확인하지 못했습니다. 대신 RFC 7538(308의 원래 정의)이 "POST에서 GET으로 바꾸는 것을 허용하지 않는다"고 적고 있고, RFC 9110 §15.4.2도 그런 변경을 원하지 않으면 308을 쓰라고 합니다. 그러니 "307/308은 메서드 변경을 금지한다"는 말은 맞습니다. 다만 금지 표현의 강도는 307(MUST NOT)과 308(허용하지 않음)이 다릅니다.
- **303:** RFC 9110에서 303은 POST 처리 결과를 다른 리소스로 보낼 때 쓰는 코드입니다. 사용자 에이전트는 그 URI로 조회 요청(HTTP라면 GET이나 HEAD)을 보낼 수 있다고 되어 있습니다.
- **브라우저 동작 명세:** WHATWG Fetch의 HTTP-redirect fetch는 두 경우에 메서드를 GET으로 바꾸고 본문을 null로 만듭니다. (1) 301/302이고 메서드가 POST일 때, (2) 303이고 메서드가 GET/HEAD가 아닐 때입니다.
- **과거 RFC 2616:** 301/302에서 GET/HEAD가 아닌 요청은 사용자 확인 없이 자동으로 리다이렉트하면 안 된다(MUST NOT)고 했습니다. POST를 GET으로 바꾸는 동작은 "erroneously"(잘못된 것)로 기록했습니다.

Level: standard  
Domain: http

| # | Claim | Tag | Quote | Source | URL |
|---|---|---|---|---|---|
| 1 | RFC 9110은 301 응답 뒤 POST를 GET으로 바꾸는 것을 허용한다(MAY) | EXTRACTED | "For historical reasons, a user agent MAY change the request method from POST to GET for the subsequent request." | RFC 9110 §15.4.2 301 Moved Permanently | https://www.rfc-editor.org/rfc/rfc9110.html |
| 2 | 302에도 같은 허용 문장이 있다 | EXTRACTED | "For historical reasons, a user agent MAY change the request method from POST to GET for the subsequent request." | RFC 9110 §15.4.3 302 Found | https://www.rfc-editor.org/rfc/rfc9110.html |
| 3 | RFC 9110 §15.4.2는 그런 변경을 원하지 않으면 308을 쓰라고 한다 | EXTRACTED | "If this behavior is undesired, the 308 (Permanent Redirect) status code can be used instead." | RFC 9110 §15.4.2 | https://datatracker.ietf.org/doc/html/rfc9110 |
| 4 | 307에서는 자동 리다이렉트 시 메서드를 바꾸면 안 된다(MUST NOT) | EXTRACTED | "the user agent MUST NOT change the request method if it performs an automatic redirection to that URI." | RFC 9110 §15.4.8 307 Temporary Redirect | https://www.rfc-editor.org/rfc/rfc9110.html |
| 5 | 308은 301과 비슷하지만 POST에서 GET으로의 변경을 허용하지 않는다 | EXTRACTED | "except that it does not allow changing the request method from POST to GET." | RFC 7538 §3 308 Permanent Redirect (Note) | https://www.rfc-editor.org/rfc/rfc7538.html |
| 6 | 303은 POST 처리 결과로 사용자 에이전트를 다른 리소스로 보낼 때 주로 쓰인다 | EXTRACTED | "is primarily used to allow the output of a POST action to redirect the user agent to a different resource." | RFC 9110 §15.4.4 303 See Other | https://www.rfc-editor.org/rfc/rfc9110.html |
| 7 | 303을 받은 사용자 에이전트는 그 URI로 GET 또는 HEAD 조회 요청을 보낼 수 있다 | EXTRACTED | "A user agent can perform a retrieval request targeting that URI (a GET or HEAD request if using HTTP)" | RFC 9110 §15.4.4 303 See Other | https://datatracker.ietf.org/doc/html/rfc9110 |
| 8 | Fetch 표준은 301/302 + POST일 때 메서드를 GET으로 바꾼다 | EXTRACTED | "internalResponse’s status is 301 or 302 and request’s method is `POST`" | WHATWG Fetch §4.5 HTTP-redirect fetch, step 12 | https://fetch.spec.whatwg.org/ |
| 9 | Fetch 표준은 303 + GET/HEAD가 아닌 메서드일 때도 GET으로 바꾼다 | EXTRACTED | "internalResponse’s status is 303 and request’s method is not `GET` or `HEAD`" | WHATWG Fetch §4.5 HTTP-redirect fetch, step 12 | https://fetch.spec.whatwg.org/ |
| 10 | 위 조건에 해당하면 메서드를 GET으로, 본문을 null로 설정한다 | EXTRACTED | "Set request’s method to `GET` and request’s body to null." | WHATWG Fetch §4.5 HTTP-redirect fetch | https://fetch.spec.whatwg.org/ |
| 11 | RFC 2616은 301/302에서 GET/HEAD가 아닌 요청을 사용자 확인 없이 자동으로 리다이렉트하는 것을 금지했다 | EXTRACTED | "MUST NOT automatically redirect the request unless it can be confirmed by the user" | RFC 2616 §10.3.2 / §10.3.3 | https://www.rfc-editor.org/rfc/rfc2616.html |
| 12 | RFC 2616은 301에서 POST를 GET으로 바꾸는 HTTP/1.0 클라이언트를 "잘못된" 동작으로 기록했다 | EXTRACTED | "some existing HTTP/1.0 user agents will erroneously change it into a GET request." | RFC 2616 §10.3.2 Note | https://www.rfc-editor.org/rfc/rfc2616.html |
| 13 | RFC 2616은 대부분의 구현이 302를 303처럼 처리한다고 기록했다 | EXTRACTED | "most existing user agent implementations treat 302 as if it were a 303 response" | RFC 2616 §10.3.3 Note | https://www.rfc-editor.org/rfc/rfc2616.html |
| 14 | RFC 2616의 303은 새 URI에서 GET으로 조회해야 한다(SHOULD)고 했다 | EXTRACTED | "SHOULD be retrieved using a GET method on that resource." | RFC 2616 §10.3.4 303 See Other | https://www.rfc-editor.org/rfc/rfc2616.html |
| 15 | RFC 7231(2014)이 301/302의 POST에서 GET으로의 재작성을 처음으로 규격 준수 동작으로 만들었다 | not confirmed | - | RFC 7231 §6.4 (검색 스니펫에서만 봄, 페이지는 열지 않음) | - |

**남은 불확실성**
- 이번에 받은 RFC 9110 §15.4.9 본문에서는 "does not allow changing the request method from POST to GET" 같은 문장을 직접 확인하지 못했습니다. 그래서 308이 메서드를 보존한다는 근거로 RFC 7538과 RFC 9110 §15.4.2를 인용했습니다.
- RFC 7231 §6.4는 직접 열지 않았습니다.
- RFC 2616 인용문은 fetch 도구가 돌려준 발췌입니다. 원문 전체 문장의 앞뒤 맥락(예: "If the 301 status code is received in response to a request other than GET or HEAD")은 직접 확인하지 못했습니다.
- RFC 2616은 이미 폐기된 문서입니다. 현행 규범은 RFC 9110입니다.

Disconfirming search: found — https://www.rfc-editor.org/rfc/rfc2616.html

</details>

Claude Code プラグインです。Google Antigravity と ChatGPT/Codex への対応は実験的です。確認できなかった主張は `not confirmed` と表示されます。

## なぜ必要か

サブエージェントにペルソナ（「あなたは X の専門家です」）を与えると、サブエージェントはその役を演じながら、学習済みの知識（パラメトリック知識）から答えます。そのため、誤った事実も正しい事実と同じくらい自信を持って述べてしまいます。このプラグインは、調べる、見つけたものを引用する、間違っていたら自分で訂正する、という本物の専門家が従う手順を強制します。

## インストール

```
/plugin install grounded-expert --marketplace pko89403/grounded-expert
```

（Claude Code 2.1.275 以降は、このリポジトリをマーケットプレイスのソースとして追加し、追加の確認と、インストールスコープの選択を順に案内します。確認なしに一度でインストールされるわけではありません。スラッシュコマンドの代わりにシェルの `claude plugin install grounded-expert --marketplace pko89403/grounded-expert` を使う場合は Claude Code 2.1.292 以降が必要です。）

ローカル開発では、`claude plugin marketplace add <path-to-this-repo>` を実行してから `claude plugin install grounded-expert@grounded-expert` を実行します。

## Google Antigravity で使う（実験的）

Antigravity 対応はコミュニティがメンテナンスしており、Claude Code の eval suite では検証していません。スキルが起動する `self` subagent が web search と URL-fetch のツールを持つかどうかは、まだ検証していません。持たない場合は記憶で答えず、回答が外部ソースで検証されていないことを伝えるよう、スキルに指示しています。

```
git clone https://github.com/pko89403/grounded-expert.git
cd grounded-expert
git checkout <release-tag>   # リリースに固定し、リンクが変化する作業ツリーを追わないようにする
scripts/install-antigravity.sh --global          # Antigravity App/IDE: ~/.gemini/config/skills/
scripts/install-antigravity.sh --global --cli    # Antigravity CLI: ~/.gemini/antigravity-cli/skills/
cd <your-project> && <clone>/scripts/install-antigravity.sh --workspace   # <project>/.agents/skills/
```

`v0.1.1` 以降のリリースタグを使ってください。`v0.1.0` には `hosts/antigravity/` が含まれていません。

スクリプトは `plugin/` ではなく `hosts/antigravity/` へのシンボリックリンクを作成します。同じモードに `--uninstall` を付けると、そのリンクだけを削除します。実ディレクトリや別の場所を指すリンクには触れません。スキルの配置場所は [Antigravity の skills ドキュメント](https://antigravity.google/docs/skills)に従います。

## ChatGPT と Codex で使う

このリポジトリには、ChatGPT と Codex 向けのポータブルな Agent Plugins
パッケージも含まれています。OpenAI 向けパッケージは `plugin/` の外にあるため、
既存の Claude Code パッケージと eval の対象は変更されません。

```bash
codex plugin marketplace add /absolute/path/to/this-checkout
codex plugin add grounded-expert@grounded-expert
```

`hosts/openai/` を含む `main` をチェックアウトしてください。`v0.3.0` 以前の
リリースタグには含まれません。OpenAI 版は実験段階で、
公開プラグインディレクトリには未提出です。ChatGPT のローカルソースでの
インストール・実行は未検証です。Codex では `$grounded-expert:grounded-expert`
を明示してください。自動トリガーの動作範囲は未検証です。
会話を継承しない子セッションはツールが対応する場合だけ要求し、それ以外は
独立性の制限を開示します。委譲不可なら直接調査、情報源の取得不可なら外部検証
できなかったと報告する指示です。実行環境による強制保証ではありません。
失敗例と再現手順、残る公開条件は [OpenAI 検証記録](docs/openai-evaluation.md) を参照してください。
OpenAI 用の [プライバシー説明](hosts/openai/PRIVACY.md) は Claude 用とは別です。

## 使い方 (Claude Code)

ドメイン固有の事実の正確さが必要な質問や、専門家の意見・レビューを明示的に求めた場合に、スキルが自動で起動します。直接呼び出すこともできます。

```
/grounded-expert <質問>
```

**コストについて：** 呼び出すたびに実際のサブエージェントが起動し、WebSearch/WebFetch をリアルタイムで呼び出します。`standard`/`thorough` では反証検索も追加で行います。キャッシュやローカル検索ではなく、実際の API 使用です。`thorough` はさらに並列サブエージェントを起動します。eval suite（`claude plugin eval`）の実行も毎回実費がかかります（judge モデルと agent モデルの両方に課金）。

### レベル

セッション単位ではなく、質問ごとにレベルを 1 つ選びます（自動推定も可能）。

| レベル | 動作 |
|---|---|
| **quick** | 情報源 1 つ、反証検索なし、自己検証 1 回。 |
| **standard**（デフォルト） | 独立した情報源 2 つ以上、EXTRACTED/INFERRED タグ付け、反証検索 1 回を含む最大 2 回の自己検証。 |
| **thorough** | standard に加え、候補となる情報源の種類ごとにサブエージェントを 1 つずつ並列で追加し、相互検証。安全・法律・金銭が関わる質問向け。 |

トリガー表現：「대충/빨리」（「ざっくり／急いで」の意）→ quick、「꼼꼼히/전부 확인해서」（「念入りに／全部確認して」の意）や法律・安全に関わる質問 → thorough、指定なし → standard。

## プラグイン構成

```
.claude-plugin/marketplace.json  マーケットプレイスマニフェスト（プラグインを ./plugin として登録）
.agents/plugins/marketplace.json ChatGPT/Codex マーケットプレイスマニフェスト
plugin/                          プラグイン本体（ユーザーがインストールする部分）
  .claude-plugin/plugin.json     プラグインマニフェスト（name, version, description, author, homepage, repository）
  SKILL.md                       grounded-expert スキルの定義（手順、レベル、注意点）
  evals/                         `claude plugin eval` 用の eval case（case ごとに prompt.md + graders/*.md）
  README.md, LICENSE             プラグイン用の短い README とライセンス
hosts/openai/                    ポータブル ChatGPT/Codex プラグインとスキルのコピー
README.md                        英語版 README
CONTRIBUTING.md                  PR 用の eval ゲート手順
CHANGELOG.md                     リリース履歴
assets/                          ロゴ（SVG + PNG 512/128/32）とソーシャルプレビュー画像
```

## コントリビュート

[CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。`claude plugin validate --strict` が通っても、変更が動作上安全だとは限りません。その理由と、代わりに何を実行すべきかがそこにまとめてあります。

## ライセンス

MIT。[LICENSE](LICENSE) を参照してください。

## バージョニング

SemVer に従い、スキルの手順と eval suite がまだ固まっていないため `0.x` の範囲にとどまります。`0.x` は minor バージョン間でも API・動作が変わりうることを示し、まだ保証できない `1.0.0` 相当の安定性を約束しないためのものです。eval suite が安定し、一定期間実運用されたら `1.0.0` に上げます。

## 翻訳レビュー

この翻訳は `/grounded-expert` スキルを呼び出し、standard レベルでレビューしました。スキルが起動したサブエージェントが以下の情報源を実際に開いて英語原文と照合し、修正案を出しました。根拠にはそれぞれ EXTRACTED または INFERRED のタグを付け、反証検索も行っています。その結果を反映し、次の点を修正しました。

- 原文との意味のずれ：トリガー表現、「legal」→ 法律、「production use」→ 実運用
- 公式日本語ドキュメントに合わせた用語：サブエージェント、スキル、マーケットプレイス、マニフェスト、スコープ
- 「parametric memory」→ パラメトリック知識
- 文体（です・ます調の統一）、括弧の全角統一、段落内の改行

全角と半角の間のスペースは、公式日本語ドキュメントと Microsoft 日本語スタイルガイドに合わせて入れています（JTF 2.3.1.1 の「スペースを入れない」とは異なります）。コロン（：）は JTF に従い全角です。

レビューは 2 回行いました。1 回目はスキルの手順を手作業で移したサブエージェントで行い、2 回目はスキルを正式に呼び出して、1 回目の修正結果も含めて再検証しました。

- [プラグインの概要（Claude Code Docs）](https://code.claude.com/docs/ja/plugins/overview)
- [プラグインのインストールと管理（Claude Code Docs）](https://code.claude.com/docs/ja/plugins/install)
- [カスタムサブエージェントの作成（Claude Code Docs）](https://code.claude.com/docs/ja/sub-agents)
- [JTF 日本語標準スタイルガイド（翻訳用）](https://www.jtf.jp/pdf/jtf_style_guide.pdf)
- [Microsoft 日本語スタイルガイド](https://download.microsoft.com/download/a/8/2/a822a118-18d4-4429-b857-1b65ab388315/jpn-jpn-StyleGuide.pdf)
- [markdown-it-cjk-breaks](https://github.com/markdown-it/markdown-it-cjk-breaks/blob/master/README.md)
