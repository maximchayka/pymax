"""Subscription API methods."""

from __future__ import annotations

from typing import TYPE_CHECKING

from maxbot.schemes import (
    GetSubscriptionsResult,
    SimpleQueryResult,
    SubscriptionRequestBody,
)

if TYPE_CHECKING:
    from maxbot.client import AsyncClient, Client


class Subscriptions:
    """Subscription (webhook) management API."""

    def __init__(self, client: "Client") -> None:
        self._client = client

    def get_subscriptions(self) -> GetSubscriptionsResult:
        """Get all active subscriptions.

        Returns:
            List of subscriptions
        """
        return self._client.request_model("GET", "subscriptions", GetSubscriptionsResult)

    def subscribe(
        self,
        url: str,
        update_types: list[str] | None = None,
        secret: str | None = None,
    ) -> SimpleQueryResult:
        """Subscribe to receive updates via webhook.

        Args:
            url: Webhook URL
            update_types: Types of updates to receive
            secret: Secret for webhook verification

        Returns:
            Operation result
        """
        body = SubscriptionRequestBody(
            url=url,
            update_types=update_types,
            version=self._client.api_version,
            secret=secret,
        )
        return self._client.request_model("POST", "subscriptions", SimpleQueryResult, body=body)

    def unsubscribe(self, url: str) -> SimpleQueryResult:
        """Unsubscribe from receiving updates.

        Args:
            url: Webhook URL to unsubscribe

        Returns:
            Operation result
        """
        params = {"url": url}
        return self._client.request_model(
            "DELETE", "subscriptions", SimpleQueryResult, params=params
        )


class AsyncSubscriptions:
    """Async subscription management API."""

    def __init__(self, client: "AsyncClient") -> None:
        self._client = client

    async def get_subscriptions(self) -> GetSubscriptionsResult:
        """Get all active subscriptions."""
        return await self._client.request_model("GET", "subscriptions", GetSubscriptionsResult)

    async def subscribe(
        self,
        url: str,
        update_types: list[str] | None = None,
        secret: str | None = None,
    ) -> SimpleQueryResult:
        """Subscribe to receive updates via webhook."""
        body = SubscriptionRequestBody(
            url=url,
            update_types=update_types,
            version=self._client.api_version,
            secret=secret,
        )
        return await self._client.request_model(
            "POST", "subscriptions", SimpleQueryResult, body=body
        )

    async def unsubscribe(self, url: str) -> SimpleQueryResult:
        """Unsubscribe from receiving updates."""
        params = {"url": url}
        return await self._client.request_model(
            "DELETE", "subscriptions", SimpleQueryResult, params=params
        )
