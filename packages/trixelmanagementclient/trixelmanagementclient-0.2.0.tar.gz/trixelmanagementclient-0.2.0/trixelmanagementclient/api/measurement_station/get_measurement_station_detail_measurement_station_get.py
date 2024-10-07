from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from typing import Dict
from ...models.measurement_station import MeasurementStation
from typing import cast



def _get_kwargs(
    *,
    token: str,

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["token"] = token



    

    

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/measurement_station",
    }


    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, HTTPValidationError, MeasurementStation]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = MeasurementStation.from_dict(response.json())



        return response_200
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        response_503 = cast(Any, None)
        return response_503
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, HTTPValidationError, MeasurementStation]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    token: str,

) -> Response[Union[Any, HTTPValidationError, MeasurementStation]]:
    """ Get details about own measurement station.

     Delete an existing measurement station from the DB.

    Args:
        token (str): Measurement station authentication token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, MeasurementStation]]
     """


    kwargs = _get_kwargs(
        token=token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    token: str,

) -> Optional[Union[Any, HTTPValidationError, MeasurementStation]]:
    """ Get details about own measurement station.

     Delete an existing measurement station from the DB.

    Args:
        token (str): Measurement station authentication token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MeasurementStation]
     """


    return sync_detailed(
        client=client,
token=token,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    token: str,

) -> Response[Union[Any, HTTPValidationError, MeasurementStation]]:
    """ Get details about own measurement station.

     Delete an existing measurement station from the DB.

    Args:
        token (str): Measurement station authentication token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, MeasurementStation]]
     """


    kwargs = _get_kwargs(
        token=token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    token: str,

) -> Optional[Union[Any, HTTPValidationError, MeasurementStation]]:
    """ Get details about own measurement station.

     Delete an existing measurement station from the DB.

    Args:
        token (str): Measurement station authentication token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MeasurementStation]
     """


    return (await asyncio_detailed(
        client=client,
token=token,

    )).parsed
