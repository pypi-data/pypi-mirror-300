from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.global_map_history import GlobalMapHistory
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: int,
    *,
    count: Union[Unset, int] = 50,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["count"] = count

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/clan/{id}/history",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, List["GlobalMapHistory"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.text
        for response_200_item_data in _response_200:
            response_200_item = GlobalMapHistory.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, List["GlobalMapHistory"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    count: Union[Unset, int] = 50,
) -> Response[Union[Any, List["GlobalMapHistory"]]]:
    """Retrieve clan's statistic history

     Fetches a list of player's performance metrics and various stats saved daily

    Args:
        id (int):
        count (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['GlobalMapHistory']]]
    """

    kwargs = _get_kwargs(
        id=id,
        count=count,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    count: Union[Unset, int] = 50,
) -> Optional[Union[Any, List["GlobalMapHistory"]]]:
    """Retrieve clan's statistic history

     Fetches a list of player's performance metrics and various stats saved daily

    Args:
        id (int):
        count (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['GlobalMapHistory']]
    """

    return sync_detailed(
        id=id,
        client=client,
        count=count,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    count: Union[Unset, int] = 50,
) -> Response[Union[Any, List["GlobalMapHistory"]]]:
    """Retrieve clan's statistic history

     Fetches a list of player's performance metrics and various stats saved daily

    Args:
        id (int):
        count (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, List['GlobalMapHistory']]]
    """

    kwargs = _get_kwargs(
        id=id,
        count=count,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    count: Union[Unset, int] = 50,
) -> Optional[Union[Any, List["GlobalMapHistory"]]]:
    """Retrieve clan's statistic history

     Fetches a list of player's performance metrics and various stats saved daily

    Args:
        id (int):
        count (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, List['GlobalMapHistory']]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            count=count,
        )
    ).parsed
