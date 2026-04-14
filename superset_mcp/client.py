"""Superset API client with automatic JWT auth and token refresh."""

import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()


class SupersetClient:
    def __init__(self) -> None:
        self._access_token: str | None = None
        self._csrf_token: str | None = None
        self._http = httpx.Client(timeout=30)
        # Resolved lazily so missing env vars only fail at first API call
        self._base_url: str | None = None
        self._username: str | None = None
        self._password: str | None = None
        self._provider: str | None = None

    @property
    def base_url(self) -> str:
        if self._base_url is None:
            url = os.environ.get("SUPERSET_URL")
            if not url:
                raise RuntimeError("SUPERSET_URL environment variable is not set. Check your .env file.")
            self._base_url = url.rstrip("/")
        return self._base_url

    @property
    def username(self) -> str:
        if self._username is None:
            self._username = os.environ.get("SUPERSET_USERNAME", "admin")
        return self._username

    @property
    def password(self) -> str:
        if self._password is None:
            self._password = os.environ.get("SUPERSET_PASSWORD", "")
        return self._password

    @property
    def provider(self) -> str:
        if self._provider is None:
            self._provider = os.environ.get("SUPERSET_PROVIDER", "db")
        return self._provider

    def _login(self) -> None:
        resp = self._http.post(
            f"{self.base_url}/api/v1/security/login",
            json={
                "username": self.username,
                "password": self.password,
                "provider": self.provider,
                "refresh": True,
            },
        )
        resp.raise_for_status()
        self._access_token = resp.json()["access_token"]

    def _get_csrf_token(self) -> str:
        resp = self._request("GET", "/api/v1/security/csrf_token/")
        return resp["result"]

    def _headers(self, with_csrf: bool = False) -> dict[str, str]:
        if not self._access_token:
            self._login()
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
        }
        if with_csrf:
            if not self._csrf_token:
                self._csrf_token = self._get_csrf_token()
            headers["X-CSRFToken"] = self._csrf_token
        return headers

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: dict | None = None,
        with_csrf: bool = False,
        retry: bool = True,
    ) -> Any:
        url = f"{self.base_url}{path}"
        try:
            resp = self._http.request(
                method,
                url,
                headers=self._headers(with_csrf=with_csrf),
                json=json,
                params=params,
            )
            if resp.status_code == 401 and retry:
                # Token expired — re-login once
                self._access_token = None
                self._csrf_token = None
                return self._request(method, path, json=json, params=params, with_csrf=with_csrf, retry=False)
            resp.raise_for_status()
            if resp.content:
                return resp.json()
            return {}
        except httpx.HTTPStatusError as e:
            try:
                detail = e.response.json()
            except Exception:
                detail = e.response.text
            raise RuntimeError(f"Superset API error {e.response.status_code}: {detail}") from e

    def get(self, path: str, params: dict | None = None) -> Any:
        return self._request("GET", path, params=params)

    def post(self, path: str, json: Any = None, with_csrf: bool = True) -> Any:
        return self._request("POST", path, json=json, with_csrf=with_csrf)

    def put(self, path: str, json: Any = None, with_csrf: bool = True) -> Any:
        return self._request("PUT", path, json=json, with_csrf=with_csrf)

    def delete(self, path: str, with_csrf: bool = True) -> Any:
        return self._request("DELETE", path, with_csrf=with_csrf)


# Shared singleton — server.py imports this
client = SupersetClient()
