# Finance Skills × Unicorn Valuation Compression Analysis

## ミッション

himself65/finance-skills を駆動エンジンとして、未上場ユニコーン15社の SaaS valuation compression 分析を実施する。各社の現状バリュエーション・推定 ARR・成長率・comparable 上場 SaaS との比較を構造化し、 「もし上場したら本来いくらになるか」 を逆算する。

## なぜこの分析か

2026年5月時点で未上場ユニコーン (特に AI 系) のバリュエーションが急騰している。Stripe・SpaceX・OpenAI・Anthropic・Databricks 等は数千億ドル規模だが、未上場であるため:

- バリュエーションが Lead 投資家とプレスリリースで決まる (市場検証なし)
- 公開財務情報が限定的
- 上場 SaaS との PER/PSR 倍率比較が困難
- 「未上場プレミアム」「未上場ディスカウント」がブラックボックス

SpaceX が IPO 観測 (時価総額 $1.75T 規模) で日本語圏でも話題になっている今、この空白を埋める分析は意味がある。

## 対象15社 (初期リスト)

優先度順:

1. SpaceX ($1.75T推定・スターリンク61%売上・Grok赤字)
2. OpenAI ($500B推定・GPT 6 サイクル)
3. Stripe ($1.5T推定・決済インフラ)
4. Anthropic ($150B推定・Claude シリーズ)
5. Databricks ($60B推定・データ + AI 統合)
6. xAI ($200B推定・Grok・Twitter 統合)
7. Perplexity ($20B推定・検索 AI)
8. Mistral AI ($15B推定・欧州 LLM)
9. Cursor / Anysphere ($10B推定・コーディング AI)
10. Cohere ($6B推定・エンタープライズ LLM)
11. Glean ($7B推定・エンタープライズ検索)
12. Harvey ($5B推定・リーガル AI)
13. Notion ($10B推定・ワークスペース)
14. Canva ($35B推定・デザインプラットフォーム)
15. Figma ($20B推定・デザインコラボ)

リストは分析中に必要に応じて差し替え可。

## 使用する Skill (実在の5つのみ)

`himself65/finance-skills` は以下の **5 Skill** で構成される。本企画では各 Skill は **データ取得・補助レイヤー** に限定して位置付ける。**SaaS valuation compression の分析ロジック (PSR 計算・SOTP・Bull/Base/Bear シナリオ・確率加重・Compression 係数) は Claude 自身が WebSearch + 推論で実装する**。

| Skill | 種別 | 本企画での用途 |
|-------|------|---------------|
| `yfinance-data` | データ取得 | **Phase 1**: comparable 上場 SaaS の market cap / revenue / PSR 取得 |
| `twitter` | データ取得 | ユニコーン CEO 投稿・Musk 投稿・IPO リーク報道・ソーシャル sentiment |
| `telegram-news` | データ取得 | 補助ニュースフィード (アジア・新興国報道含む) |
| `options-payoff` | 補助分析 | 上場代理銘柄 (`RKLB`, `ADBE`, `MSFT` 等) でのヘッジ pay-off 可視化 |
| `generative-ui` | 出力生成 | **Phase 4**: note 記事用の compression 係数チャート / 比較表 |

### 分析ロジックの担当範囲

| 項目 | 担当 |
|------|------|
| comparable 上場 SaaS データ取得 | `yfinance-data` |
| 公開 SaaS PSR 中央値計算 | **Claude が yfinance 取得値から計算** |
| 未上場ユニコーンのバリュエーション収集 | **Claude + WebSearch** (公式 PR / The Information / FT / Bloomberg / WSJ) |
| 未上場 ARR 推定 | **Claude + WebSearch** + リーク報道照合 |
| PSR 計算 / SOTP / Bull・Base・Bear / 確率加重 / Compression 係数 | **Claude が手計算で実装** |
| sentiment 補強 | `twitter` / `telegram-news` |
| 図表・比較表生成 (note 記事用) | `generative-ui` |

