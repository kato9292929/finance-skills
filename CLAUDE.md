# Onchain Stock Data — Watchlist-driven niche stock data API

## ミッション

twitter 監視リストで言及されたニッチ銘柄 + 株式トークン化情報 + IPO 一次発行情報を統合し、**x402 対応データ API** として配信する。「S&P500 全銘柄ベース」ではなく、信頼できる18人の twitter 監視対象から「今この瞬間に話題になっているニッチ銘柄」だけを動的にカバーする。

エージェント (Bot / AI Agent) には従量課金 (Base USDC 0.01/call)、人間ブラウザには無料 HTML ページを返す。

## なぜこの企画か

1. **S&P500 全カバーは redundant**: Bloomberg / Yahoo / Polygon が既に網羅。差別化不可。
2. **ニッチ銘柄こそ価値**: VELO / RDW / BKSY / GHM / SPCX (未上場) 等、機関ユニバースから漏れる銘柄を信頼ソース経由で拾う。
3. **トークン化と一次発行 onchain の融合**: xStocks (Solana)、Backed (Base)、Dinari (Arbitrum)、Ondo、そして Backpack IPOs Onchain (Superstate × Solana) — この4–5基盤を1つの ticker JSON に正規化したサービスはまだない。
4. **x402 native**: 「エージェントが叩く API」を最初から想定し、人間/エージェントを HTTP レイヤで分岐する。

## カバーする3層

| Layer | 対象 | 主要発行体 / プラットフォーム |
|------|------|----------------------------|
| **L1: 上場済株式のトークン化 (二次流通)** | 上場株式の onchain 表現 | Backed Finance xStocks (Solana 60+), Backed Finance Base (`bCOIN` 他), Dinari Arbitrum (`dXXX`), Ondo Finance RWA |
| **L2: 一次発行 IPO アロケーション** | SEC 登録 IPO の onchain 配布 | Backpack IPOs Onchain (Superstate × Solana) |
| **L3: 取引所側のトークン化計画 (情報のみ)** | 統合は将来 | Coinbase Tokenize (2026年内ローンチ予定), Base App のトークン化株式取引ハブ計画 |

L3 は status トラッキングのみ (実データ統合は対象外、ニュース欄として扱う)。

## 使用する Skill (実在の5つだけ)

`himself65/finance-skills` の Skill は以下の **5つのみ**。本企画は分析企画ではなくデータ統合企画なので、用途は限定的。

| Skill | 用途 |
|-------|------|
| `twitter` | 監視リスト18人の直近24h post 取得 (本企画の **主データソース**) |
| `yfinance-data` | ticker 抽出後、上場済銘柄の価格・時価総額・出来高・earnings 日程取得 |
| `telegram-news` | 補助 (アジア圏報道・暗号 RWA 系チャンネル) |
| `generative-ui` | ダッシュボード / HTML page の図表生成 |
| `options-payoff` | (今は不使用。将来「監視リスト言及銘柄でのオプション戦略可視化」に拡張可) |

データ取得は **Skill 経由** で、分析・抽出・統合ロジックは **Claude/コード側** で実装する。

## twitter 監視リスト (初期18人)

`config/watchlist.json` で管理。リストは継続更新可能。

| カテゴリ | アカウント | 注目領域 |
|---------|----------|---------|
| マクロ・センチメント | `@KobeissiLetter` | マクロ・市場全般 |
| 半導体 / AI ハードウェア | `@Doug_OLaughlin`, `@SemiAnalysis_`, `@dnystedt` | キオクシア・Micron・NVDA・台湾サプライチェーン |
| ニッチグロース / 中小型株 | `@InTheAssembly`, `@NoLimitGains`, `@hkuppy`, `@unusual_whales`, `@KuminderD` | スペース・防衛・小型グロース |
| SaaS / クラウド | `@jaminball`, `@public_comps`, `@sammccrear` | SaaS バリュエーション |
| 中国 / アジア株 | `@Sino_Market` | 中国株・香港 |
| 株式トークン化 (L1) | `@BackedFi`, `@dinari_io`, `@OndoFinance` | xStocks / dStocks / RWA |
| IPO onchain (L2) | `@backpack`, `@Superstate_eco` | IPO Onchain |

