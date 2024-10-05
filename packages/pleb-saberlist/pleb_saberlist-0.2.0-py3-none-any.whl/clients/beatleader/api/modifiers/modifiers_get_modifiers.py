from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.legacy_modifiers import LegacyModifiers
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/modifiers",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[LegacyModifiers]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LegacyModifiers.from_dict(response.text)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[LegacyModifiers]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[LegacyModifiers]:
    """Retrieve Legacy Modifiers

     Provides a list of Beat Saber modifiers and their associated score multiplier values. This is legacy
    support, for the recent values please use `modifierValues` and `modifierRatings` on leaderboards.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LegacyModifiers]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[LegacyModifiers]:
    """Retrieve Legacy Modifiers

     Provides a list of Beat Saber modifiers and their associated score multiplier values. This is legacy
    support, for the recent values please use `modifierValues` and `modifierRatings` on leaderboards.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LegacyModifiers
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[LegacyModifiers]:
    """Retrieve Legacy Modifiers

     Provides a list of Beat Saber modifiers and their associated score multiplier values. This is legacy
    support, for the recent values please use `modifierValues` and `modifierRatings` on leaderboards.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LegacyModifiers]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[LegacyModifiers]:
    """Retrieve Legacy Modifiers

     Provides a list of Beat Saber modifiers and their associated score multiplier values. This is legacy
    support, for the recent values please use `modifierValues` and `modifierRatings` on leaderboards.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LegacyModifiers
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
