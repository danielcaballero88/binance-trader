"""CLI for quick Binance API interactions.

Uses `typer` for nicer help, automatic validation, and easy completion support.
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from .clients.binance.client import BinanceClient
from .clients.requester.httpx_requester import HttpxRequester
from .clients.requester.requests_requester import RequestsRequester

app = typer.Typer(help="Interact with the Binance public REST API")


def _build_requester(name: str):
    if name == "httpx":
        return HttpxRequester()
    return RequestsRequester()


@app.command()
def ping(
    base_url: str = typer.Option("https://api.binance.com", help="Binance base URL"),
    requester: str = typer.Option("requests", help="Requester backend: requests|httpx"),
    timeout: Optional[float] = typer.Option(None, help="Request timeout in seconds"),
):
    """Test connectivity to the REST API."""
    req = _build_requester(requester)
    client = BinanceClient(req, base_url=base_url, timeout=timeout)
    res = client.ping()
    typer.echo(json.dumps(res, indent=2, ensure_ascii=False))


@app.command()
def time(
    base_url: str = typer.Option("https://api.binance.com", help="Binance base URL"),
    requester: str = typer.Option("requests", help="Requester backend: requests|httpx"),
    timeout: Optional[float] = typer.Option(None, help="Request timeout in seconds"),
):
    """Get server time."""
    req = _build_requester(requester)
    client = BinanceClient(req, base_url=base_url, timeout=timeout)
    res = client.time()
    typer.echo(json.dumps(res, indent=2, ensure_ascii=False))


@app.command("exchange-info")
def exchange_info(
    symbol: Optional[str] = typer.Option(None, help="Filter by symbol (e.g. BTCUSDT)"),
    base_url: str = typer.Option("https://api.binance.com", help="Binance base URL"),
    requester: str = typer.Option("requests", help="Requester backend: requests|httpx"),
    timeout: Optional[float] = typer.Option(None, help="Request timeout in seconds"),
):
    """Get exchange information."""
    req = _build_requester(requester)
    client = BinanceClient(req, base_url=base_url, timeout=timeout)
    res = client.exchange_info(symbol=symbol)
    typer.echo(json.dumps(res, indent=2, ensure_ascii=False))


def main(argv: Optional[list[str]] = None) -> int:  # pragma: no cover - CLI
    app(prog_name="binance-trader", args=argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
