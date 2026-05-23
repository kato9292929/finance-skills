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

## 使用する Skill

himself65/finance-skills の以下のプラグインを活用:

### 主要 Skill
- saas-valuation-compression — メイン分析エンジン (DCF + relative + SOTP triangulation)
- startup-analysis — VC視点でのスタートアップ評価
- estimate-analysis — ARR / 成長率の estimate 構造化

### 補助 Skill
- stock-correlation — comparable 上場 SaaS との相関 (Snowflake・MongoDB・Datadog 等)
- stock-liquidity — 上場後の想定流動性試算
- finance-sentiment — Twitter/X・LinkedIn・Discord・HackerNews での言及センチメント
- discord-reader / linkedin-reader — ソーシャルでの定性データ取得
- funda-data — Funda AI MCP server 経由の補強データ (必要時のみ・課金観測対象)

## インストール状況

```bash
npx plugins add himself65/finance-skills --plugin finance-startup-tools
npx plugins add himself65/finance-skills --plugin finance-market-analysis
npx plugins add himself65/finance-skills --plugin finance-data-providers
npx plugins add himself65/finance-skills --plugin finance-social-readers
```

(インストール済み Skill は本ファイル更新で反映)

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
- finance-skills の各プラグインが正常動作することを確認
- comparable 上場 SaaS の現状 PSR を取得 (Snowflake・MongoDB・Datadog 等10-15社)
- 公開 SaaS 中央値 PSR を計算・固定値として保存

### Phase 2 (3-7日): 個別企業分析
- 優先度順に1社ずつ分析
- 1日1-3社のペース
- 各社の分析ファイルを作成

### Phase 3 (1-2日): 総合レポート
- 15社の compression 係数比較
- ランキング作成
- 全体傾向の抽出

### Phase 4 (1-2日): note 公開記事化
- 投資家・スタートアップ層向けに整理
- 図表生成 (generative-ui Skill 活用)
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

本プロジェクトの副次的な目的として、 「Skill が呼ぶ有料データレイヤー」の特定 を継続する。

### 観察対象
- funda-data Skill が Funda AI MCP server を呼ぶタイミング・課金額
- discord-reader / linkedin-reader が有料 API 経由になるか
- 公開 SaaS の earnings データ取得で yfinance 制約に当たるか
- 他に「サブスクではなく従量で叩きたいデータ」が発見されるか

これらは別途記録し、後日 x402 化候補リストとしてまとめる。

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
