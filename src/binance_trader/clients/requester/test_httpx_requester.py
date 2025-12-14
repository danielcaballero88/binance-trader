"""Unit tests for HttpxRequester (sync and async behavior)."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from binance_trader.clients.requester.httpx_requester import HttpxRequester


def test_get_json_response_sync():
    requester = HttpxRequester()
    mock_response = MagicMock()
    mock_response.json.return_value = {"key": "value"}
    mock_response.raise_for_status.return_value = None

    with patch.object(
        requester._client, "request", return_value=mock_response
    ) as mock_request:
        result = requester.get("https://example.com/api/data")

    assert result == {"key": "value"}
    mock_request.assert_called_once_with(
        "GET",
        "https://example.com/api/data",
        params=None,
        headers=None,
        timeout=None,
    )


def test_post_json_response_sync():
    requester = HttpxRequester()
    mock_response = MagicMock()
    mock_response.json.return_value = {"ok": True}
    mock_response.raise_for_status.return_value = None

    with patch.object(
        requester._client, "request", return_value=mock_response
    ) as mock_request:
        result = requester.post("https://example.com/api/orders", json={"a": 1})

    assert result == {"ok": True}
    mock_request.assert_called_once_with(
        "POST",
        "https://example.com/api/orders",
        data=None,
        json={"a": 1},
        headers=None,
        timeout=None,
    )


def test_get_text_fallback_sync():
    requester = HttpxRequester()
    mock_response = MagicMock()
    mock_response.json.side_effect = ValueError("no json")
    mock_response.text = "plain text"
    mock_response.raise_for_status.return_value = None

    with patch.object(requester._client, "request", return_value=mock_response):
        result = requester.get("https://example.com")

    assert result == "plain text"


def test_get_json_response_async():
    requester = HttpxRequester()
    mock_response = MagicMock()
    mock_response.json.return_value = {"key": "value"}
    mock_response.raise_for_status.return_value = None

    async def runner():
        async_mock = AsyncMock(return_value=mock_response)
        with patch.object(requester._async_client, "request", async_mock):
            return await requester.get("https://example.com/api/data")

    result = asyncio.run(runner())
    assert result == {"key": "value"}


def test_post_json_response_async():
    requester = HttpxRequester()
    mock_response = MagicMock()
    mock_response.json.return_value = {"ok": True}
    mock_response.raise_for_status.return_value = None

    async def runner():
        async_mock = AsyncMock(return_value=mock_response)
        with patch.object(requester._async_client, "request", async_mock):
            return await requester.post("https://example.com/api/orders", json={"a": 1})

    result = asyncio.run(runner())
    assert result == {"ok": True}
