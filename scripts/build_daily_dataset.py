#!/usr/bin/env python3
"""
Build the daily merged dataset for the Onchain Stock Data API.

Inputs:
  - data/extracted-tickers-YYYY-MM-DD.json   (output of extract_tickers.py)
  - data/yfinance-enrichment-YYYY-MM-DD.json (output of enrich step, see schema)
  - data/tokenized-issuers.json              (master, refreshed weekly)
  - data/primary-issuance.json               (master, refreshed weekly)
  - data/unlisted-context-YYYY-MM-DD.json    (optional, WebSearch outputs for unlisted tickers)

Output:
  - outputs/daily-stock-data-YYYY-MM-DD.json (final merged dataset for the x402 API)

Usage:
    python scripts/build_daily_dataset.py --date 2026-05-23
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def safe_load(path: Path) -> dict | None:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def index_tokenized_by_ticker(tokenized_master: dict) -> dict[str, list[dict]]:
    """
    Build { "TSLA": [{issuer info + token_symbol}, ...] } map.
    """
    by_ticker: dict[str, list[dict]] = {}
    for issuer in tokenized_master.get("issuers", []):
        for kt in issuer.get("known_tickers", []):
            underlying = kt["underlying_ticker"].upper()
            by_ticker.setdefault(underlying, []).append(
                {
                    "issuer": issuer["name"],
                    "issuer_id": issuer["id"],
                    "symbol": kt["token_symbol"],
                    "chain": issuer["primary_chain"],
                    "model": issuer["model"],
                    "venues": (
                        issuer.get("venues_cex", [])
                        + issuer.get("venues_dex_solana", [])
                        + issuer.get("venues_dex_base", [])
                        + issuer.get("venues_eu_regulated", [])
                    ),
                    "geo_restrictions": issuer.get("geo_restrictions", []),
                }
            )
    return by_ticker


def primary_issuance_for_ticker(ticker: str, primary_master: dict) -> list[dict]:
    """
    Backpack IPOs Onchain は ticker 限定の deals_pipeline を持つ。
    現状は pipeline 空なので「対象が waitlist にあるか」で判定。
    将来は deals_pipeline に ticker を追加した時に自動 join される。
    """
    hits = []
    for platform in primary_master.get("platforms", []):
        for deal in platform.get("deals_pipeline", []):
            if deal.get("ticker", "").upper() == ticker.upper():
                hits.append(
                    {
                        "platform": platform["name"],
                        "partner": platform.get("transfer_agent"),
                        "chain": platform["chain"],
                        "status": deal.get("status", platform.get("current_status")),
                    }
                )
    return hits


def merge(
    extracted: dict,
    yfinance: dict | None,
    tokenized_master: dict,
    primary_master: dict,
    unlisted_ctx: dict | None,
    date_str: str,
) -> dict:
    tokenized_index = index_tokenized_by_ticker(tokenized_master)
    yf_index = {row["ticker"].upper(): row for row in (yfinance or {}).get("tickers", [])}
    unlisted_index = {
        row["ticker"].upper(): row for row in (unlisted_ctx or {}).get("tickers", [])
    }

    result_tickers = []
    for entry in extracted.get("tickers", []):
        ticker = entry["ticker"].upper()
        yf = yf_index.get(ticker)
        unlisted = unlisted_index.get(ticker)
        tokenized = tokenized_index.get(ticker, [])
        primary = primary_issuance_for_ticker(ticker, primary_master)

        is_listed = yf is not None
        row = {
            "ticker": ticker,
            "company_name": (yf or unlisted or {}).get("company_name"),
            "listing_market": (yf or unlisted or {}).get("listing_market"),
            "is_listed": is_listed,
            "price_usd": (yf or {}).get("price_usd"),
            "price_change_24h_pct": (yf or {}).get("price_change_24h_pct"),
            "market_cap_usd": (yf or unlisted or {}).get("market_cap_usd"),
            "volume_24h": (yf or {}).get("volume_24h"),
            "earnings_date_next": (yf or {}).get("earnings_date_next"),
            "mentions_24h": entry["mentions"],
            "mention_count": entry["mention_count"],
            "weighted_mention_count": entry["weighted_mention_count"],
            "unique_sources": entry["unique_sources"],
            "tokenized_versions": tokenized,
            "primary_issuance_available": bool(primary),
            "primary_issuance_platforms": primary,
        }
        if unlisted:
            row["unlisted_context"] = {
                "ipo_status": unlisted.get("ipo_status"),
                "notes": unlisted.get("notes"),
                "sources": unlisted.get("sources", []),
            }
        result_tickers.append(row)

    return {
        "date": date_str,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "schema_version": "1.0.0",
        "disclaimer": "Data API only. Not investment advice. xStocks/Backpack IPOs Onchain have geographic eligibility requirements; verify on the platform.",
        "ticker_count": len(result_tickers),
        "tickers": sorted(result_tickers, key=lambda r: -(r["weighted_mention_count"] or 0)),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--data-dir", default=str(ROOT / "data"))
    parser.add_argument("--output-dir", default=str(ROOT / "outputs"))
    args = parser.parse_args(argv)

    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)

    extracted = safe_load(data_dir / f"extracted-tickers-{args.date}.json")
    if extracted is None:
        print(
            f"ERROR: extracted-tickers-{args.date}.json not found. Run extract_tickers.py first.",
            file=sys.stderr,
        )
        return 2

    yfinance = safe_load(data_dir / f"yfinance-enrichment-{args.date}.json")
    unlisted = safe_load(data_dir / f"unlisted-context-{args.date}.json")
    tokenized_master = safe_load(data_dir / "tokenized-issuers.json")
    primary_master = safe_load(data_dir / "primary-issuance.json")

    if tokenized_master is None or primary_master is None:
        print(
            "ERROR: tokenized-issuers.json or primary-issuance.json missing in data/.",
            file=sys.stderr,
        )
        return 2

    payload = merge(extracted, yfinance, tokenized_master, primary_master, unlisted, args.date)

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"daily-stock-data-{args.date}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(
        f"Built dataset for {args.date}: {payload['ticker_count']} tickers → {out_path}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
