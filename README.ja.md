<p align="center">
  <img src="assets/logo.svg" width="180" alt="grounded-expert ロゴ：横向きのラーテルの頭">
</p>

# grounded-expert

[![Release](https://img.shields.io/github/v/release/pko89403/grounded-expert)](https://github.com/pko89403/grounded-expert/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | [한국어](README.ko.md) | **日本語** | [简体中文](README.zh-CN.md)

> この翻訳は grounded-expert 自身でレビューし、改善しています（standard レベル）。詳しくは末尾の[翻訳レビュー](#翻訳レビュー)を参照してください。

ドメインの質問に答えるとき、記憶に頼って専門家ペルソナを演じるのではなく、一次情報源（公式仕様、ドキュメント、論文、標準）をリアルタイムで実際に調べ、自分の主張をそれと照合するサブエージェントを起動する Claude Code プラグインです。

## なぜ必要か

サブエージェントにペルソナ（「あなたは X の専門家です」）を与えると、モデルはその役を演じながらパラメーター記憶から答えます。そのため、誤った事実も正しい事実と同じくらい自信を持って述べてしまいます。このプラグインは、調べる、見つけたものを引用する、間違っていたら自分で訂正する、という本物の専門家が従う手順を強制します。

## インストール

```
/plugin install grounded-expert --marketplace pko89403/grounded-expert
```

（Claude Code 2.1.275 以降は、このリポジトリをマーケットプレイスのソースとして追加し、その追加の確認とインストールスコープの選択を案内します。確認なしに一度でインストールされるわけではありません。スラッシュコマンドの代わりにシェルの `claude plugin install grounded-expert --marketplace pko89403/grounded-expert` を使う場合は Claude Code 2.1.292 以降が必要です。）

ローカル開発では、`claude plugin marketplace add <このリポジトリのパス>` を実行してから `claude plugin install grounded-expert@grounded-expert` を実行します。

## 使い方

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
| **thorough** | standard に加え、候補となる情報源の種類ごとにサブエージェントを 1 つずつ並列で追加し、相互検証。安全・法的責任・金銭が関わる質問向け。 |

トリガー表現：「대충/빨리」（「ざっくり／急いで」の意）→ quick、「꼼꼼히/전부 확인해서」（「念入りに／全部確認して」の意）や法律・安全に関わる質問 → thorough、指定なし → standard。

### 例

```
/grounded-expert HTTP 301 でリダイレクトされたとき、POST を GET に変えてよいか
RFC に基づいて確認して。
```

サブエージェントが RFC 9110/7231 を調べて該当箇所を引用し、主張ごとに EXTRACTED または INFERRED のタグを付け、まだ不確かな点を報告します。

## プラグイン構成

```
.claude-plugin/plugin.json       プラグインマニフェスト（name, version, description, author, homepage, repository）
.claude-plugin/marketplace.json  `/plugin install ... --marketplace` がこのプラグインを見つけるためのマーケットプレイスマニフェスト
SKILL.md                         grounded-expert スキルの定義（手順、レベル、注意点）
evals/                           `claude plugin eval` 用の eval case（case ごとに prompt.md + graders/*.md）
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

SemVer に従い、スキルの手順と eval suite がまだ固まっていないため `0.x` の範囲にとどまります。`0.x` は minor バージョン間でも API・動作が変わりうることを示し、まだ保証できない `1.0.0` 相当の安定性を約束しないためのものです。eval suite が安定し、本番環境で一定期間運用されたら `1.0.0` に上げます。

## 翻訳レビュー

この翻訳は grounded-expert（standard レベル）でレビューしました。サブエージェントが以下の情報源を実際に開いて英語原文と照合し、修正案を出しました。根拠にはそれぞれ EXTRACTED または INFERRED のタグを付け、反証検索も 1 回行っています。その結果を反映し、トリガー表現の意味のずれ、公式日本語ドキュメントに合わせた用語（サブエージェント、スキル、マーケットプレイス、マニフェスト、スコープ）、文体（です・ます調の統一）、括弧の全角統一、段落内の改行を修正しました。

- [プラグインの概要（Claude Code Docs）](https://code.claude.com/docs/ja/plugins/overview)
- [プラグインのインストールと管理（Claude Code Docs）](https://code.claude.com/docs/ja/plugins/install)
- [textlint-rule-preset-JTF-style（JTF 日本語標準スタイルガイド準拠）](https://github.com/textlint-ja/textlint-rule-preset-JTF-style)
- [markdown-it-cjk-breaks](https://github.com/markdown-it/markdown-it-cjk-breaks/blob/master/README.md)
