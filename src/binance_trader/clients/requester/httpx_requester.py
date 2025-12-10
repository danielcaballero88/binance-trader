"""HTTPX-backed Requester implementation that supports sync and async usage.

The public methods (`get`, `post`) are dual-mode:
- If called from synchronous code they perform a blocking, synchronous request
  and return the result.
- If called from within an active asyncio event loop they return an awaitable
  coroutine which the caller should `await`.

This keeps a persistent `httpx.Client` and `httpx.AsyncClient` for efficiency.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

import httpx

from .base import Requester


class HttpxRequester(Requester):
    """Adapter around `httpx.Client` / `httpx.AsyncClient`.

    Use the same method names for sync and async: in async contexts the
    methods return a coroutine; in sync contexts they return the final
    result.
    """

    def __init__(
        self,
        client: Optional[httpx.Client] = None,
        async_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self._client = client or httpx.Client()
        self._async_client = async_client or httpx.AsyncClient()

    def _handle_response(self, resp: httpx.Response) -> Any:
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            return resp.text

    def _sync_request(self, method: str, url: str, **kwargs) -> Any:
        resp = self._client.request(method, url, **kwargs)
        return self._handle_response(resp)

    async def _async_request(self, method: str, url: str, **kwargs) -> Any:
        resp = await self._async_client.request(method, url, **kwargs)
        return self._handle_response(resp)

    def _maybe_async_request(self, method: str, url: str, **kwargs) -> Any:
        """Return a coroutine in async context, otherwise perform sync request."""
        try:
            asyncio.get_running_loop()
            return self._async_request(method, url, **kwargs)
        except RuntimeError:
            return self._sync_request(method, url, **kwargs)

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        return self._maybe_async_request(
            "GET", url, params=params, headers=headers, timeout=timeout
        )

    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        return self._maybe_async_request(
            "POST",
            url,
            data=data,
            json=json,
            headers=headers,
            timeout=timeout,
        )
