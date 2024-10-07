from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from typing import Dict
from typing import cast
import datetime
from typing import cast, Union
from dateutil.parser import isoparse



def _get_kwargs(
    trixel_id: int,
    sensor_id: int,
    *,
    value: float,
    timestamp: Union[datetime.datetime, int],
    token: str,

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["token"] = token



    

    params: Dict[str, Any] = {}

    params["value"] = value

    json_timestamp: Union[int, str]
    if isinstance(timestamp, datetime.datetime):
        json_timestamp = timestamp.isoformat()
    else:
        json_timestamp = timestamp
    params["timestamp"] = json_timestamp


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": "/trixel/{trixel_id}/update/{sensor_id}".format(trixel_id=trixel_id,sensor_id=sensor_id,),
        "params": params,
    }


    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = response.json()
        return response_200
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        response_503 = cast(Any, None)
        return response_503
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.SEE_OTHER:
        response_303 = cast(Any, None)
        return response_303
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
    trixel_id: int,
    sensor_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    value: float,
    timestamp: Union[datetime.datetime, int],
    token: str,

) -> Response[Union[Any, HTTPValidationError]]:
    """ Publish a single sensor value update to the TMS.

     Publish a single sensor value update to the TMS which is stored and processed within the desired
    trixel.

    Args:
        trixel_id (int): The Trixel to which the sensor contributes.
        sensor_id (int): The ID of the sensor which took the measurement.
        value (float): The updated measurement value.
        timestamp (Union[datetime.datetime, int]): Point in time at which the measurement was
            taken (unix time).
        token (str): Measurement station authentication token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        trixel_id=trixel_id,
sensor_id=sensor_id,
value=value,
timestamp=timestamp,
token=token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    trixel_id: int,
    sensor_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    value: float,
    timestamp: Union[datetime.datetime, int],
    token: str,

) -> Optional[Union[Any, HTTPValidationError]]:
    """ Publish a single sensor value update to the TMS.

     Publish a single sensor value update to the TMS which is stored and processed within the desired
    trixel.

    Args:
        trixel_id (int): The Trixel to which the sensor contributes.
        sensor_id (int): The ID of the sensor which took the measurement.
        value (float): The updated measurement value.
        timestamp (Union[datetime.datetime, int]): Point in time at which the measurement was
            taken (unix time).
        token (str): Measurement station authentication token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
     """


    return sync_detailed(
        trixel_id=trixel_id,
sensor_id=sensor_id,
client=client,
value=value,
timestamp=timestamp,
token=token,

    ).parsed

async def asyncio_detailed(
    trixel_id: int,
    sensor_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    value: float,
    timestamp: Union[datetime.datetime, int],
    token: str,

) -> Response[Union[Any, HTTPValidationError]]:
    """ Publish a single sensor value update to the TMS.

     Publish a single sensor value update to the TMS which is stored and processed within the desired
    trixel.

    Args:
        trixel_id (int): The Trixel to which the sensor contributes.
        sensor_id (int): The ID of the sensor which took the measurement.
        value (float): The updated measurement value.
        timestamp (Union[datetime.datetime, int]): Point in time at which the measurement was
            taken (unix time).
        token (str): Measurement station authentication token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        trixel_id=trixel_id,
sensor_id=sensor_id,
value=value,
timestamp=timestamp,
token=token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    trixel_id: int,
    sensor_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    value: float,
    timestamp: Union[datetime.datetime, int],
    token: str,

) -> Optional[Union[Any, HTTPValidationError]]:
    """ Publish a single sensor value update to the TMS.

     Publish a single sensor value update to the TMS which is stored and processed within the desired
    trixel.

    Args:
        trixel_id (int): The Trixel to which the sensor contributes.
        sensor_id (int): The ID of the sensor which took the measurement.
        value (float): The updated measurement value.
        timestamp (Union[datetime.datetime, int]): Point in time at which the measurement was
            taken (unix time).
        token (str): Measurement station authentication token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
     """


    return (await asyncio_detailed(
        trixel_id=trixel_id,
sensor_id=sensor_id,
client=client,
value=value,
timestamp=timestamp,
token=token,

    )).parsed
