from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

from fastapi import FastAPI
from fastapi.testclient import TestClient

from mythic_edge_parser.local_app.backend import (
    GUARDED_MUTATING_API_ROUTES,
    LOCAL_REQUEST_GUARD_HEADER,
)

LOOPBACK_BASE_URL = "http://127.0.0.1:8000"


class GuardedLocalAppTestClient(TestClient):
    _request_guard_headers: dict[str, str] | None = None

    def post(self, url: Any, *args: Any, **kwargs: Any) -> Any:
        if _is_guarded_mutating_path(url):
            headers = dict(kwargs.get("headers") or {})
            headers.setdefault(LOCAL_REQUEST_GUARD_HEADER, self.request_guard_headers()[LOCAL_REQUEST_GUARD_HEADER])
            kwargs["headers"] = headers
        return super().post(url, *args, **kwargs)

    def request_guard_headers(self) -> dict[str, str]:
        if self._request_guard_headers is None:
            self._request_guard_headers = request_guard_headers(self)
        return self._request_guard_headers


def guarded_client(app: FastAPI) -> GuardedLocalAppTestClient:
    return GuardedLocalAppTestClient(app, base_url=LOOPBACK_BASE_URL)


def request_guard_headers(client: TestClient) -> dict[str, str]:
    response = client.get("/api/app/request-guard")
    assert response.status_code == 200
    payload = response.json()
    assert payload["header_name"] == LOCAL_REQUEST_GUARD_HEADER
    return {LOCAL_REQUEST_GUARD_HEADER: payload["token"]}


def _is_guarded_mutating_path(url: object) -> bool:
    return urlsplit(str(url)).path in GUARDED_MUTATING_API_ROUTES
