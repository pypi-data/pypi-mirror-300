from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    search: Union[Unset, str] = UNSET,
    countries: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["search"] = search

    params["countries"] = countries

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/players/count",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, float]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(float, response.text)
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
) -> Response[Union[Any, float]]:
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
    countries: Union[Unset, str] = UNSET,
) -> Response[Union[Any, float]]:
    """Get a list of active players based on filters

    Args:
        search (Union[Unset, str]):
        countries (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, float]]
    """

    kwargs = _get_kwargs(
        search=search,
        countries=countries,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, str] = UNSET,
    countries: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, float]]:
    """Get a list of active players based on filters

    Args:
        search (Union[Unset, str]):
        countries (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, float]
    """

    return sync_detailed(
        client=client,
        search=search,
        countries=countries,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, str] = UNSET,
    countries: Union[Unset, str] = UNSET,
) -> Response[Union[Any, float]]:
    """Get a list of active players based on filters

    Args:
        search (Union[Unset, str]):
        countries (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, float]]
    """

    kwargs = _get_kwargs(
        search=search,
        countries=countries,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, str] = UNSET,
    countries: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, float]]:
    """Get a list of active players based on filters

    Args:
        search (Union[Unset, str]):
        countries (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, float]
    """

    return (
        await asyncio_detailed(
            client=client,
            search=search,
            countries=countries,
        )
    ).parsed
