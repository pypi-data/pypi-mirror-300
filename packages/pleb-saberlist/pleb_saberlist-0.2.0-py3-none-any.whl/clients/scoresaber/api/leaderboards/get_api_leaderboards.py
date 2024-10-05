from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.leaderboard_info_collection import LeaderboardInfoCollection
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    search: Union[Unset, str] = UNSET,
    verified: Union[Unset, bool] = UNSET,
    ranked: Union[Unset, bool] = UNSET,
    qualified: Union[Unset, bool] = UNSET,
    loved: Union[Unset, bool] = UNSET,
    min_star: Union[Unset, float] = UNSET,
    max_star: Union[Unset, float] = UNSET,
    category: Union[Unset, float] = UNSET,
    sort: Union[Unset, float] = UNSET,
    unique: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["search"] = search

    params["verified"] = verified

    params["ranked"] = ranked

    params["qualified"] = qualified

    params["loved"] = loved

    params["minStar"] = min_star

    params["maxStar"] = max_star

    params["category"] = category

    params["sort"] = sort

    params["unique"] = unique

    params["page"] = page

    params["withMetadata"] = with_metadata

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/leaderboards",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, LeaderboardInfoCollection]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LeaderboardInfoCollection.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = cast(Any, None)
        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, LeaderboardInfoCollection]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, str] = UNSET,
    verified: Union[Unset, bool] = UNSET,
    ranked: Union[Unset, bool] = UNSET,
    qualified: Union[Unset, bool] = UNSET,
    loved: Union[Unset, bool] = UNSET,
    min_star: Union[Unset, float] = UNSET,
    max_star: Union[Unset, float] = UNSET,
    category: Union[Unset, float] = UNSET,
    sort: Union[Unset, float] = UNSET,
    unique: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, LeaderboardInfoCollection]]:
    """Get a list of leaderboards based on filters

    Args:
        search (Union[Unset, str]):
        verified (Union[Unset, bool]):
        ranked (Union[Unset, bool]):
        qualified (Union[Unset, bool]):
        loved (Union[Unset, bool]):
        min_star (Union[Unset, float]):
        max_star (Union[Unset, float]):
        category (Union[Unset, float]):
        sort (Union[Unset, float]):
        unique (Union[Unset, bool]):
        page (Union[Unset, int]):
        with_metadata (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LeaderboardInfoCollection]]
    """

    kwargs = _get_kwargs(
        search=search,
        verified=verified,
        ranked=ranked,
        qualified=qualified,
        loved=loved,
        min_star=min_star,
        max_star=max_star,
        category=category,
        sort=sort,
        unique=unique,
        page=page,
        with_metadata=with_metadata,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, str] = UNSET,
    verified: Union[Unset, bool] = UNSET,
    ranked: Union[Unset, bool] = UNSET,
    qualified: Union[Unset, bool] = UNSET,
    loved: Union[Unset, bool] = UNSET,
    min_star: Union[Unset, float] = UNSET,
    max_star: Union[Unset, float] = UNSET,
    category: Union[Unset, float] = UNSET,
    sort: Union[Unset, float] = UNSET,
    unique: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, LeaderboardInfoCollection]]:
    """Get a list of leaderboards based on filters

    Args:
        search (Union[Unset, str]):
        verified (Union[Unset, bool]):
        ranked (Union[Unset, bool]):
        qualified (Union[Unset, bool]):
        loved (Union[Unset, bool]):
        min_star (Union[Unset, float]):
        max_star (Union[Unset, float]):
        category (Union[Unset, float]):
        sort (Union[Unset, float]):
        unique (Union[Unset, bool]):
        page (Union[Unset, int]):
        with_metadata (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LeaderboardInfoCollection]
    """

    return sync_detailed(
        client=client,
        search=search,
        verified=verified,
        ranked=ranked,
        qualified=qualified,
        loved=loved,
        min_star=min_star,
        max_star=max_star,
        category=category,
        sort=sort,
        unique=unique,
        page=page,
        with_metadata=with_metadata,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, str] = UNSET,
    verified: Union[Unset, bool] = UNSET,
    ranked: Union[Unset, bool] = UNSET,
    qualified: Union[Unset, bool] = UNSET,
    loved: Union[Unset, bool] = UNSET,
    min_star: Union[Unset, float] = UNSET,
    max_star: Union[Unset, float] = UNSET,
    category: Union[Unset, float] = UNSET,
    sort: Union[Unset, float] = UNSET,
    unique: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, LeaderboardInfoCollection]]:
    """Get a list of leaderboards based on filters

    Args:
        search (Union[Unset, str]):
        verified (Union[Unset, bool]):
        ranked (Union[Unset, bool]):
        qualified (Union[Unset, bool]):
        loved (Union[Unset, bool]):
        min_star (Union[Unset, float]):
        max_star (Union[Unset, float]):
        category (Union[Unset, float]):
        sort (Union[Unset, float]):
        unique (Union[Unset, bool]):
        page (Union[Unset, int]):
        with_metadata (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LeaderboardInfoCollection]]
    """

    kwargs = _get_kwargs(
        search=search,
        verified=verified,
        ranked=ranked,
        qualified=qualified,
        loved=loved,
        min_star=min_star,
        max_star=max_star,
        category=category,
        sort=sort,
        unique=unique,
        page=page,
        with_metadata=with_metadata,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, str] = UNSET,
    verified: Union[Unset, bool] = UNSET,
    ranked: Union[Unset, bool] = UNSET,
    qualified: Union[Unset, bool] = UNSET,
    loved: Union[Unset, bool] = UNSET,
    min_star: Union[Unset, float] = UNSET,
    max_star: Union[Unset, float] = UNSET,
    category: Union[Unset, float] = UNSET,
    sort: Union[Unset, float] = UNSET,
    unique: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    with_metadata: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, LeaderboardInfoCollection]]:
    """Get a list of leaderboards based on filters

    Args:
        search (Union[Unset, str]):
        verified (Union[Unset, bool]):
        ranked (Union[Unset, bool]):
        qualified (Union[Unset, bool]):
        loved (Union[Unset, bool]):
        min_star (Union[Unset, float]):
        max_star (Union[Unset, float]):
        category (Union[Unset, float]):
        sort (Union[Unset, float]):
        unique (Union[Unset, bool]):
        page (Union[Unset, int]):
        with_metadata (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LeaderboardInfoCollection]
    """

    return (
        await asyncio_detailed(
            client=client,
            search=search,
            verified=verified,
            ranked=ranked,
            qualified=qualified,
            loved=loved,
            min_star=min_star,
            max_star=max_star,
            category=category,
            sort=sort,
            unique=unique,
            page=page,
            with_metadata=with_metadata,
        )
    ).parsed
