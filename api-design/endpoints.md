# x402 API Endpoints — Onchain Stock Data

実装は別 repo (Vercel) で行う想定。本 repo は日次 JSON を生成するエンジン側。

## アクセスモデル

| Client | Detection | Pricing | Format |
|--------|-----------|---------|--------|
| AI Agent / Bot | `User-Agent` に bot 系 / `Accept: application/json` / x402 `payment` header | **$0.01 / call** (Base USDC) | JSON |
| Browser (human) | `Accept: text/html` | **無料** | HTML (compression chart + table) |

### x402 フロー (エージェント)

```
1. Agent GET /api/daily-watchlist
2. Server 402 Payment Required + x402 payment instructions
3. Agent sign Base USDC tx ($0.01) → resubmit with payment proof
4. Server verifies → 200 JSON
```

### 無料 HTML フロー (人間)

`Accept: text/html` → static HTML rendering (Next.js SSR / SSG)。
- 日次 watchlist 言及銘柄テーブル
- 各 ticker の tokenized version バッジ (Solana / Base / Arbitrum / BNB Chain アイコン)
- IPO Onchain available のバッジ
- `note` 記事への CTA

## Endpoints

### `GET /api/daily-watchlist`

直近1日分の watchlist 言及銘柄を返す。

**Query params:**
- `date` (optional, default: today UTC) — `YYYY-MM-DD`
- `tokenized` (optional, bool) — `true` の場合は tokenized 対象のみ
- `primary_issuance` (optional, bool) — `true` の場合は IPO Onchain available のみ
- `min_mentions` (optional, int) — 最小言及数フィルタ

**Response (200):**
`outputs/daily-stock-data-YYYY-MM-DD.json` をそのまま返す。

### `GET /api/stocks/:ticker`

個別 ticker の最新統合情報。`outputs/daily-stock-data-*.json` の該当行を返す (なければ過去日を遡る)。

### `GET /api/stocks?tokenized=true`

`tokenized_versions.length > 0` の銘柄のみフィルタして返す。

### `GET /api/stocks?primary_issuance=available`

`primary_issuance_available === true` の銘柄のみフィルタ。

### `GET /api/tokenized-issuers`

`data/tokenized-issuers.json` のマスタを返す (発行体一覧 + チェーン + 制限地域)。週1更新。

### `GET /api/primary-issuance`

`data/primary-issuance.json` のマスタを返す。

## レスポンスヘッダ (共通)

- `X-Disclaimer`: "Data API only. Not investment advice."
- `X-Tokenization-Geo-Notice`: "xStocks / Backpack IPOs Onchain have eligibility restrictions. Verify on platform."
- `Cache-Control`: `public, max-age=300` (5分キャッシュ)
- `X-Data-Source`: "himself65/finance-skills (twitter, yfinance-data) + WebSearch"

## 認証 (将来)

- **無料 tier (人間)**: rate limit 100 req/h (IP ベース)
- **エージェント tier**: 従量課金 $0.01/call、上限なし (x402 micropayment)
- **API key tier (法人)**: 月額または上位料金、Stripe 決済 (オプション)

## デプロイ場所

- Frontend / API: Vercel (別 repo: `x402inc/onchain-stock-api` (仮))
- Data engine: 本 repo (`himself65/finance-skills` consumer) → 日次 cron で JSON 生成 → Vercel に push or S3 連携

## 公開順序

1. 日次 JSON 生成パイプラインを本 repo で安定化 (現段階)
2. Vercel に静的 API として deploy (JSON を直接 serve)
3. x402 payment layer を追加 (User-Agent 判定 → 402 Required → Base USDC 検証)
4. HTML ページの図表 (`generative-ui` Skill で生成) を組み込み
