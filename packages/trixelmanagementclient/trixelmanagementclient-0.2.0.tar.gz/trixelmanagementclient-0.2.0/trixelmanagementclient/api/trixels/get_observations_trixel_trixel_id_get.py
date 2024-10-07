from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from typing import Dict
from typing import cast
from ...models.observation import Observation
from typing import cast, List
from ...models.measurement_type_enum import MeasurementTypeEnum
from typing import cast, Union
from typing import Union
from ...types import UNSET, Unset



def _get_kwargs(
    trixel_id: int,
    *,
    types: Union[Unset, List[MeasurementTypeEnum]] = UNSET,
    age: Union[None, Unset, int] = UNSET,

) -> Dict[str, Any]:
    

    

    params: Dict[str, Any] = {}

    json_types: Union[Unset, List[str]] = UNSET
    if not isinstance(types, Unset):
        json_types = []
        for types_item_data in types:
            types_item = types_item_data.value
            json_types.append(types_item)


    params["types"] = json_types

    json_age: Union[None, Unset, int]
    if isinstance(age, Unset):
        json_age = UNSET
    else:
        json_age = age
    params["age"] = json_age


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/trixel/{trixel_id}".format(trixel_id=trixel_id,),
        "params": params,
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, HTTPValidationError, List['Observation']]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = Observation.from_dict(response_200_item_data)



            response_200.append(response_200_item)

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


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, HTTPValidationError, List['Observation']]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    trixel_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    types: Union[Unset, List[MeasurementTypeEnum]] = UNSET,
    age: Union[None, Unset, int] = UNSET,

) -> Response[Union[Any, HTTPValidationError, List['Observation']]]:
    """ Gets the current environmental observations for a trixel.

     Retrieve the latest measurement for the provided types for a trixel from the DB.

    Args:
        trixel_id (int): The trixel for which observations are retrieved.
        types (Union[Unset, List[MeasurementTypeEnum]]): List of measurement types which restrict
            results. If none are provided, all types are used.
        age (Union[None, Unset, int]): Maximum age of measurement timestamps in seconds.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, List['Observation']]]
     """


    kwargs = _get_kwargs(
        trixel_id=trixel_id,
types=types,
age=age,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    trixel_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    types: Union[Unset, List[MeasurementTypeEnum]] = UNSET,
    age: Union[None, Unset, int] = UNSET,

) -> Optional[Union[Any, HTTPValidationError, List['Observation']]]:
    """ Gets the current environmental observations for a trixel.

     Retrieve the latest measurement for the provided types for a trixel from the DB.

    Args:
        trixel_id (int): The trixel for which observations are retrieved.
        types (Union[Unset, List[MeasurementTypeEnum]]): List of measurement types which restrict
            results. If none are provided, all types are used.
        age (Union[None, Unset, int]): Maximum age of measurement timestamps in seconds.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, List['Observation']]
     """


    return sync_detailed(
        trixel_id=trixel_id,
client=client,
types=types,
age=age,

    ).parsed

async def asyncio_detailed(
    trixel_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    types: Union[Unset, List[MeasurementTypeEnum]] = UNSET,
    age: Union[None, Unset, int] = UNSET,

) -> Response[Union[Any, HTTPValidationError, List['Observation']]]:
    """ Gets the current environmental observations for a trixel.

     Retrieve the latest measurement for the provided types for a trixel from the DB.

    Args:
        trixel_id (int): The trixel for which observations are retrieved.
        types (Union[Unset, List[MeasurementTypeEnum]]): List of measurement types which restrict
            results. If none are provided, all types are used.
        age (Union[None, Unset, int]): Maximum age of measurement timestamps in seconds.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, List['Observation']]]
     """


    kwargs = _get_kwargs(
        trixel_id=trixel_id,
types=types,
age=age,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    trixel_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    types: Union[Unset, List[MeasurementTypeEnum]] = UNSET,
    age: Union[None, Unset, int] = UNSET,

) -> Optional[Union[Any, HTTPValidationError, List['Observation']]]:
    """ Gets the current environmental observations for a trixel.

     Retrieve the latest measurement for the provided types for a trixel from the DB.

    Args:
        trixel_id (int): The trixel for which observations are retrieved.
        types (Union[Unset, List[MeasurementTypeEnum]]): List of measurement types which restrict
            results. If none are provided, all types are used.
        age (Union[None, Unset, int]): Maximum age of measurement timestamps in seconds.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, List['Observation']]
     """


    return (await asyncio_detailed(
        trixel_id=trixel_id,
client=client,
types=types,
age=age,

    )).parsed
