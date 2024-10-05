from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.follower_type import FollowerType
from ...models.player_follower import PlayerFollower
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    type: Union[Unset, FollowerType] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["page"] = page

    params["count"] = count

    json_type: Union[Unset, str] = UNSET
    if not isinstance(type, Unset):
        json_type = type.value

    params["type"] = json_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/player/{id}/followers",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["PlayerFollower"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.text
        for response_200_item_data in _response_200:
            response_200_item = PlayerFollower.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, List["PlayerFollower"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    type: Union[Unset, FollowerType] = UNSET,
) -> Response[Union[Any, List["PlayerFollower"]]]:
    """Get player's full follower list

     Retrieves a full list of player' followers and players this player follow.

    Args:
        id (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        type (Union[Unset, FollowerType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['PlayerFollower']]]
    """

    kwargs = _get_kwargs(
        id=id,
        page=page,
        count=count,
        type=type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    type: Union[Unset, FollowerType] = UNSET,
) -> Optional[Union[Any, List["PlayerFollower"]]]:
    """Get player's full follower list

     Retrieves a full list of player' followers and players this player follow.

    Args:
        id (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        type (Union[Unset, FollowerType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['PlayerFollower']]
    """

    return sync_detailed(
        id=id,
        client=client,
        page=page,
        count=count,
        type=type,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    type: Union[Unset, FollowerType] = UNSET,
) -> Response[Union[Any, List["PlayerFollower"]]]:
    """Get player's full follower list

     Retrieves a full list of player' followers and players this player follow.

    Args:
        id (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        type (Union[Unset, FollowerType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['PlayerFollower']]]
    """

    kwargs = _get_kwargs(
        id=id,
        page=page,
        count=count,
        type=type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    type: Union[Unset, FollowerType] = UNSET,
) -> Optional[Union[Any, List["PlayerFollower"]]]:
    """Get player's full follower list

     Retrieves a full list of player' followers and players this player follow.

    Args:
        id (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        type (Union[Unset, FollowerType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['PlayerFollower']]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            page=page,
            count=count,
            type=type,
        )
    ).parsed
