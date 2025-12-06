from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Requester(ABC):
    """Abstract requester interface used by API clients.

    Implementations must raise on transport-level errors (e.g. non-2xx responses)
    and return either parsed JSON or raw text where appropriate.
    """

    @abstractmethod
    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:  # pragma: no cover - interface
        raise NotImplementedError

    @abstractmethod
    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:  # pragma: no cover - interface
        raise NotImplementedError
