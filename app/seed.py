import asyncio

from geoalchemy2.elements import WKTElement
from sqlalchemy import delete

from app.core.database import async_session_maker
from app.models import Activity, Building, Organization, OrganizationActivity, OrganizationPhone


def make_point(lon: float, lat: float) -> WKTElement:
    return WKTElement(f"POINT({lon} {lat})", srid=4326)


async def seed_data() -> None:
    async with async_session_maker() as session:
        async with session.begin():
            await session.execute(delete(OrganizationActivity))
            await session.execute(delete(OrganizationPhone))
            await session.execute(delete(Organization))
            await session.execute(delete(Activity))
            await session.execute(delete(Building))

        async with session.begin():
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

            auto = Activity(name="Автомобили")
            cargo = Activity(name="Грузовые", parent=auto)
            passenger = Activity(name="Легковые", parent=auto)
            parts = Activity(name="Запчасти", parent=passenger)
            accessories = Activity(name="Аксессуары", parent=passenger)

            org1 = Organization(
                name='ООО "Рога и Копыта"',
                building=yekb,
                activities=[meat, milk],
                phones=[
                    OrganizationPhone(phone="2-222-222"),
                    OrganizationPhone(phone="3-333-333"),
                    OrganizationPhone(phone="8-923-666-13-13"),
                ],
            )
            org2 = Organization(
                name="ООО АвтоМир",
                building=moscow,
                activities=[cargo],
                phones=[OrganizationPhone(phone="8-800-555-35-35")],
            )
            org3 = Organization(
                name="ИП Молочный Дом",
                building=moscow,
                activities=[milk],
                phones=[OrganizationPhone(phone="8-495-123-45-67")],
            )
            org4 = Organization(
                name="Запчасти Плюс",
                building=yekb,
                activities=[parts, accessories],
                phones=[OrganizationPhone(phone="8-343-111-22-33")],
            )

            session.add_all(
                [
                    moscow,
                    yekb,
                    food,
                    auto,
                    org1,
                    org2,
                    org3,
                    org4,
                ],
            )


def main() -> None:
    asyncio.run(seed_data())


if __name__ == "__main__":
    main()
