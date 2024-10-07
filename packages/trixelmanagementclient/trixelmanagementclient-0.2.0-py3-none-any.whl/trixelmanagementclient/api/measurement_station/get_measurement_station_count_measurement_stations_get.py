from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from typing import Dict
from typing import cast
from typing import cast, Union
from typing import Union
from ...types import UNSET, Unset



def _get_kwargs(
    *,
    active: Union[None, Unset, bool] = UNSET,

) -> Dict[str, Any]:
    

    

    params: Dict[str, Any] = {}

    json_active: Union[None, Unset, bool]
    if isinstance(active, Unset):
        json_active = UNSET
    else:
        json_active = active
    params["active"] = json_active


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/measurement_stations",
        "params": params,
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = response.json()
        return response_200
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        response_503 = cast(Any, None)
        return response_503
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    active: Union[None, Unset, bool] = UNSET,

) -> Response[Union[Any, HTTPValidationError]]:
    """ Get the number of measurement station registered at this TMS.

     Get the current number of registered measurement stations.

    Args:
        active (Union[None, Unset, bool]): Filters by active state. Use both states if None.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        active=active,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    active: Union[None, Unset, bool] = UNSET,

) -> Optional[Union[Any, HTTPValidationError]]:
    """ Get the number of measurement station registered at this TMS.

     Get the current number of registered measurement stations.

    Args:
        active (Union[None, Unset, bool]): Filters by active state. Use both states if None.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
     """


    return sync_detailed(
        client=client,
active=active,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    active: Union[None, Unset, bool] = UNSET,

) -> Response[Union[Any, HTTPValidationError]]:
    """ Get the number of measurement station registered at this TMS.

     Get the current number of registered measurement stations.

    Args:
        active (Union[None, Unset, bool]): Filters by active state. Use both states if None.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        active=active,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    active: Union[None, Unset, bool] = UNSET,

) -> Optional[Union[Any, HTTPValidationError]]:
    """ Get the number of measurement station registered at this TMS.

     Get the current number of registered measurement stations.

    Args:
        active (Union[None, Unset, bool]): Filters by active state. Use both states if None.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
     """


    return (await asyncio_detailed(
        client=client,
active=active,

    )).parsed
