<p align="center">
  <img src="assets/logo.svg" width="180" alt="grounded-expert ロゴ：横向きのラーテルの頭">
</p>

# grounded-expert

[![Release](https://img.shields.io/github/v/release/pko89403/grounded-expert)](https://github.com/pko89403/grounded-expert/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | [한국어](README.ko.md) | **日本語** | [简体中文](README.zh-CN.md)

ドメインの質問に答えるとき、記憶に頼って専門家ペルソナを演じるのではなく、
一次情報源（公式仕様、ドキュメント、論文、標準）をリアルタイムで実際に調べ、
自分の主張をそれと照合する subagent を起動する Claude Code プラグインです。

## なぜ必要か

subagent にペルソナ（「あなたは X の専門家です」）を与えると、モデルはその役を
演じながらパラメータ記憶から答えます。そのため、誤った事実も正しい事実と
同じくらい自信を持って述べてしまいます。このプラグインは、本物の専門家が
従う手順を強制します。調べる、見つけたものを引用する、間違っていたら
自分で訂正する。

## インストール

```
/plugin install grounded-expert --marketplace pko89403/grounded-expert
```

（Claude Code 2.1.275 以降では、このリポジトリを marketplace ソースとして追加し、
確認とインストール scope の選択を経てインストールされます。確認なしの
ワンステップインストールではありません。slash command の代わりにシェルの
`claude plugin install grounded-expert --marketplace pko89403/grounded-expert`
を使う場合は Claude Code 2.1.292 以降が必要です。）

ローカル開発用：`claude plugin marketplace add <このリポジトリのパス>` を実行してから
`claude plugin install grounded-expert@grounded-expert`。

## 使い方

ドメイン固有の事実の正確さが必要な質問や、専門家の意見・レビューを明示的に
求めた場合に、skill が自動で起動します。直接呼び出すこともできます。

```
/grounded-expert <質問>
```

**コストについて：** 呼び出すたびに実際の subagent が起動し、WebSearch/WebFetch
をリアルタイムで呼び出します。`standard`/`thorough` では反証検索も追加で行います。
キャッシュやローカル検索ではなく、実際の API 使用です。`thorough` はさらに
並列 subagent を起動します。eval suite（`claude plugin eval`）の実行も毎回
実費がかかります（judge モデルと agent モデルの両方に課金）。

### レベル

セッション単位ではなく、質問ごとにレベルを 1 つ選びます（自動推定も可能）。

| レベル | 動作 |
|---|---|
| **quick** | 情報源 1 つ、反証検索なし、検討 1 回。 |
| **standard**（デフォルト） | 独立した情報源 2 つ以上、EXTRACTED/INFERRED タグ付け、反証検索 1 回を含む最大 2 回の検討。 |
| **thorough** | standard に加え、候補となる情報源の種類ごとに subagent を 1 つずつ並列で追加し、相互検証。安全・法的責任・金銭が関わる質問向け。 |

トリガー表現：「ざっくり／急いで」（韓国語では「대충/빨리」）→ quick、
「念入りに／全部確認して」（「꼼꼼히/전부 확인해서」）や法律・安全に関わる質問
→ thorough、指定なし → standard。

### 例

```
/grounded-expert HTTP 301 でリダイレクトされたとき、POST を GET に変えてよいか
RFC に基づいて確認して。
```

subagent が RFC 9110/7231 を調べて該当箇所を引用し、主張ごとに EXTRACTED
または INFERRED のタグを付け、まだ不確かな点を報告します。

## プラグイン構成

```
.claude-plugin/plugin.json       プラグイン manifest (name, version, description, author, homepage, repository)
.claude-plugin/marketplace.json  `/plugin install ... --marketplace` がこのプラグインを見つけるための marketplace manifest
SKILL.md                         grounded-expert skill の定義（手順、レベル、注意点）
evals/                           `claude plugin eval` 用の eval case（case ごとに prompt.md + graders/*.md）
README.md                        英語版 README
CONTRIBUTING.md                  PR 用の eval ゲート手順
CHANGELOG.md                     リリース履歴
assets/                          ロゴ（SVG + PNG 512/128/32）とソーシャルプレビュー画像
```

## コントリビュート

[CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。`claude plugin validate --strict`
が通っても、変更が動作上安全だとは限りません。その理由と、代わりに何を実行
すべきかがそこにまとめてあります。

## ライセンス

MIT。[LICENSE](LICENSE) を参照してください。

## バージョニング

SemVer に従い、skill の手順と eval suite がまだ固まっていないため `0.x` の範囲に
とどまります。`0.x` は minor バージョン間でも API・動作が変わりうることを示し、
まだ保証できない `1.0.0` 相当の安定性を約束しないためのものです。eval suite が
安定し、実運用の期間が十分に積み重なったら `1.0.0` に上げます。
