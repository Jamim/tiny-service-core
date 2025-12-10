import hmac
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import core
from ..crypto import get_key_hash


def get_app_client_key(
    credentials: Annotated[
        HTTPAuthorizationCredentials, Depends(HTTPBearer())
    ],
) -> str:
    return credentials.credentials


AppClientKey = Annotated[str, Depends(get_app_client_key)]


def verify_app_client_key(app_key: AppClientKey) -> None:
    key_hash = get_key_hash(app_key)
    for allowed_key_hash in core.settings.app_client_key_hashes:
        if hmac.compare_digest(key_hash, allowed_key_hash):
            return

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'App key is not valid')


VerifyClient = Depends(verify_app_client_key)
