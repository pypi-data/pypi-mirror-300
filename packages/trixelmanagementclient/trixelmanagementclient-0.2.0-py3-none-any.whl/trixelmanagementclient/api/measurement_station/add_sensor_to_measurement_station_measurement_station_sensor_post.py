from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from typing import Dict
from typing import cast
from ...models.measurement_type_enum import MeasurementTypeEnum
from ...models.sensor_detailed import SensorDetailed
from typing import cast, Union
from typing import Union
from ...types import UNSET, Unset



def _get_kwargs(
    *,
    type: MeasurementTypeEnum,
    accuracy: Union[None, Unset, float] = UNSET,
    sensor_name: Union[None, Unset, str] = UNSET,
    token: str,

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["token"] = token



    

    params: Dict[str, Any] = {}

    json_type = type.value
    params["type"] = json_type

    json_accuracy: Union[None, Unset, float]
    if isinstance(accuracy, Unset):
        json_accuracy = UNSET
    else:
        json_accuracy = accuracy
    params["accuracy"] = json_accuracy

    json_sensor_name: Union[None, Unset, str]
    if isinstance(sensor_name, Unset):
        json_sensor_name = UNSET
    else:
        json_sensor_name = sensor_name
    params["sensor_name"] = json_sensor_name


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/measurement_station/sensor",
        "params": params,
    }


    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, HTTPValidationError, SensorDetailed]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = SensorDetailed.from_dict(response.json())



        return response_201
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


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, HTTPValidationError, SensorDetailed]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    type: MeasurementTypeEnum,
    accuracy: Union[None, Unset, float] = UNSET,
    sensor_name: Union[None, Unset, str] = UNSET,
    token: str,

) -> Response[Union[Any, HTTPValidationError, SensorDetailed]]:
    """ Add a new sensor to an existing measurement station.

     Create a new sensor for a measurement station.

    Args:
        type (MeasurementTypeEnum): Supported measurement types.
        accuracy (Union[None, Unset, float]): Accuracy of the sensor (true observation within +/-
            accuracy).
        sensor_name (Union[None, Unset, str]): Name of the sensor which takes measurements.
        token (str): Measurement station authentication token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, SensorDetailed]]
     """


    kwargs = _get_kwargs(
        type=type,
accuracy=accuracy,
sensor_name=sensor_name,
token=token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    type: MeasurementTypeEnum,
    accuracy: Union[None, Unset, float] = UNSET,
    sensor_name: Union[None, Unset, str] = UNSET,
    token: str,

) -> Optional[Union[Any, HTTPValidationError, SensorDetailed]]:
    """ Add a new sensor to an existing measurement station.

     Create a new sensor for a measurement station.

    Args:
        type (MeasurementTypeEnum): Supported measurement types.
        accuracy (Union[None, Unset, float]): Accuracy of the sensor (true observation within +/-
            accuracy).
        sensor_name (Union[None, Unset, str]): Name of the sensor which takes measurements.
        token (str): Measurement station authentication token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, SensorDetailed]
     """


    return sync_detailed(
        client=client,
type=type,
accuracy=accuracy,
sensor_name=sensor_name,
token=token,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    type: MeasurementTypeEnum,
    accuracy: Union[None, Unset, float] = UNSET,
    sensor_name: Union[None, Unset, str] = UNSET,
    token: str,

) -> Response[Union[Any, HTTPValidationError, SensorDetailed]]:
    """ Add a new sensor to an existing measurement station.

     Create a new sensor for a measurement station.

    Args:
        type (MeasurementTypeEnum): Supported measurement types.
        accuracy (Union[None, Unset, float]): Accuracy of the sensor (true observation within +/-
            accuracy).
        sensor_name (Union[None, Unset, str]): Name of the sensor which takes measurements.
        token (str): Measurement station authentication token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, SensorDetailed]]
     """


    kwargs = _get_kwargs(
        type=type,
accuracy=accuracy,
sensor_name=sensor_name,
token=token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    type: MeasurementTypeEnum,
    accuracy: Union[None, Unset, float] = UNSET,
    sensor_name: Union[None, Unset, str] = UNSET,
    token: str,

) -> Optional[Union[Any, HTTPValidationError, SensorDetailed]]:
    """ Add a new sensor to an existing measurement station.

     Create a new sensor for a measurement station.

    Args:
        type (MeasurementTypeEnum): Supported measurement types.
        accuracy (Union[None, Unset, float]): Accuracy of the sensor (true observation within +/-
            accuracy).
        sensor_name (Union[None, Unset, str]): Name of the sensor which takes measurements.
        token (str): Measurement station authentication token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, SensorDetailed]
     """


    return (await asyncio_detailed(
        client=client,
type=type,
accuracy=accuracy,
sensor_name=sensor_name,
token=token,

    )).parsed
