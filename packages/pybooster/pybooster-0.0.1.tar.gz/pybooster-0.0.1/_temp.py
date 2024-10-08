import asyncio
from collections.abc import AsyncIterator

from pybooster import injector
from pybooster import provider
from pybooster import required
from pybooster import shared
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase): ...


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


@provider.asynciterator
async def sqlalchemy_async_engine(url: str) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(url)
    try:
        yield engine
    finally:
        await engine.dispose()


@provider.asynciterator
async def sqlalchemy_async_session(*, engine: AsyncEngine = required) -> AsyncIterator[AsyncSession]:
    async with (
        AsyncSession(bind=engine, expire_on_commit=False) as session,
        session.begin(),
    ):
        yield session
        print(session)
        await session.commit()


@injector.asyncfunction
async def create_tables(*, engine: AsyncEngine = required) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@injector.asyncfunction
async def add_user(name: str, *, session: AsyncSession = required) -> int:
    print(session)
    user = User(name=name)
    session.add(user)
    await session.flush()
    return user.id


@injector.asyncfunction
async def get_user(user_id: int, *, session: AsyncSession = required) -> User:
    return (await session.execute(select(User).where(User.id == user_id))).scalar_one()


async def main():
    url = "sqlite+aiosqlite:///:memory:"
    with sqlalchemy_async_engine.scope(url), sqlalchemy_async_session.scope():
        async with shared(AsyncEngine):
            await create_tables()
            user_id = await add_user("Alice")
            user = await get_user(user_id)
            assert user.name == "Alice"


asyncio.run(main())
