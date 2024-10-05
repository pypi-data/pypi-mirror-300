from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.clan_response_full_response_with_metadata import ClanResponseFullResponseWithMetadata
from ...models.clan_sort_by import ClanSortBy
from ...models.order import Order
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort: Union[Unset, ClanSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    search: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, ClanSortBy] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["page"] = page

    params["count"] = count

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    json_order: Union[Unset, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["search"] = search

    json_sort_by: Union[Unset, str] = UNSET
    if not isinstance(sort_by, Unset):
        json_sort_by = sort_by.value

    params["sortBy"] = json_sort_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/clans",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ClanResponseFullResponseWithMetadata]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ClanResponseFullResponseWithMetadata.from_dict(response.text)

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
) -> Response[Union[Any, ClanResponseFullResponseWithMetadata]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort: Union[Unset, ClanSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    search: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, ClanSortBy] = UNSET,
) -> Response[Union[Any, ClanResponseFullResponseWithMetadata]]:
    """Retrieve a list of clans

     Fetches a paginated and optionally filtered list of clans (group of players). Filters include
    sorting by performance points, search, name, rank, and more.

    Args:
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort (Union[Unset, ClanSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        search (Union[Unset, str]):
        sort_by (Union[Unset, ClanSortBy]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ClanResponseFullResponseWithMetadata]]
    """

    kwargs = _get_kwargs(
        page=page,
        count=count,
        sort=sort,
        order=order,
        search=search,
        sort_by=sort_by,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort: Union[Unset, ClanSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    search: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, ClanSortBy] = UNSET,
) -> Optional[Union[Any, ClanResponseFullResponseWithMetadata]]:
    """Retrieve a list of clans

     Fetches a paginated and optionally filtered list of clans (group of players). Filters include
    sorting by performance points, search, name, rank, and more.

    Args:
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort (Union[Unset, ClanSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        search (Union[Unset, str]):
        sort_by (Union[Unset, ClanSortBy]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ClanResponseFullResponseWithMetadata]
    """

    return sync_detailed(
        client=client,
        page=page,
        count=count,
        sort=sort,
        order=order,
        search=search,
        sort_by=sort_by,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort: Union[Unset, ClanSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    search: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, ClanSortBy] = UNSET,
) -> Response[Union[Any, ClanResponseFullResponseWithMetadata]]:
    """Retrieve a list of clans

     Fetches a paginated and optionally filtered list of clans (group of players). Filters include
    sorting by performance points, search, name, rank, and more.

    Args:
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort (Union[Unset, ClanSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        search (Union[Unset, str]):
        sort_by (Union[Unset, ClanSortBy]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ClanResponseFullResponseWithMetadata]]
    """

    kwargs = _get_kwargs(
        page=page,
        count=count,
        sort=sort,
        order=order,
        search=search,
        sort_by=sort_by,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    count: Union[Unset, int] = 10,
    sort: Union[Unset, ClanSortBy] = UNSET,
    order: Union[Unset, Order] = UNSET,
    search: Union[Unset, str] = UNSET,
    sort_by: Union[Unset, ClanSortBy] = UNSET,
) -> Optional[Union[Any, ClanResponseFullResponseWithMetadata]]:
    """Retrieve a list of clans

     Fetches a paginated and optionally filtered list of clans (group of players). Filters include
    sorting by performance points, search, name, rank, and more.

    Args:
        page (Union[Unset, int]):  Default: 1.
        count (Union[Unset, int]):  Default: 10.
        sort (Union[Unset, ClanSortBy]):
        order (Union[Unset, Order]): Represents the order in which values will be sorted.
        search (Union[Unset, str]):
        sort_by (Union[Unset, ClanSortBy]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ClanResponseFullResponseWithMetadata]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            count=count,
            sort=sort,
            order=order,
            search=search,
            sort_by=sort_by,
        )
    ).parsed
