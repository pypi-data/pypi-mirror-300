from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from typing import Dict
from typing import cast
from ...models.measurement_station_create import MeasurementStationCreate
from typing import Union
from ...types import UNSET, Unset



def _get_kwargs(
    *,
    k_requirement: Union[Unset, int] = 3,

) -> Dict[str, Any]:
    

    

    params: Dict[str, Any] = {}

    params["k_requirement"] = k_requirement


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/measurement_station",
        "params": params,
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, HTTPValidationError, MeasurementStationCreate]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = MeasurementStationCreate.from_dict(response.json())



        return response_201
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


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, HTTPValidationError, MeasurementStationCreate]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    k_requirement: Union[Unset, int] = 3,

) -> Response[Union[Any, HTTPValidationError, MeasurementStationCreate]]:
    """ Register a new measurement station.

     Register a new measurement station at this TMS.

    The measurement station token can be used to register and update sensors.
    Store the token properly, it is only transferred once!

    Args:
        k_requirement (Union[Unset, int]): The k-anonymity requirement, which is enforced for this
            measurement station and it's sensors. Default: 3.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, MeasurementStationCreate]]
     """


    kwargs = _get_kwargs(
        k_requirement=k_requirement,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    k_requirement: Union[Unset, int] = 3,

) -> Optional[Union[Any, HTTPValidationError, MeasurementStationCreate]]:
    """ Register a new measurement station.

     Register a new measurement station at this TMS.

    The measurement station token can be used to register and update sensors.
    Store the token properly, it is only transferred once!

    Args:
        k_requirement (Union[Unset, int]): The k-anonymity requirement, which is enforced for this
            measurement station and it's sensors. Default: 3.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MeasurementStationCreate]
     """


    return sync_detailed(
        client=client,
k_requirement=k_requirement,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    k_requirement: Union[Unset, int] = 3,

) -> Response[Union[Any, HTTPValidationError, MeasurementStationCreate]]:
    """ Register a new measurement station.

     Register a new measurement station at this TMS.

    The measurement station token can be used to register and update sensors.
    Store the token properly, it is only transferred once!

    Args:
        k_requirement (Union[Unset, int]): The k-anonymity requirement, which is enforced for this
            measurement station and it's sensors. Default: 3.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, MeasurementStationCreate]]
     """


    kwargs = _get_kwargs(
        k_requirement=k_requirement,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    k_requirement: Union[Unset, int] = 3,

) -> Optional[Union[Any, HTTPValidationError, MeasurementStationCreate]]:
    """ Register a new measurement station.

     Register a new measurement station at this TMS.

    The measurement station token can be used to register and update sensors.
    Store the token properly, it is only transferred once!

    Args:
        k_requirement (Union[Unset, int]): The k-anonymity requirement, which is enforced for this
            measurement station and it's sensors. Default: 3.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, MeasurementStationCreate]
     """


    return (await asyncio_detailed(
        client=client,
k_requirement=k_requirement,

    )).parsed
