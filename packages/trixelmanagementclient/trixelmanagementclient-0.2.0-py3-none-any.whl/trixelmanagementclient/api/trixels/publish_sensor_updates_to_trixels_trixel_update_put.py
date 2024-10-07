from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from typing import Dict
from typing import cast
from ...models.publish_sensor_updates_to_trixels_trixel_update_put_updates import PublishSensorUpdatesToTrixelsTrixelUpdatePutUpdates



def _get_kwargs(
    *,
    body: PublishSensorUpdatesToTrixelsTrixelUpdatePutUpdates,
    token: str,

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["token"] = token



    

    

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": "/trixel/update",
    }

    _body = body.to_dict()


    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

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
    *,
    client: Union[AuthenticatedClient, Client],
    body: PublishSensorUpdatesToTrixelsTrixelUpdatePutUpdates,
    token: str,

) -> Response[Union[Any, HTTPValidationError]]:
    """ Publish multiple sensor updates to the TMS.

     Publish multiple sensor updates to the TMS which are stored and processed within the desired
    trixels.

    Args:
        token (str): Measurement station authentication token.
        body (PublishSensorUpdatesToTrixelsTrixelUpdatePutUpdates): A dictionary where for each
            trixel, sensors with their updated measurements are described.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        body=body,
token=token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PublishSensorUpdatesToTrixelsTrixelUpdatePutUpdates,
    token: str,

) -> Optional[Union[Any, HTTPValidationError]]:
    """ Publish multiple sensor updates to the TMS.

     Publish multiple sensor updates to the TMS which are stored and processed within the desired
    trixels.

    Args:
        token (str): Measurement station authentication token.
        body (PublishSensorUpdatesToTrixelsTrixelUpdatePutUpdates): A dictionary where for each
            trixel, sensors with their updated measurements are described.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
     """


    return sync_detailed(
        client=client,
body=body,
token=token,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PublishSensorUpdatesToTrixelsTrixelUpdatePutUpdates,
    token: str,

) -> Response[Union[Any, HTTPValidationError]]:
    """ Publish multiple sensor updates to the TMS.

     Publish multiple sensor updates to the TMS which are stored and processed within the desired
    trixels.

    Args:
        token (str): Measurement station authentication token.
        body (PublishSensorUpdatesToTrixelsTrixelUpdatePutUpdates): A dictionary where for each
            trixel, sensors with their updated measurements are described.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        body=body,
token=token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PublishSensorUpdatesToTrixelsTrixelUpdatePutUpdates,
    token: str,

) -> Optional[Union[Any, HTTPValidationError]]:
    """ Publish multiple sensor updates to the TMS.

     Publish multiple sensor updates to the TMS which are stored and processed within the desired
    trixels.

    Args:
        token (str): Measurement station authentication token.
        body (PublishSensorUpdatesToTrixelsTrixelUpdatePutUpdates): A dictionary where for each
            trixel, sensors with their updated measurements are described.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
     """


    return (await asyncio_detailed(
        client=client,
body=body,
token=token,

    )).parsed