### 重要な制約

- **未上場ユニコーンは `yfinance-data` では取得不可** (Yahoo Finance は上場銘柄のみ)。15社のバリュエーション・ARR は全て WebSearch ベースの推定。
- 「Skill が valuation を分析してくれる」という前提は**誤り**。Skill はあくまでデータ取得・出力支援で、**分析ロジックは Claude が組み立てる**。
- 各推定値は出典 URL を明記し、二次情報には「報道ベース推定」と注記する。

## インストール (上流要確認)

`himself65/finance-skills` は Claude Code プラグイン形式で配布されている (詳細は上流リポジトリ https://github.com/himself65/finance-skills の README で確認)。

以下のような plugin 名は **存在しない** ので使用しないこと:
- ❌ `finance-startup-tools`
- ❌ `finance-market-analysis`
- ❌ `finance-data-providers`
- ❌ `finance-social-readers`

正しいインストールコマンドは上流 README を参照し、本ファイルに追記する。

## 分析フレームワーク

各社について以下を出力する。

### 1. 基本情報
- 現状バリュエーション (Lead round 時点・推定中央値)
- 直近調達 (年月・金額・Lead 投資家)
- 推定 ARR (公開情報・リークベース)
- 推定 ARR 成長率 (YoY)
- 主要事業セグメント
- 主要競合 (上場 + 未上場)

### 2. SaaS Valuation Compression 計算

```
適用倍率: PSR (Price-to-Sales) ベース
基準: 公開 SaaS 上場企業群の中央値 (例: Snowflake・MongoDB・Datadog・Cloudflare・HubSpot)

公開 SaaS 中央値 PSR: X倍 (2026年5月時点)
対象未上場企業 PSR: Y倍 (推定バリュエーション ÷ 推定 ARR)
Compression係数: Y / X

> 1.0 = 上場 SaaS よりプレミアム評価
< 1.0 = 上場 SaaS よりディスカウント評価
```

### 3. Bull / Base / Bear シナリオ

```
Bull: 成長率上振れ + 倍率拡大シナリオの上場後想定時価総額
Base: 現状トレンド継続の上場後想定時価総額
Bear: 成長率下振れ + 倍率収縮シナリオの上場後想定時価総額
```

各シナリオの確率加重期待値も算出。

### 4. リスク要因
- 規制リスク (AI 規制・データ規制等)
- 競合リスク (大手 → 自社の置き換え可能性)
- 収益集中リスク (例: SpaceX のスターリンク61%依存)
- ガバナンスリスク (例: SpaceX の Musk 支配構造)
- 為替・地政学リスク

### 5. 結論
- 「もし今日上場したら」の想定価格 (Bull/Base/Bear 範囲)
- 現状バリュエーションへの評価 (適正 / プレミアム / ディスカウント)
- 個人投資家がアクセスする手段 (セカンダリーマーケット・関連ETF・ADR 等)

## 成果物

### 1. 個別分析ファイル (15本)
```
analyses/
├── 01-spacex.md
├── 02-openai.md
├── 03-stripe.md
├── ...
└── 15-figma.md
```

各ファイル 1500-3000 字程度。上記フレームワークに沿った構造。

### 2. 総合レポート (1本)
```
reports/
└── unicorn-15-summary.md
```

15社の compression 係数比較表・ランキング・全体傾向・投資テーマの整理。

### 3. note 公開用記事 (1-3本)
```
notes/
├── 01-overview-15-unicorns.md       # 全体俯瞰
├── 02-spacex-deep-dive.md           # スペースX 詳細 (IPO 観測の流れに乗せる)
└── 03-ai-vs-non-ai-divergence.md    # AI ユニコーン vs それ以外
```

note 公開用は読者向けに整理・簡略化。

## 進め方

### Phase 1 (1-2日): セットアップと検証
- `yfinance-data` Skill が正常動作することを確認
- comparable 上場 SaaS の現状 PSR を `yfinance-data` で取得 (Snowflake・MongoDB・Datadog 等16社)
- 中央値 PSR を Claude が計算し `reports/phase-1-comparable-psr-baseline.md` に固定値として保存
- `twitter` / `telegram-news` の取得テスト (ユニコーン名で検索 → 報道が拾えるか)

### Phase 2 (3-7日): 個別企業分析
- 優先度順に1社ずつ分析
- 1日1-3社のペース
- **WebSearch でバリュエーション・ARR・直近調達ラウンドの一次/二次情報を収集**
- Phase 1 ベースライン PSR を分母に Compression 係数を Claude が計算
- SOTP・Bull/Base/Bear シナリオも Claude が手計算で記述
- `twitter` で当該企業/CEO に関する直近 sentiment を補強取得

### Phase 3 (1-2日): 総合レポート
- 15社の compression 係数比較
- ランキング作成
- 全体傾向の抽出

### Phase 4 (1-2日): note 公開記事化
- 投資家・スタートアップ層向けに整理
- 図表生成は `generative-ui` Skill を活用 (compression 係数比較チャート等)
- 公開

## 制約と注意事項

### 1. 推定値の扱い
未上場企業のバリュエーション・ARR は公開情報からの推定。各数字には推定レンジ (Low / Mid / High) を付与する。「Approx」「Estimated」を明示。

### 2. 投資助言ではない
分析結果は投資判断材料ではない。免責事項を明記する。

### 3. 一次情報優先
- 公式プレスリリース
- SEC filing (上場予定企業)
- 信頼できるメディア (Bloomberg・WSJ・FT・The Information)
- 投資家公表データ

二次情報・憶測は参考程度。

### 4. データソースの信頼度
各数字に出典を付ける。「The Information report (2026/4)」「FT report (2026/3)」等。

### 5. 著作権
他社レポートの引用は要点抜粋程度に留める。全文転載 NG。

## x402 接続観察ポイント

本プロジェクトの副次的な目的として、 **「分析実行中に発生した有料/従量データ需要の特定」** を継続する。

### 観察対象 (現実的なギャップ)
- `yfinance-data` の制約: rate limit / 銘柄カバレッジ / fundamentals 深度 (10-K レベルにどこまで届くか)
- WebSearch では取得しきれない一次情報 (The Information / Bloomberg Terminal / FT Premium の paywall 記事) の出現頻度
- 未上場ユニコーンの secondary trade データ (Forge Global / EquityZen / Hiive) — 無料 API なし
- `twitter` / `telegram-news` で取りきれない LinkedIn / Discord / 業界 Slack 等のクローズドソース
- 業種特化データ (Starlink subscriber count / SaaS ARR estimate aggregator / 半導体出荷データ)

これらは「サブスク契約は重いが、たまに従量で叩きたい」需要として記録し、後日 x402 化候補リストとしてまとめる。

## 関連リソース

- himself65/finance-skills: https://github.com/himself65/finance-skills
- Funda AI: 各 finance-skills の補強データソース
- x402 Inc. note: https://note.com/x402inc
- x402 Inc. メインプロダクト: https://x402jp.com
- APAC Macro Dashboard (関連): https://x402amd.vercel.app
- 戦略アップデート (前提文書): https://note.com/x402inc/n/nf1c0b4545900

## オーナー

Katomasa (x402 Inc.)

## 更新履歴

- 2026-05-23: 初版作成
- 2026-05-23: **重大修正**。架空の Skill (`saas-valuation-compression` / `startup-analysis` / `estimate-analysis` / `stock-correlation` / `stock-liquidity` / `finance-sentiment` / `discord-reader` / `linkedin-reader` / `funda-data`) と架空の plugin 名 (`finance-startup-tools` 等) を全て削除。実在 5 Skill (`yfinance-data` / `twitter` / `telegram-news` / `options-payoff` / `generative-ui`) に置換し、分析ロジックは Claude 自身が WebSearch + 推論で実装する設計に変更。
