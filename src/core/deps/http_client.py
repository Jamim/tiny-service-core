from typing import Annotated, cast

from fastapi import Depends, Request
from httpx import AsyncClient


def get_http_client(request: Request) -> AsyncClient:
    return cast(AsyncClient, request.app.state.http_client)


HTTPClient = Annotated[AsyncClient, Depends(get_http_client)]
