from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.order import Order
from ...models.player_response_clan_response_full_response_with_metadata_and_container import (
    PlayerResponseClanResponseFullResponseWithMetadataAndContainer,
)
from ...models.player_sort_by import PlayerSortBy
from ...types import UNSET, Response, Unset


def _get_kwargs(
    tag: str,
    *,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, PlayerSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    primary: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["page"] = page

    params["count"] = count

    json_sort_by: Union[Unset, str] = UNSET
    if not isinstance(sort_by, Unset):
        json_sort_by = sort_by.value

    params["sortBy"] = json_sort_by

    json_order: Union[Unset, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["primary"] = primary

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/clan/{tag}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, PlayerResponseClanResponseFullResponseWithMetadataAndContainer]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PlayerResponseClanResponseFullResponseWithMetadataAndContainer.from_dict(response.text)

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
) -> Response[Union[Any, PlayerResponseClanResponseFullResponseWithMetadataAndContainer]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tag: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, PlayerSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    primary: Union[Unset, bool] = False,
) -> Response[Union[Any, PlayerResponseClanResponseFullResponseWithMetadataAndContainer]]:
    """Retrieve details of a specific clan by tag

     Fetches details of a specific clan identified by its tag.

    Args:
        tag (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, PlayerSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        primary (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PlayerResponseClanResponseFullResponseWithMetadataAndContainer]]
    """

    kwargs = _get_kwargs(
        tag=tag,
        page=page,
        count=count,
        sort_by=sort_by,
        order=order,
        primary=primary,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tag: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, PlayerSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    primary: Union[Unset, bool] = False,
) -> Optional[Union[Any, PlayerResponseClanResponseFullResponseWithMetadataAndContainer]]:
    """Retrieve details of a specific clan by tag

     Fetches details of a specific clan identified by its tag.

    Args:
        tag (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, PlayerSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        primary (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PlayerResponseClanResponseFullResponseWithMetadataAndContainer]
    """

    return sync_detailed(
        tag=tag,
        client=client,
        page=page,
        count=count,
        sort_by=sort_by,
        order=order,
        primary=primary,
    ).parsed


async def asyncio_detailed(
    tag: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, PlayerSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    primary: Union[Unset, bool] = False,
) -> Response[Union[Any, PlayerResponseClanResponseFullResponseWithMetadataAndContainer]]:
    """Retrieve details of a specific clan by tag

     Fetches details of a specific clan identified by its tag.

    Args:
        tag (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, PlayerSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        primary (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PlayerResponseClanResponseFullResponseWithMetadataAndContainer]]
    """

    kwargs = _get_kwargs(
        tag=tag,
        page=page,
        count=count,
        sort_by=sort_by,
        order=order,
        primary=primary,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tag: str,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort_by: Union[Unset, PlayerSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    primary: Union[Unset, bool] = False,
) -> Optional[Union[Any, PlayerResponseClanResponseFullResponseWithMetadataAndContainer]]:
    """Retrieve details of a specific clan by tag

     Fetches details of a specific clan identified by its tag.

    Args:
        tag (str):
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort_by (Union[Unset, PlayerSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        primary (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PlayerResponseClanResponseFullResponseWithMetadataAndContainer]
    """

    return (
        await asyncio_detailed(
            tag=tag,
            client=client,
            page=page,
            count=count,
            sort_by=sort_by,
            order=order,
            primary=primary,
        )
    ).parsed
