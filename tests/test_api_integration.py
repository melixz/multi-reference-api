import pytest


@pytest.mark.integration
async def test_requires_api_key(client):
    response = await client.get("/api/v1/buildings/")
    assert response.status_code == 401


@pytest.mark.integration
async def test_list_buildings(client, api_headers, seed_data):
    response = await client.get("/api/v1/buildings/", headers=api_headers)

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert len(payload["data"]) == 2


@pytest.mark.integration
async def test_get_organization(client, api_headers, seed_data):
    org = seed_data["organizations"]["meat"]
    response = await client.get(f"/api/v1/organizations/{org.id}", headers=api_headers)

    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["id"] == org.id
    assert payload["data"]["name"] == org.name


@pytest.mark.integration
async def test_list_by_building(client, api_headers, seed_data):
    building = seed_data["buildings"]["moscow"]
    response = await client.get(
        f"/api/v1/organizations/by-building/{building.id}",
        headers=api_headers,
    )

    assert response.status_code == 200
    payload = response.json()
    names = {item["name"] for item in payload["data"]}
    assert names == {"Еда Плюс", "ИП Молочный Дом"}


@pytest.mark.integration
async def test_list_by_activity_with_descendants(client, api_headers, seed_data):
    activity = seed_data["activities"]["food"]
    response = await client.get(
        f"/api/v1/organizations/by-activity/{activity.id}?include_descendants=true",
        headers=api_headers,
    )

    assert response.status_code == 200
    payload = response.json()
    names = {item["name"] for item in payload["data"]}
    assert names == {"Еда Плюс", 'ООО "Рога и Копыта"', "ИП Молочный Дом"}


@pytest.mark.integration
async def test_search_by_name(client, api_headers, seed_data):
    response = await client.get(
        "/api/v1/organizations/search?name=Молочный",
        headers=api_headers,
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["data"]) == 1
    assert payload["data"][0]["name"] == "ИП Молочный Дом"


@pytest.mark.integration
async def test_geo_radius(client, api_headers, seed_data):
    response = await client.get(
        "/api/v1/organizations/geo?lat=55.7558&lon=37.6173&radius_m=1500",
        headers=api_headers,
    )

    assert response.status_code == 200
    payload = response.json()
    names = {item["name"] for item in payload["data"]}
    assert names == {"Еда Плюс", "ИП Молочный Дом"}


@pytest.mark.integration
async def test_geo_bbox(client, api_headers, seed_data):
    response = await client.get(
        "/api/v1/organizations/geo?bbox=60.5,56.7,60.7,56.9",
        headers=api_headers,
    )

    assert response.status_code == 200
    payload = response.json()
    names = {item["name"] for item in payload["data"]}
    assert names == {'ООО "Рога и Копыта"'}
