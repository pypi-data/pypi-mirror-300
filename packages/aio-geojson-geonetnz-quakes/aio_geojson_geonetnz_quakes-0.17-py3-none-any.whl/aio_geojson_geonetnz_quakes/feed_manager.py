"""Feed Manager for GeoNet NZ Quakes feed."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import datetime

from aio_geojson_client.feed_manager import FeedManagerBase
from aio_geojson_client.status_update import StatusUpdate
from aiohttp import ClientSession

from .feed import GeonetnzQuakesFeed


class GeonetnzQuakesFeedManager(FeedManagerBase):
    """Feed Manager for GeoNet NZ Quakes feed."""

    def __init__(
        self,
        websession: ClientSession,
        generate_callback: Callable[[str], Awaitable[None]],
        update_callback: Callable[[str], Awaitable[None]],
        remove_callback: Callable[[str], Awaitable[None]],
        home_coordinates: tuple[float, float],
        mmi: int = -1,
        filter_radius: float | None = None,
        filter_minimum_magnitude: float | None = None,
        filter_time: datetime | None = None,
        status_callback: Callable[[StatusUpdate], Awaitable[None]] | None = None,
    ):
        """Initialize the GeoNet NZ Quakes Feed Manager."""
        feed = GeonetnzQuakesFeed(
            websession,
            home_coordinates,
            mmi=mmi,
            filter_radius=filter_radius,
            filter_minimum_magnitude=filter_minimum_magnitude,
            filter_time=filter_time,
        )
        super().__init__(
            feed, generate_callback, update_callback, remove_callback, status_callback
        )
