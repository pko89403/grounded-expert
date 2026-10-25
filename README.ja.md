<p align="center">
  <img src="assets/logo.svg" width="180" alt="grounded-expert ロゴ：横向きのラーテルの頭">
</p>

# grounded-expert

[![Release](https://img.shields.io/github/v/release/pko89403/grounded-expert)](https://github.com/pko89403/grounded-expert/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | [한국어](README.ko.md) | **日本語** | [简体中文](README.zh-CN.md)

> この翻訳は grounded-expert でレビューし、改善しました（standard レベル）。詳しくは末尾の[翻訳レビュー](#翻訳レビュー)を参照してください。

ドメインの質問に答えるとき、記憶に頼って専門家ペルソナを演じるのではなく、一次情報源（公式仕様、ドキュメント、論文、標準）をリアルタイムで実際に調べ、自分の主張をそれと照合するサブエージェントを起動する Claude Code プラグインです。

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
codex plugin marketplace add pko89403/grounded-expert
codex plugin add grounded-expert@grounded-expert
```

OpenAI パッケージは実験段階です。ChatGPT ではホストのプラグインディレクトリを
使いますが、利用可否はホスト・アカウントに依存し、実動作は未検証です。
Codex では `$grounded-expert:grounded-expert` を明示するか、自動トリガーを利用します。
会話を継承しない子セッションはツールが対応する場合だけ要求し、それ以外は
独立性の制限を開示します。委譲不可なら直接調査、情報源の取得不可なら外部検証
できなかったと報告する指示です。実行環境による強制保証ではありません。
失敗例と再現手順、残る公開条件は [OpenAI 検証記録](docs/openai-evaluation.md) を参照してください。

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

### 例

```
/grounded-expert HTTP 301 でリダイレクトされたとき、POST を GET に変えてよいか
RFC に基づいて確認して。
```

サブエージェントが RFC 9110/7231 を調べて該当箇所を引用し、主張ごとに EXTRACTED または INFERRED のタグを付け、まだ不確かな点を報告します。

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
