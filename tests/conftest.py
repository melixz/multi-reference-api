import asyncio
import os

import pytest
import pytest_asyncio
from geoalchemy2.elements import WKTElement
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.database import get_db
from app.main import app
from app.models import Activity, Building, Organization, OrganizationPhone
from app.models.base import Base

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", settings.database_url)


def make_point(lon: float, lat: float) -> WKTElement:
    return WKTElement(f"POINT({lon} {lat})", srid=4326)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    engine = create_async_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with session_maker() as session:
        yield session
        await session.rollback()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture()
async def client(db_session: AsyncSession):
    async def _get_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture()
def api_headers() -> dict[str, str]:
    return {settings.api_key_header: settings.api_key}


@pytest_asyncio.fixture()
async def seed_data(db_session: AsyncSession):
    moscow = Building(
        address="г. Москва, ул. Ленина 1, офис 3",
        latitude=55.7558,
        longitude=37.6173,
        location=make_point(37.6173, 55.7558),
    )
    yekb = Building(
        address="г. Екатеринбург, ул. Блюхера, 32/1",
        latitude=56.8389,
        longitude=60.6057,
        location=make_point(60.6057, 56.8389),
    )

    food = Activity(name="Еда")
    meat = Activity(name="Мясная продукция", parent=food)
    milk = Activity(name="Молочная продукция", parent=food)

    org_food = Organization(
        name="Еда Плюс",
        building=moscow,
        activities=[food],
        phones=[OrganizationPhone(phone="8-495-000-11-22")],
    )
    org_meat = Organization(
        name='ООО "Рога и Копыта"',
        building=yekb,
        activities=[meat],
        phones=[OrganizationPhone(phone="2-222-222")],
    )
    org_milk = Organization(
        name="ИП Молочный Дом",
        building=moscow,
        activities=[milk],
        phones=[OrganizationPhone(phone="8-495-123-45-67")],
    )

    db_session.add_all([moscow, yekb, food, meat, milk, org_food, org_meat, org_milk])
    await db_session.commit()

    return {
        "buildings": {"moscow": moscow, "yekb": yekb},
        "activities": {"food": food, "meat": meat, "milk": milk},
        "organizations": {"food": org_food, "meat": org_meat, "milk": org_milk},
    }
