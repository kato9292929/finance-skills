#!/usr/bin/env python3
"""
Enrich extracted tickers with financial data.

Two backends:
  * --backend yfinance : Uses yfinance python lib (intended for the user's
    local Mac. Requires the runtime to have outbound access to
    query{1,2}.finance.yahoo.com. Fails in network-restricted sandboxes.)
  * --backend manual   : Reads pre-built enrichment from --manual-file.
    Useful when yfinance is unavailable and data has been collected via
    WebSearch or another path.

The output schema matches what build_daily_dataset.py expects to find at
outputs/yfinance-enrichment-<date>.json.

Usage:
    # On the user's Mac (with network)
    python scripts/enrich_tickers.py \
        --extracted outputs/extracted-tickers-2026-05-23.json \
        --output    outputs/yfinance-enrichment-2026-05-23.json \
        --backend   yfinance

    # In sandbox / fallback (manual WebSearch results)
    python scripts/enrich_tickers.py \
        --extracted outputs/extracted-tickers-2026-05-23.json \
        --output    outputs/yfinance-enrichment-2026-05-23.json \
        --backend   manual \
        --manual-file data/manual-enrichment-2026-05-23.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def fetch_yfinance(ticker: str) -> dict | None:
    try:
        import yfinance as yf
    except ImportError:
        print(f"  [skip] yfinance not installed", file=sys.stderr)
        return None

    try:
        t = yf.Ticker(ticker)
        fi = t.fast_info
        info = t.info or {}
        price = fi.last_price
        prev = fi.previous_close
        change_pct = None
        if price is not None and prev:
            change_pct = round((price - prev) / prev * 100, 2)

        next_earnings = None
        try:
            cal = t.calendar
            if cal is not None and "Earnings Date" in cal:
                ed = cal["Earnings Date"]
                if hasattr(ed, "__iter__") and len(ed):
                    next_earnings = str(ed[0])
                elif ed:
                    next_earnings = str(ed)
        except Exception:
            pass

        return {
            "ticker": ticker,
            "company_name": info.get("longName") or info.get("shortName"),
            "listing_market": info.get("exchange") or info.get("fullExchangeName"),
            "price_usd": f"{price:.2f}" if price else None,
            "price_change_24h_pct": f"{change_pct:+.2f}" if change_pct is not None else None,
            "market_cap_usd": str(fi.market_cap) if fi.market_cap else None,
            "volume_24h": str(fi.last_volume) if fi.last_volume else None,
            "earnings_date_next": next_earnings,
            "_backend": "yfinance",
        }
    except Exception as e:
        print(f"  [fail] {ticker}: {e}", file=sys.stderr)
        return None


def load_manual(path: Path) -> dict[str, dict]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return {row["ticker"].upper(): row for row in data.get("tickers", [])}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extracted", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--backend", choices=["yfinance", "manual"], default="yfinance")
    parser.add_argument("--manual-file", type=Path, help="Path to manual enrichment JSON (required if --backend manual)")
    args = parser.parse_args(argv)

    with args.extracted.open(encoding="utf-8") as f:
        extracted = json.load(f)

    manual_map: dict[str, dict] = {}
    if args.backend == "manual":
        if not args.manual_file:
            print("ERROR: --manual-file required with --backend manual", file=sys.stderr)
            return 2
        manual_map = load_manual(args.manual_file)

    enriched: list[dict] = []
    missing: list[str] = []

    for row in extracted.get("tickers", []):
        ticker = row["ticker"].upper()
        if args.backend == "yfinance":
            data = fetch_yfinance(ticker)
        else:
            data = manual_map.get(ticker)
            if data:
                data = {**data, "_backend": "manual"}

        if data is None:
            missing.append(ticker)
        else:
            enriched.append(data)

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "backend": args.backend,
        "ticker_count": len(enriched),
        "missing_count": len(missing),
        "missing_tickers": missing,
        "tickers": enriched,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(
        f"Enriched {len(enriched)} tickers ({len(missing)} missing) via {args.backend} → {args.output}"
    )
    if missing:
        print(f"Missing: {missing}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
