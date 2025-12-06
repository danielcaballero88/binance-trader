"""Requests-backed Requester implementation."""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from .base import Requester


class RequestsRequester(Requester):
    """A thin adapter around `requests.Session` that implements `Requester`.

    - Raises `requests.HTTPError` on non-2xx responses via `response.raise_for_status()`.
    - Returns parsed JSON when possible, otherwise returns response text.
    """

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()

    def _request(self, method: str, url: str, **kwargs) -> Any:
        resp = self.session.request(method, url, **kwargs)
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            return resp.text

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        return self._request(
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
        return self._request(
            "POST", url, data=data, json=json, headers=headers, timeout=timeout
        )
