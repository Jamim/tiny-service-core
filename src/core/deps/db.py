from collections.abc import AsyncGenerator
from typing import Annotated, cast

from fastapi import Depends, Request
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_session(request: Request) -> AsyncGenerator[AsyncSession]:
    async_session = sessionmaker(
        request.app.state.db,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    session = cast(AsyncSession, async_session())
    async with session:
        yield session


Session = Annotated[AsyncSession, Depends(get_session)]