(将来は監視リストごとに weight を持たせて mention 重み付け予定。初期は単純カウント。)

## データ取得フロー

```
[1] twitter 監視リスト config/watchlist.json を直近24h スキャン
        ↓ twitter Skill
[2] 各 post から ticker 抽出 ($XXX / 大文字3-5字 + 文脈フィルタ)
        ↓ scripts/extract_tickers.py
[3] ticker ごとに集計 (mention_count, source list, context, url)
        ↓
[4a] 上場 ticker → yfinance-data で財務取得 (price / mcap / volume / earnings)
[4b] 未上場 ticker → WebSearch で IPO 状況確認
        ↓
[5] 各 ticker でトークン化状況確認 (data/tokenized-issuers.json と join)
        ↓ WebSearch (週1更新)
[6] 一次発行 (Backpack IPOs Onchain) 対象か確認 (data/primary-issuance.json と join)
        ↓ WebSearch (週1更新)
[7] outputs/daily-stock-data-YYYY-MM-DD.json 生成
        ↓
[8] x402 endpoint (Vercel side, 別 repo) で配信
```

## ディレクトリ構造

```
.
├── CLAUDE.md                              # このファイル
├── config/
│   └── watchlist.json                     # 監視リスト 18 アカウント
├── data/
│   ├── tokenized-issuers.json             # xStocks/Backed/Dinari/Ondo 銘柄リスト (週1更新)
│   └── primary-issuance.json              # Backpack IPOs Onchain 等 (週1更新)
├── scripts/
│   ├── extract_tickers.py                 # post → ticker 抽出 (正規表現+文脈フィルタ)
│   ├── enrich_tickers.py                  # yfinance + WebSearch で各 ticker 補強
│   └── build_daily_dataset.py             # 統合 JSON ビルダー
├── outputs/
│   └── daily-stock-data-YYYY-MM-DD.json   # 日次成果物
├── analyses/
│   └── YYYY-MM-DD-test-run.md             # テストランの分析記録
└── api-design/
    └── endpoints.md                       # x402 endpoint 設計メモ
```

## データ構造 (出力 JSON)

```json
{
  "date": "2026-05-23",
  "generated_at": "2026-05-23T23:59:59Z",
  "tickers": [
    {
      "ticker": "NVDA",
      "company_name": "NVIDIA Corporation",
      "listing_market": "NASDAQ",
      "is_listed": true,
      "price_usd": "...",
      "price_change_24h_pct": "...",
      "market_cap_usd": "...",
      "volume_24h": "...",
      "earnings_date_next": "...",
      "mentions_24h": [
        {
          "source": "@Doug_OLaughlin",
          "url": "https://x.com/...",
          "timestamp": "2026-05-23T14:23:00Z",
          "context": "NVDA Blackwell ramp accelerating..."
        }
      ],
      "mention_count": 5,
      "tokenized_versions": [
        {
          "issuer": "Backed Finance (xStocks)",
          "symbol": "NVDAx",
          "chain": "Solana",
          "contract_address": "...",
          "model": "Freely Transferable",
          "venues": ["Kraken", "Bybit", "Jupiter", "Raydium"]
        }
      ],
      "primary_issuance_available": false
    },
    {
      "ticker": "SPCX",
      "company_name": "SpaceX",
      "listing_market": "NASDAQ (planned 2026-06-12)",
      "is_listed": false,
      "mentions_24h": [
        {
          "source": "@InTheAssembly",
          "url": "...",
          "timestamp": "...",
          "context": "..."
        }
      ],
      "mention_count": 1,
      "tokenized_versions": [],
      "primary_issuance_available": true,
      "primary_issuance_platforms": [
        {
          "platform": "Backpack IPOs Onchain",
          "partner": "Superstate × Solana",
          "status": "waitlist open"
        }
      ]
    }
  ]
}
```

## API 設計案 (実装は別 repo / Vercel 側で後日)

