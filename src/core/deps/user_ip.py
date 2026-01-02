from typing import Annotated

from fastapi import Depends, Header

XForwardedFor = Header(alias='X-Forwarded-For', include_in_schema=False)


def user_ip(forwarded_for: Annotated[str, XForwardedFor]) -> str:
    return forwarded_for.split(',', maxsplit=1)[0]


UserIP = Annotated[str, Depends(user_ip)]
