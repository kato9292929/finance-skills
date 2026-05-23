#!/usr/bin/env python3
"""
Extract ticker mentions from a list of twitter posts.

Input  : JSON list of posts (output from `twitter` Skill)
Output : per-ticker aggregation (mention_count, sources, contexts, urls)

Usage:
    python scripts/extract_tickers.py \
        --posts data/twitter-posts-2026-05-23.json \
        --config config/watchlist.json \
        --output data/extracted-tickers-2026-05-23.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def load_config(config_path: Path) -> dict:
    with config_path.open(encoding="utf-8") as f:
        return json.load(f)


def load_posts(posts_path: Path) -> list[dict]:
    """
    Expected post schema:
        {
          "id": "1795...",
          "author": "@Doug_OLaughlin",
          "text": "Loving the $NVDA Blackwell ramp...",
          "url":  "https://x.com/Doug_OLaughlin/status/1795...",
          "created_at": "2026-05-23T14:23:00Z"
        }
    """
    with posts_path.open(encoding="utf-8") as f:
        return json.load(f)


def build_candidate_set(text: str, patterns: list[str]) -> set[str]:
    candidates: set[str] = set()
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            candidates.add(match.group(1))
    return candidates


def is_dollar_amount(text: str, ticker: str) -> bool:
    """Reject e.g. $5, $5.00, $5B, $5M — these are not tickers."""
    pattern = rf"\${re.escape(ticker)}\b"
    for match in re.finditer(pattern, text):
        start = match.start()
        if start + 1 < len(text) and text[start + 1].isdigit():
            return True
    digit_after = re.search(rf"\${ticker[0]}", text)
    if digit_after is None and ticker and ticker[0].isdigit():
        return True
    return False


def extract_context(text: str, ticker: str, window: int = 60) -> str:
    """Return a window of characters around the first ticker occurrence."""
    pattern = rf"(?:\${re.escape(ticker)}|\b{re.escape(ticker)}\b)"
    m = re.search(pattern, text)
    if not m:
        return text[:window].strip()
    start = max(0, m.start() - window)
    end = min(len(text), m.end() + window)
    return text[start:end].strip()


def extract_tickers(posts: list[dict], config: dict) -> dict:
    extraction = config["ticker_extraction"]
    patterns = extraction["patterns"]
    exclude_words: set[str] = {w.upper() for w in extraction["exclude_words"]}
    min_count = extraction.get("min_mention_count_to_include", 1)

    account_weights: dict[str, float] = {
        a["handle"]: a.get("weight", 1.0) for a in config["accounts"]
    }

    per_ticker: dict[str, dict] = defaultdict(
        lambda: {
            "mention_count": 0,
            "weighted_mention_count": 0.0,
            "mentions": [],
            "sources": set(),
        }
    )

    for post in posts:
        text = post.get("text", "") or ""
        author = post.get("author", "")
        candidates = build_candidate_set(text, patterns)
        for token in candidates:
            ticker = token.upper()
            if ticker in exclude_words:
                continue
            if len(ticker) < 1 or len(ticker) > 5:
                continue
            if is_dollar_amount(text, ticker):
                continue
            entry = per_ticker[ticker]
            entry["mention_count"] += 1
            entry["weighted_mention_count"] += account_weights.get(author, 1.0)
            entry["sources"].add(author)
            entry["mentions"].append(
                {
                    "source": author,
                    "url": post.get("url"),
                    "timestamp": post.get("created_at"),
                    "context": extract_context(text, ticker),
                }
            )

    result = {}
    for ticker, entry in per_ticker.items():
        if entry["mention_count"] < min_count:
            continue
        result[ticker] = {
            "ticker": ticker,
            "mention_count": entry["mention_count"],
            "weighted_mention_count": round(entry["weighted_mention_count"], 3),
            "unique_sources": sorted(entry["sources"]),
            "mentions": entry["mentions"],
        }

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "post_count": len(posts),
        "ticker_count": len(result),
        "tickers": sorted(result.values(), key=lambda t: -t["weighted_mention_count"]),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--posts", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)

    config = load_config(args.config)
    posts = load_posts(args.posts)
    payload = extract_tickers(posts, config)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(
        f"Extracted {payload['ticker_count']} tickers from {payload['post_count']} posts → {args.output}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
