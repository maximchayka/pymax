"""HTTP client for Max Bot API."""

from __future__ import annotations

import json
import logging
from typing import Any, BinaryIO, TypeVar
from urllib.parse import urlencode, urljoin

import httpx
from pydantic import BaseModel

from maxbot.errors import (
    APIError,
    EmptyTokenError,
    InvalidURLError,
    NetworkError,
    SerializationError,
    TimeoutError,
)

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

DEFAULT_TIMEOUT = 30.0
DEFAULT_API_URL = "https://botapi.max.ru/"
VERSION = "1.0.0"


class Client:
    """HTTP client for Max Bot API."""

    def __init__(
        self,
        token: str,
        api_url: str = DEFAULT_API_URL,
        api_version: str = "0.1.2",
        timeout: float = DEFAULT_TIMEOUT,
        http_client: httpx.Client | None = None,
    ) -> None:
        """Initialize the client.

        Args:
            token: Bot API token
            api_url: Base API URL
            api_version: API version
            timeout: Request timeout in seconds
            http_client: Optional custom httpx.Client
        """
        if not token:
            raise EmptyTokenError()

        if not api_url:
            raise InvalidURLError()

        self.token = token
        self.api_url = api_url.rstrip("/") + "/"
        self.api_version = api_version
        self.timeout = timeout

        if http_client is not None:
            self._client = http_client
            self._owns_client = False
        else:
            self._client = httpx.Client(timeout=timeout)
            self._owns_client = True

    def close(self) -> None:
        """Close the HTTP client."""
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    @property
    def _headers(self) -> dict[str, str]:
        """Get default headers."""
        return {
            "User-Agent": f"max-bot-api-python/{VERSION}",
            "Authorization": f"access_token={self.token}",
            "Content-Type": "application/json",
        }

    def _build_url(self, endpoint: str, params: dict[str, Any] | None = None) -> str:
        """Build full URL with query parameters.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Full URL
        """
        url = urljoin(self.api_url, endpoint)
        query_params = {"v": self.api_version}
        if params:
            query_params.update({k: v for k, v in params.items() if v is not None})

        if query_params:
            url = f"{url}?{urlencode(query_params)}"

        return url

    def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        body: BaseModel | dict[str, Any] | None = None,
        use_token_in_url: bool = False,
    ) -> dict[str, Any]:
        """Make HTTP request.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            body: Request body
            use_token_in_url: Whether to put token in URL instead of header

        Returns:
            Response data as dictionary

        Raises:
            APIError: If API returns an error
            NetworkError: If network error occurs
            TimeoutError: If request times out
            SerializationError: If serialization fails
        """
        # Build URL
        url_params = params.copy() if params else {}
        if use_token_in_url:
            url_params["access_token"] = self.token

        url = self._build_url(endpoint, url_params)

        # Build headers
        headers = self._headers.copy()
        if use_token_in_url:
            del headers["Authorization"]

        # Build body
        json_body = None
        if body is not None:
            if isinstance(body, BaseModel):
                json_body = body.model_dump(by_alias=True, exclude_none=True)
            else:
                json_body = body

        try:
            response = self._client.request(
                method=method,
                url=url,
                headers=headers,
                json=json_body,
                timeout=self.timeout,
            )
        except httpx.TimeoutException as e:
            raise TimeoutError(f"{method} {endpoint}", str(e))
        except httpx.RequestError as e:
            raise NetworkError(f"{method} {endpoint}", e)

        # Parse response
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            raise SerializationError("decode", "response", e)

        # Check for errors
        if response.status_code != 200:
            error = data.get("error", data) if isinstance(data, dict) else data
            if isinstance(error, dict):
                raise APIError(
                    code=error.get("code", str(response.status_code)),
                    message=error.get("message", "Unknown error"),
                    details=error.get("details"),
                )
            raise APIError(
                code=str(response.status_code),
                message=str(error),
            )

        return data

    def request_model(
        self,
        method: str,
        endpoint: str,
        model: type[T],
        params: dict[str, Any] | None = None,
        body: BaseModel | dict[str, Any] | None = None,
        use_token_in_url: bool = False,
    ) -> T:
        """Make HTTP request and parse response into a model.

        Args:
            method: HTTP method
            endpoint: API endpoint
            model: Pydantic model class to parse response into
            params: Query parameters
            body: Request body
            use_token_in_url: Whether to put token in URL instead of header

        Returns:
            Parsed response as model instance
        """
        data = self.request(method, endpoint, params, body, use_token_in_url)
        try:
            return model.model_validate(data)
        except Exception as e:
            raise SerializationError("validate", model.__name__, e)

    def upload_file(
        self,
        url: str,
        file: BinaryIO,
        filename: str,
        field_name: str = "data",
    ) -> dict[str, Any]:
        """Upload file using multipart form.

        Args:
            url: Upload URL
            file: File-like object
            filename: Filename
            field_name: Form field name

        Returns:
            Upload response data
        """
        try:
            response = self._client.post(
                url,
                files={field_name: (filename, file)},
                timeout=self.timeout,
            )
        except httpx.TimeoutException as e:
            raise TimeoutError("upload", str(e))
        except httpx.RequestError as e:
            raise NetworkError("upload", e)

        try:
            data = response.json()
        except json.JSONDecodeError as e:
            raise SerializationError("decode", "upload_response", e)

        if response.status_code != 200:
            error = data.get("error", data) if isinstance(data, dict) else data
            if isinstance(error, dict):
                raise APIError(
                    code=error.get("code", str(response.status_code)),
                    message=error.get("message", "Unknown error"),
                    details=error.get("details"),
                )
            raise APIError(code=str(response.status_code), message=str(error))

        return data


