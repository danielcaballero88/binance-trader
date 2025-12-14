"""Unit tests for RequestsRequester."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from binance_trader.clients.requester import RequestsRequester


class TestRequestsRequesterInit:
    """Tests for RequestsRequester initialization."""

    def test_init_with_default_session(self):
        """A default session is created if none is provided."""
        requester = RequestsRequester()
        assert isinstance(requester.session, requests.Session)

    def test_init_with_custom_session(self):
        """A custom session can be provided."""
        custom_session = requests.Session()
        custom_session.headers.update({"X-Custom": "header"})
        requester = RequestsRequester(session=custom_session)
        assert requester.session is custom_session
        assert requester.session.headers.get("X-Custom") == "header"


class TestRequestsRequesterGet:
    """Tests for RequestsRequester.get()."""

    def test_get_json_response(self):
        """GET request returns parsed JSON."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_response.raise_for_status.return_value = None

        with patch.object(
            requester.session, "request", return_value=mock_response
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

    def test_get_with_params(self):
        """GET request passes params to session.request."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "ok"}
        mock_response.raise_for_status.return_value = None

        with patch.object(
            requester.session, "request", return_value=mock_response
        ) as mock_request:
            result = requester.get(
                "https://example.com/api/data",
                params={"symbol": "BTCUSDT", "limit": 10},
            )

        assert result == {"result": "ok"}
        mock_request.assert_called_once_with(
            "GET",
            "https://example.com/api/data",
            params={"symbol": "BTCUSDT", "limit": 10},
            headers=None,
            timeout=None,
        )

    def test_get_with_headers(self):
        """GET request passes headers to session.request."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None

        with patch.object(
            requester.session, "request", return_value=mock_response
        ) as mock_request:
            requester.get(
                "https://example.com/api",
                headers={"Authorization": "Bearer token123"},
            )

        mock_request.assert_called_once_with(
            "GET",
            "https://example.com/api",
            params=None,
            headers={"Authorization": "Bearer token123"},
            timeout=None,
        )

    def test_get_with_timeout(self):
        """GET request passes timeout to session.request."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None

        with patch.object(
            requester.session, "request", return_value=mock_response
        ) as mock_request:
            requester.get("https://example.com/api", timeout=5.0)

        mock_request.assert_called_once_with(
            "GET", "https://example.com/api", params=None, headers=None, timeout=5.0
        )

    def test_get_text_fallback(self):
        """GET returns response text if JSON parsing fails."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("No JSON")
        mock_response.text = "plain text response"
        mock_response.raise_for_status.return_value = None

        with patch.object(requester.session, "request", return_value=mock_response):
            result = requester.get("https://example.com/api")

        assert result == "plain text response"

    def test_get_http_error_raised(self):
        """GET raises HTTPError on non-2xx responses."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

        with patch.object(requester.session, "request", return_value=mock_response):
            with pytest.raises(requests.HTTPError):
                requester.get("https://example.com/notfound")


class TestRequestsRequesterPost:
    """Tests for RequestsRequester.post()."""

    def test_post_json_response(self):
        """POST request returns parsed JSON."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.json.return_value = {"order_id": 123}
        mock_response.raise_for_status.return_value = None

        with patch.object(
            requester.session, "request", return_value=mock_response
        ) as mock_request:
            result = requester.post("https://example.com/api/orders")

        assert result == {"order_id": 123}
        mock_request.assert_called_once_with(
            "POST",
            "https://example.com/api/orders",
            data=None,
            json=None,
            headers=None,
            timeout=None,
        )

    def test_post_with_json_body(self):
        """POST request passes json body to session.request."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True}
        mock_response.raise_for_status.return_value = None

        with patch.object(
            requester.session, "request", return_value=mock_response
        ) as mock_request:
            result = requester.post(
                "https://example.com/api/orders",
                json={"symbol": "BTCUSDT", "side": "BUY", "quantity": 1},
            )

        assert result == {"success": True}
        mock_request.assert_called_once_with(
            "POST",
            "https://example.com/api/orders",
            data=None,
            json={"symbol": "BTCUSDT", "side": "BUY", "quantity": 1},
            headers=None,
            timeout=None,
        )

    def test_post_with_form_data(self):
        """POST request passes form data to session.request."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.raise_for_status.return_value = None

        with patch.object(
            requester.session, "request", return_value=mock_response
        ) as mock_request:
            requester.post("https://example.com/api/submit", data={"field1": "value1"})

        mock_request.assert_called_once_with(
            "POST",
            "https://example.com/api/submit",
            data={"field1": "value1"},
            json=None,
            headers=None,
            timeout=None,
        )

    def test_post_with_headers(self):
        """POST request passes headers to session.request."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None

        with patch.object(
            requester.session, "request", return_value=mock_response
        ) as mock_request:
            requester.post(
                "https://example.com/api/data",
                headers={"X-API-Key": "secret"},
                json={"data": "value"},
            )

        mock_request.assert_called_once_with(
            "POST",
            "https://example.com/api/data",
            data=None,
            json={"data": "value"},
            headers={"X-API-Key": "secret"},
            timeout=None,
        )

    def test_post_with_timeout(self):
        """POST request passes timeout to session.request."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None

        with patch.object(
            requester.session, "request", return_value=mock_response
        ) as mock_request:
            requester.post("https://example.com/api", timeout=10.0)

        mock_request.assert_called_once_with(
            "POST",
            "https://example.com/api",
            data=None,
            json=None,
            headers=None,
            timeout=10.0,
        )

    def test_post_text_fallback(self):
        """POST returns response text if JSON parsing fails."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "HTML error page"
        mock_response.raise_for_status.return_value = None

        with patch.object(requester.session, "request", return_value=mock_response):
            result = requester.post("https://example.com/api")

        assert result == "HTML error page"

    def test_post_http_error_raised(self):
        """POST raises HTTPError on non-2xx responses."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError(
            "500 Internal Server Error"
        )

        with patch.object(requester.session, "request", return_value=mock_response):
            with pytest.raises(requests.HTTPError):
                requester.post("https://example.com/api")


class TestRequestsRequesterIntegration:
    """Integration tests with realistic scenarios."""

    def test_nested_json_response(self):
        """Complex nested JSON responses are parsed correctly."""
        requester = RequestsRequester()
        complex_response = {
            "data": {
                "user": {"id": 1, "name": "Alice"},
                "items": [{"id": 1, "price": 10.5}, {"id": 2, "price": 20.3}],
            }
        }
        mock_response = MagicMock()
        mock_response.json.return_value = complex_response
        mock_response.raise_for_status.return_value = None

        with patch.object(requester.session, "request", return_value=mock_response):
            result = requester.get("https://example.com/api/complex")

        assert result == complex_response
        assert result["data"]["user"]["name"] == "Alice"

    def test_empty_json_response(self):
        """Empty JSON objects and arrays are handled."""
        requester = RequestsRequester()
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None

        with patch.object(requester.session, "request", return_value=mock_response):
            result = requester.get("https://example.com/api")

        assert result == {}

    def test_session_persistence(self):
        """Session state is preserved across multiple requests."""
        session = requests.Session()
        session.headers.update({"Authorization": "Bearer token"})
        requester = RequestsRequester(session=session)

        mock_response = MagicMock()
        mock_response.json.return_value = {"result": 1}
        mock_response.raise_for_status.return_value = None

        with patch.object(session, "request", return_value=mock_response):
            requester.get("https://example.com/api/1")
            requester.get("https://example.com/api/2")

        # Session object should be the same (and headers preserved)
        assert requester.session is session
        assert session.headers.get("Authorization") == "Bearer token"
