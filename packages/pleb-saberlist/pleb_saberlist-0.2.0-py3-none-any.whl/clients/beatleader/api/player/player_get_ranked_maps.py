from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ranked_mapper_response import RankedMapperResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: int,
    *,
    sort_by: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["sortBy"] = sort_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/player/{id}/rankedMaps",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, RankedMapperResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RankedMapperResponse.from_dict(response.text)

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
) -> Response[Union[Any, RankedMapperResponse]]:
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
    sort_by: Union[Unset, str] = UNSET,
) -> Response[Union[Any, RankedMapperResponse]]:
    """Get ranked maps this player mapped

     Retrieves a list of maps this player created that later became ranked and give PP now.

    Args:
        id (int):
        sort_by (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, RankedMapperResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
        sort_by=sort_by,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, RankedMapperResponse]]:
    """Get ranked maps this player mapped

     Retrieves a list of maps this player created that later became ranked and give PP now.

    Args:
        id (int):
        sort_by (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, RankedMapperResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        sort_by=sort_by,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
) -> Response[Union[Any, RankedMapperResponse]]:
    """Get ranked maps this player mapped

     Retrieves a list of maps this player created that later became ranked and give PP now.

    Args:
        id (int):
        sort_by (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, RankedMapperResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
        sort_by=sort_by,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    sort_by: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, RankedMapperResponse]]:
    """Get ranked maps this player mapped

     Retrieves a list of maps this player created that later became ranked and give PP now.

    Args:
        id (int):
        sort_by (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, RankedMapperResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            sort_by=sort_by,
        )
    ).parsed
