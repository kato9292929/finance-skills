# scripts/

| Script | 役割 | 依存 |
|--------|------|-----|
| `extract_tickers.py` | post → ticker 抽出 (正規表現 + exclude_words + dollar-amount filter + 重み付き集計) | stdlib のみ |
| `enrich_tickers.py` (TODO) | 抽出した ticker を `yfinance-data` Skill 経由で財務 enrichment | `yfinance-data` Skill |
| `enrich_unlisted.py` (TODO) | yfinance に無い ticker を WebSearch で補強 (`unlisted-context-*.json` 生成) | WebSearch |
| `build_daily_dataset.py` | 全 input を merge → `outputs/daily-stock-data-YYYY-MM-DD.json` | stdlib のみ |

## 1日のフロー

```bash
# Step A: twitter Skill で直近24h post 取得 (本 repo 外で実行)
# → data/twitter-posts-2026-05-23.json

# Step B: ticker 抽出
python3 scripts/extract_tickers.py \
  --posts data/twitter-posts-2026-05-23.json \
  --config config/watchlist.json \
  --output data/extracted-tickers-2026-05-23.json

# Step C: yfinance enrichment (TODO: enrich_tickers.py 実装後)
# → data/yfinance-enrichment-2026-05-23.json

# Step D: 未上場 context (TODO: enrich_unlisted.py 実装後)
# → data/unlisted-context-2026-05-23.json

# Step E: 統合
python3 scripts/build_daily_dataset.py --date 2026-05-23
# → outputs/daily-stock-data-2026-05-23.json
```

## サンプル実行 (mock データ)

`analyses/2026-05-23-test-run.md` を参照。`data/examples/` に mock 入力一式あり。
