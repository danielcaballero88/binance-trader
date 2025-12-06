"""Requester subpackage: abstracts HTTP client implementation."""

from .base import Requester
from .requests_requester import RequestsRequester

__all__ = ["Requester", "RequestsRequester"]
