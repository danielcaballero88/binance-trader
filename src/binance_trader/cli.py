"""Command line interface for quick Binance API interactions.

Provides simple commands: `ping`, `time`, and `exchange-info`.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Optional

from .clients.binance.client import BinanceClient
from .clients.requester.httpx_requester import HttpxRequester
from .clients.requester.requests_requester import RequestsRequester


def _build_requester(name: str, timeout: Optional[float] = None):
    if name == "httpx":
        return HttpxRequester()
    return RequestsRequester()


def main(argv: Optional[list[str]] = None) -> int:  # pragma: no cover - CLI
    parser = argparse.ArgumentParser(prog="binance-trader")
    parser.add_argument("--base-url", default="https://api.binance.com")
    parser.add_argument(
        "--requester", choices=["requests", "httpx"], default="requests"
    )
    parser.add_argument("--timeout", type=float, default=None)

    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ping", help="Test connectivity to the REST API")
    sub.add_parser("time", help="Get server time")
    ex = sub.add_parser("exchange-info", help="Get exchange information")
    ex.add_argument("--symbol", help="Filter by symbol (e.g. BTCUSDT)")

    args = parser.parse_args(argv)

    requester = _build_requester(args.requester, timeout=args.timeout)
    client = BinanceClient(requester, base_url=args.base_url)

    try:
        if args.cmd == "ping":
            res = client.ping()
        elif args.cmd == "time":
            res = client.time()
        elif args.cmd == "exchange-info":
            res = client.exchange_info(symbol=args.symbol)
        else:
            parser.error("unknown command")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    try:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except (TypeError, ValueError):
        print(res)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
