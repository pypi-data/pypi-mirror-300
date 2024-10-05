from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.playlist_search_response import PlaylistSearchResponse
from ...types import Response


def _get_kwargs(
    user_id: int,
    page: int,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/playlists/user/{user_id}/{page}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[PlaylistSearchResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PlaylistSearchResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PlaylistSearchResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: int,
    page: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[PlaylistSearchResponse]:
    """Get playlists by user

    Args:
        user_id (int):
        page (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlaylistSearchResponse]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        page=page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: int,
    page: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[PlaylistSearchResponse]:
    """Get playlists by user

    Args:
        user_id (int):
        page (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PlaylistSearchResponse
    """

    return sync_detailed(
        user_id=user_id,
        page=page,
        client=client,
    ).parsed


async def asyncio_detailed(
    user_id: int,
    page: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[PlaylistSearchResponse]:
    """Get playlists by user

    Args:
        user_id (int):
        page (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlaylistSearchResponse]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        page=page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: int,
    page: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[PlaylistSearchResponse]:
    """Get playlists by user

    Args:
        user_id (int):
        page (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PlaylistSearchResponse
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            page=page,
            client=client,
        )
    ).parsed
