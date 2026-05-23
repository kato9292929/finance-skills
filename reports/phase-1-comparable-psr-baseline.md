# Phase 1: Comparable 上場 SaaS PSR ベースライン

- **作成日**: 2026-05-23
- **更新方針**: 月次 (毎月第一営業日に再取得)
- **担当**: Katomasa (x402 Inc.)
- **使用 Skill**: `stock-correlation` / `finance-data-providers` 経由で Yahoo Finance / Eastmoney adapter を叩く

---

## 1. 目的

未上場ユニコーン15社の `Compression 係数 = (対象 PSR) / (公開 SaaS 中央値 PSR)` を計算するための **分母** を確定する。本ドキュメントは2026年5月23日時点の中央値を固定値として保存し、`analyses/*.md` から参照する。

---

## 2. Comparable Basket 定義

未上場ユニコーン15社が広く分布するため、basket を3層に分ける。各社の分析では、最も近い basket の中央値を分母として採用する。

### Tier A: ハイパースケール SaaS / インフラ (時価総額 $20B+)

| ティッカー | 企業名 | セクター | 役割 |
|----------|--------|---------|------|
| `SNOW` | Snowflake | データウェアハウス | Databricks 比較 |
| `MDB` | MongoDB | DB | データ基盤比較 |
| `DDOG` | Datadog | 監視 | 開発者向け SaaS |
| `NET` | Cloudflare | エッジ | インフラ SaaS |
| `CRWD` | CrowdStrike | セキュリティ | エンタープライズ SaaS |
| `ZS` | Zscaler | セキュリティ | 〃 |
| `HUBS` | HubSpot | CRM | 中堅 SaaS 代表 |

### Tier B: AI / 開発者ツール / ワークスペース (時価総額 $5–20B)

| ティッカー | 企業名 | セクター | 役割 |
|----------|--------|---------|------|
| `PATH` | UiPath | 自動化 | エンタープライズ AI 比較 |
| `AI` | C3.ai | AI プラットフォーム | エンタープライズ AI |
| `GTLB` | GitLab | DevOps | Cursor / Glean 比較 |
| `MNDY` | Monday.com | ワークスペース | Notion 比較 |
| `ASAN` | Asana | ワークスペース | 〃 |

### Tier C: クリエイティブ / 決済 / 特化型

| ティッカー | 企業名 | セクター | 役割 |
|----------|--------|---------|------|
| `ADBE` | Adobe | クリエイティブ | Canva / Figma 比較 |
| `PYPL` | PayPal | 決済 | Stripe 比較 |
| `ADYEN.AS` | Adyen | 決済 (EU) | 〃 |
| `SQ` (Block) | Block | 決済 | 〃 |

---

## 3. PSR 取得手順 (再現可能性のため明記)

`finance-data-providers` プラグイン経由で:

```bash
# 1. Trailing 12-month revenue を取得
finance-data fetch --tickers SNOW,MDB,DDOG,NET,CRWD,ZS,HUBS,PATH,AI,GTLB,MNDY,ASAN,ADBE,PYPL,ADYEN.AS,SQ \
  --field revenue_ttm \
  --source yahoo

# 2. 直近時価総額を取得
finance-data fetch --tickers <同上> --field market_cap --source yahoo

# 3. PSR = market_cap / revenue_ttm
```

または `stock-correlation` Skill 内で自動計算。

---

## 4. ベースライン値 (2026-05-23 時点 — 要再取得)

> ⚠️ 以下は **プレースホルダ**。Phase 1 実行時に finance-skills を呼んで実値で上書きする。training cutoff (2026年1月) 以降の動きは反映されていない。

| Tier | サンプル N | PSR 中央値 (Mid) | PSR レンジ (P25–P75) |
|------|-----------|----------------|---------------------|
| A | 7 | **TBD** | TBD – TBD |
| B | 5 | **TBD** | TBD – TBD |
| C | 4 | **TBD** | TBD – TBD |
| **全体 (16社)** | 16 | **TBD** | TBD – TBD |

参考: 2024–2025年の公開報道ベースでは、SaaS PSR 中央値は概ね **6–10倍** のレンジで推移していた。AI 特需で Snowflake / MongoDB 等は2025年に再評価が進んだ可能性あり。

---

## 5. ユニコーン別の採用 basket マッピング

| 未上場ユニコーン | 主採用 basket | 補正理由 |
|----------------|--------------|---------|
| SpaceX | Tier A + 通信/航空セクター | 純粋 SaaS でないため hybrid |
| OpenAI | Tier A | ハイパースケール AI |
| Stripe | Tier C (決済) | 決済特化 |
| Anthropic | Tier A | ハイパースケール AI |
| Databricks | Tier A (`SNOW` 中心) | 直接対比 |
| xAI | Tier A | ハイパースケール AI (収益化早期) |
| Perplexity | Tier B | 検索 AI 初期 |
| Mistral AI | Tier B | LLM スタートアップ |
| Cursor (Anysphere) | Tier B (`GTLB`) | 開発者ツール |
| Cohere | Tier B | エンタープライズ LLM |
| Glean | Tier B (`GTLB` + 検索) | エンタープライズ検索 |
| Harvey | Tier B | 業種特化 SaaS |
| Notion | Tier B (`MNDY`/`ASAN`) | ワークスペース |
| Canva | Tier C (`ADBE`) | クリエイティブ |
| Figma | Tier C (`ADBE`) | クリエイティブ |

---

## 6. 次のアクション

- [ ] `finance-data-providers` プラグインで上記17社の PSR を取得しテーブルを実値で上書き
- [ ] 中央値を3 tier × 全体で計算
- [ ] 月次 cron で再取得する仕組みを設定 (`settings.json` で hook 検討)
- [ ] training cutoff 後の構造変化 (例: AI バブル調整・金利動向) を `finance-sentiment` で確認

---

## 出典 / 参照

- `himself65/finance-skills` プラグイン群
- Yahoo Finance (PSR 計算用 revenue / market cap)
- Bloomberg / FT / The Information (補強)
