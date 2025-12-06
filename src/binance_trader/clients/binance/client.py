"""A simple Binance API client using a pluggable `Requester`.

This client intentionally keeps things minimal and synchronous. It expects
an object implementing `Requester` so the HTTP backend can be swapped easily.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..requester import Requester


class BinanceClient:
    """Minimal Binance REST API client.

    Example:
        from binance_trader.clients.requester import RequestsRequester
        from binance_trader.clients.binance import BinanceClient

        req = RequestsRequester()
        client = BinanceClient(req)
        client.ping()
    """

    def __init__(
        self, requester: Requester, base_url: str = "https://api.binance.com"
    ) -> None:
        self._requester = requester
        self.base_url = base_url.rstrip("/")

    def _url(self, path: str) -> str:
        if path.startswith("/"):
            return f"{self.base_url}{path}"
        return f"{self.base_url}/{path}"

    def ping(self) -> Any:
        """Test connectivity to the REST API."""
        return self._requester.get(self._url("/api/v3/ping"))

    def time(self) -> Any:
        """Get server time."""
        return self._requester.get(self._url("/api/v3/time"))

    def exchange_info(self, symbol: Optional[str] = None) -> Any:
        """Get exchange information. Pass `symbol` to filter for a single symbol."""
        params: Optional[Dict[str, Any]] = {"symbol": symbol} if symbol else None
        return self._requester.get(self._url("/api/v3/exchangeInfo"), params=params)