class AsyncClient:
    """Async HTTP client for Max Bot API."""

    def __init__(
        self,
        token: str,
        api_url: str = DEFAULT_API_URL,
        api_version: str = "0.1.2",
        timeout: float = DEFAULT_TIMEOUT,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        """Initialize the async client.

        Args:
            token: Bot API token
            api_url: Base API URL
            api_version: API version
            timeout: Request timeout in seconds
            http_client: Optional custom httpx.AsyncClient
        """
        if not token:
            raise EmptyTokenError()

        if not api_url:
            raise InvalidURLError()

        self.token = token
        self.api_url = api_url.rstrip("/") + "/"
        self.api_version = api_version
        self.timeout = timeout

        if http_client is not None:
            self._client = http_client
            self._owns_client = False
        else:
            self._client = httpx.AsyncClient(timeout=timeout)
            self._owns_client = True

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    @property
    def _headers(self) -> dict[str, str]:
        """Get default headers."""
        return {
            "User-Agent": f"max-bot-api-python/{VERSION}",
            "Authorization": f"access_token={self.token}",
            "Content-Type": "application/json",
        }

    def _build_url(self, endpoint: str, params: dict[str, Any] | None = None) -> str:
        """Build full URL with query parameters."""
        url = urljoin(self.api_url, endpoint)
        query_params = {"v": self.api_version}
        if params:
            query_params.update({k: v for k, v in params.items() if v is not None})

        if query_params:
            url = f"{url}?{urlencode(query_params)}"

        return url

    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        body: BaseModel | dict[str, Any] | None = None,
        use_token_in_url: bool = False,
    ) -> dict[str, Any]:
        """Make async HTTP request."""
        url_params = params.copy() if params else {}
        if use_token_in_url:
            url_params["access_token"] = self.token

        url = self._build_url(endpoint, url_params)

        headers = self._headers.copy()
        if use_token_in_url:
            del headers["Authorization"]

        json_body = None
        if body is not None:
            if isinstance(body, BaseModel):
                json_body = body.model_dump(by_alias=True, exclude_none=True)
            else:
                json_body = body

        try:
            response = await self._client.request(
                method=method,
                url=url,
                headers=headers,
                json=json_body,
                timeout=self.timeout,
            )
        except httpx.TimeoutException as e:
            raise TimeoutError(f"{method} {endpoint}", str(e))
        except httpx.RequestError as e:
            raise NetworkError(f"{method} {endpoint}", e)

        try:
            data = response.json()
        except json.JSONDecodeError as e:
            raise SerializationError("decode", "response", e)

        if response.status_code != 200:
            error = data.get("error", data) if isinstance(data, dict) else data
            if isinstance(error, dict):
                raise APIError(
                    code=error.get("code", str(response.status_code)),
                    message=error.get("message", "Unknown error"),
                    details=error.get("details"),
                )
            raise APIError(code=str(response.status_code), message=str(error))

        return data

    async def request_model(
        self,
        method: str,
        endpoint: str,
        model: type[T],
        params: dict[str, Any] | None = None,
        body: BaseModel | dict[str, Any] | None = None,
        use_token_in_url: bool = False,
    ) -> T:
        """Make async HTTP request and parse response into a model."""
        data = await self.request(method, endpoint, params, body, use_token_in_url)
        try:
            return model.model_validate(data)
        except Exception as e:
            raise SerializationError("validate", model.__name__, e)

    async def upload_file(
        self,
        url: str,
        file: BinaryIO,
        filename: str,
        field_name: str = "data",
    ) -> dict[str, Any]:
        """Upload file using multipart form."""
        try:
            response = await self._client.post(
                url,
                files={field_name: (filename, file)},
                timeout=self.timeout,
            )
        except httpx.TimeoutException as e:
            raise TimeoutError("upload", str(e))
        except httpx.RequestError as e:
            raise NetworkError("upload", e)

        try:
            data = response.json()
        except json.JSONDecodeError as e:
            raise SerializationError("decode", "upload_response", e)

        if response.status_code != 200:
            error = data.get("error", data) if isinstance(data, dict) else data
            if isinstance(error, dict):
                raise APIError(
                    code=error.get("code", str(response.status_code)),
                    message=error.get("message", "Unknown error"),
                    details=error.get("details"),
                )
            raise APIError(code=str(response.status_code), message=str(error))

        return data
