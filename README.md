# multi-reference-api

REST API справочник организаций/зданий/деятельностей на FastAPI + SQLAlchemy + Alembic + PostGIS.

## Запуск через Docker

1) Создать `.env`:

```bash
cp .env.example .env
```

1) Запуск контейнеров:

```bash
docker compose up --build
```

1) Применить миграции:

```bash
docker compose exec app alembic upgrade head
```

1) Заполнить тестовыми данными:

```bash
docker compose exec app python -m app.seed
```

API доступен на `http://localhost:8000`.

## Документация

- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

## Тесты

После запуска контейнеров:

```bash
docker compose exec app pytest
```

Для отдельных наборов:

```bash
docker compose exec app pytest -m "unit"
docker compose exec app pytest -m "integration"
```

## Аутентификация

Используется статический API‑ключ через заголовок `X-API-Key`.

Пример:

```bash
curl -H "X-API-Key: change-me" http://localhost:8000/api/v1/buildings
```

## Эндпоинты

- `GET /api/v1/buildings` — список зданий
- `GET /api/v1/organizations/{id}` — организация по идентификатору
- `GET /api/v1/organizations/by-building/{building_id}` — организации в здании
- `GET /api/v1/organizations/by-activity/{activity_id}?include_descendants=true|false`
- `GET /api/v1/organizations/search?name=...` — поиск по названию
- `GET /api/v1/organizations/geo?lat=...&lon=...&radius_m=...` — поиск в радиусе (метры)
- `GET /api/v1/organizations/geo?bbox=min_lon,min_lat,max_lon,max_lat` — поиск в прямоугольнике

## Переменные окружения

- `DATABASE_URL` — строка подключения, пример: `postgresql+asyncpg://app:app@db:5432/app`
- `API_KEY` — статический ключ
- `API_KEY_HEADER` — имя заголовка (по умолчанию `X-API-Key`)