| Endpoint | 用途 |
|----------|------|
| `GET /api/daily-watchlist?date=YYYY-MM-DD` | 指定日の watchlist 言及銘柄一覧 |
| `GET /api/stocks/:ticker` | 個別 ticker の最新情報 |
| `GET /api/stocks?tokenized=true` | トークン化対象のみフィルタ |
| `GET /api/stocks?primary_issuance=available` | IPO onchain アロケーション可能のみ |

### アクセス制御

| クライアント種別 | 判定 | 課金 |
|----------------|------|------|
| エージェント (Bot / AI Agent) | User-Agent / `Accept: application/json` | **$0.01 / call** (Base USDC・x402) |
| ブラウザ (人間) | `Accept: text/html` | **無料 HTML ページ** |

## 実装ステップ進捗

- [x] Step 1: 旧プロジェクト archive ブランチ退避
- [x] Step 2: 新 CLAUDE.md 作成 (本ファイル)
- [ ] Step 3: twitter Skill セットアップ + `config/watchlist.json`
- [ ] Step 4: ticker 抽出ロジック (`scripts/extract_tickers.py`)
- [ ] Step 5: トークン化発行体リスト (`data/tokenized-issuers.json`)
- [ ] Step 6: 一次発行情報 (`data/primary-issuance.json`)
- [ ] Step 7: 統合 JSON ビルダー (`scripts/build_daily_dataset.py`)
- [ ] Step 8: 2026-05-23 test run (`analyses/2026-05-23-test-run.md`)

## 注意事項

1. **地域制限**: xStocks は米英加豪EU 居住者は利用不可。Backpack IPOs Onchain も eligibility 要件あり (waitlist)。「API は情報提供のみ、購入経路は各 platform の eligibility 確認が必要」と明記する。
2. **投資助言ではない**: データ統合 API。トレード判断材料ではない旨を全 endpoint レスポンスに含める。
3. **監視リスト更新**: `config/watchlist.json` を編集するだけで反映。GitHub PR 経由で公開 contribution も将来受け付け可。
4. **トークン化対象範囲**: xStocks / Backed Base / Dinari / Ondo の正規データのみを正とし、二次的取引所が独自ラップした派生トークンは含めない (発行体非公式は除外)。
5. **誤検出**: 「$5」「$10」等の通貨表記、`$EARNINGS` 等の AAVE 文化的記号、`USD` `EPS` `EBITDA` 等の財務頭字語は ticker 候補から除外する。
6. **rate limit**: twitter Skill が叩く API rate limit (Twitter API v2 / scraping いずれか) は要監視。x402 観測対象。

## x402 接続観察ポイント

本プロジェクトは「自分自身が x402 endpoint を出す側」なので観察視点が前回までと異なる。

### 観察対象
- twitter Skill の API rate limit / コスト (Twitter API v2 paid tier 必須か)
- yfinance の rate limit (大量 ticker 取得時)
- WebSearch 結果の更新タイミング (xStocks / Dinari の新規上場 ticker)
- secondary trading データ (Forge / EquityZen / Hiive 等の未上場流通) — 無料 API なし、x402 化候補
- onchain price feed (Pyth / Chainlink) との将来統合

## 関連リソース

- himself65/finance-skills: https://github.com/himself65/finance-skills
- xStocks (Backed Finance Solana): https://xstocks.fi
- Backed Finance (Base): https://backed.fi
- Dinari: https://dinari.com
- Ondo Finance: https://ondo.finance
- Backpack IPOs Onchain: https://backpack.exchange/ipo-access
- Superstate: https://superstate.com
- x402 Inc.: https://x402jp.com
- x402 Inc. note: https://note.com/x402inc

## オーナー

Katomasa (x402 Inc.) — hello@x402jp.com

## 更新履歴

- 2026-05-23: 旧 Unicorn Valuation Compression プロジェクトから方向転換。新企画 (Onchain Stock Data) として再スタート。旧プロジェクトは `archive/unicorn-valuation-compression` ブランチに退避済み。
