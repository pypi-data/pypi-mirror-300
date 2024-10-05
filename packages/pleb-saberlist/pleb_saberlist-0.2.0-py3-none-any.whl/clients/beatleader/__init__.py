"""A client library for accessing BeatLeader API. Get various Beat Saber information."""

from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
)
