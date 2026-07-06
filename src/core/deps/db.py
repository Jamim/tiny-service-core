from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_session(request: Request) -> AsyncGenerator[AsyncSession]:
    async_session = async_sessionmaker(
        request.app.state.db,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    async with async_session() as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_session)]
