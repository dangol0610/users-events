# Users & Events Service

Сервис управления пользователями и событиями с асинхронной архитектурой на базе **FastAPI**.

## 📋 Описание

REST API сервис для регистрации, аутентификации пользователей и управления событиями. Поддерживает:

- ✅ JWT аутентификацию (access + refresh токены)
- ✅ Кэширование в Redis
- ✅ Асинхронную обработку сообщений через RabbitMQ + FastStream
- ✅ Фоновые задачи через Celery
- ✅ Периодические задачи через Celery Beat
- ✅ Мониторинг задач через Flower

---

## 🏗 Архитектура

```
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI (app)                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐ │
│  │  Auth    │  │  Users   │  │  Events  │  │   Broker       │ │
│  │  Router  │  │  Router  │  │  Router  │  │   (publish)    │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───────┬────────┘ │
│       │             │             │                 │          │
│  ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐  ┌───────▼────────┐ │
│  │  Auth    │  │  Users   │  │  Events  │  │   RabbitMQ     │ │
│  │  Service │  │  Service │  │  Service │  │   (queue)      │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───────┬────────┘ │
│       │             │             │                 │          │
│  ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐         │          │
│  │  Auth    │  │  Users   │  │  Events  │         │          │
│  │  Repo    │  │  Repo    │  │  Repo    │         │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘         │          │
└───────┼─────────────┼─────────────┼────────────────┼──────────┘
        │             │             │                │
        ▼             ▼             ▼                ▼
   ┌────────┐   ┌──────────┐  ┌────────┐   ┌──────────────┐
   │  JWT   │   │ PostgreSQL│  │ Redis  │   │   Consumer   │
   │  Token │   │  (async)  │  │ (cache)│   │   (separate) │
   └────────┘   └──────────┘  └────────┘   └──────────────┘
                                                      │
                                                      ▼
                                               ┌──────────────┐
                                               │    Celery    │
                                               │   (worker)   │
                                               └──────────────┘
```

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd users_events
```

### 2. Настройка окружения

```bash
# Создать файл окружения
cp src/.env.docker src/.env

# Отредактировать настройки (при необходимости)
nano src/.env
```

### 3. Запуск через Docker Compose

```bash
# Запустить все сервисы
docker compose up -d

# Просмотреть логи
docker compose logs -f

# Остановить
docker compose down
```

---

## 📦 Сервисы

| Сервис | Порт | Описание |
|--------|------|----------|
| **app** | 8000 | FastAPI приложение |
| **postgres** | 5433 | PostgreSQL база данных |
| **redis** | 6377 | Redis для кэширования |
| **rabbitmq** | 5672, 15672 | RabbitMQ брокер сообщений |
| **consumer** | - | FastStream consumer |
| **celery-worker** | - | Celery worker для фоновых задач |
| **celery-beat** | - | Celery Beat для периодических задач |
| **flower** | 5555 | Мониторинг Celery задач |
| **pgadmin** | 5050 | Веб-интерфейс для PostgreSQL |
| **redisinsight** | 5540 | Веб-интерфейс для Redis |

---

## 🔌 API Endpoints

### Auth

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/auth/register` | Регистрация пользователя |
| POST | `/api/auth/login` | Вход (получение токенов) |
| POST | `/api/auth/refresh` | Обновление access токена |

### Users

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/users/me` | Получить текущий профиль |
| PATCH | `/api/users/me` | Обновить профиль |
| DELETE | `/api/users/me` | Удалить профиль |

### Events

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/events/` | Создать событие |
| GET | `/api/events/` | Получить список событий пользователя |

---

## 📝 Примеры использования

### Регистрация

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "john_doe",
    "password": "SecurePass123"
  }'
```

### Вход

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

### Создание события

```bash
curl -X POST http://localhost:8000/api/events/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "title": "Мое событие",
    "description": "Описание события"
  }'
```

### Получение событий

```bash
curl -X GET http://localhost:8000/api/events/ \
  -H "Authorization: Bearer <access_token>"
```

---

## 🗂 Структура проекта

```
src/
├── apps/
│   ├── auth/              # Аутентификация и авторизация
│   │   ├── dependencies.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── consumers/         # FastStream consumer
│   │   ├── events/
│   │   │   └── handlers.py
│   │   └── serve.py
│   ├── events/            # Управление событиями
│   │   ├── dependencies.py
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── services.py
│   └── users/             # Управление пользователями
│       ├── dependencies.py
│       ├── models.py
│       ├── repository.py
│       ├── routers.py
│       ├── schemas.py
│       └── services.py
├── broker/                # Конфигурация брокера
│   ├── schemas.py
│   └── serve.py
├── celery_app/            # Celery приложение
│   ├── __init__.py
│   ├── periodic.py
│   ├── signals.py
│   └── tasks.py
├── migrations/            # Alembic миграции
├── routers/
│   └── api_router.py
├── settings/
│   └── settings.py
├── tests/                 # Тесты
├── utils/
│   ├── database.py
│   ├── dependencies.py
│   ├── exceptions.py
│   ├── pwd_utils.py
│   ├── redis.py
│   └── token_utils.py
├── main.py
├── .env
└── .env.docker
```

---

## ⚙️ Конфигурация

### Переменные окружения

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_CACHE_DB=0
CACHE_TTL=3600

# RabbitMQ
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES_MINUTES=15
REFRESH_TOKEN_EXPIRES_DAYS=7
```

---

## 🧪 Тестирование

```bash
# Запустить тесты
docker compose exec app pytest

# Запустить тесты с покрытием
docker compose exec app pytest --cov=src

# Запустить тестовую БД
docker compose up postgres-test
```

---

## 🔧 Разработка

### Установка зависимостей

```bash
# Создать виртуальное окружение
uv venv

# Активировать
source .venv/bin/activate

# Установить зависимости
uv sync

# Добавить новую зависимость
uv add <package-name>
```

### Миграции базы данных

```bash
# Создать новую миграцию
docker compose exec app alembic revision --autogenerate -m "Description"

# Применить миграции
docker compose exec app alembic upgrade head

# Откатить миграцию
docker compose exec app alembic downgrade -1
```

---

## 📊 Мониторинг

### Flower (Celery)

Открой http://localhost:5555 для просмотра:
- Статус задач
- Прогресс выполнения
- История задач
- Воркеры

### RabbitMQ Management

Открой http://localhost:15672 (guest/guest) для просмотра:
- Очереди сообщений
- Консьюмеры
- Статистика

### pgAdmin

Открой http://localhost:5050 (admin@admin.com/admin) для:
- Просмотра таблиц
- Выполнения запросов
- Управления БД

### RedisInsight

Открой http://localhost:5540 для:
- Просмотра ключей Redis
- Анализа кэша
- Мониторинга памяти

---

## 🛠 Технологии

| Категория | Технологии |
|-----------|-----------|
| **Framework** | FastAPI, Pydantic |
| **Database** | PostgreSQL, SQLAlchemy 2.0, Alembic |
| **Cache** | Redis |
| **Message Queue** | RabbitMQ, FastStream |
| **Task Queue** | Celery, Celery Beat |
| **Auth** | JWT, python-jose, passlib, bcrypt |
| **Container** | Docker, Docker Compose |
| **Package Manager** | uv |
| **Python** | 3.12+ |

---

## 📈 Архитектурные решения

### Repository Pattern

```
Router → Service → Repository → Database
```

Разделение ответственности:
- **Router** — HTTP запросы/ответы
- **Service** — Бизнес-логика
- **Repository** — Работа с БД

### Кэширование

- Пользователи кэшируются в Redis по ключу `user:{id}`
- TTL настраивается через `CACHE_TTL`
- Кэш инвалидируется при обновлении/удалении

### Сообщения (FastStream)

При создании события публикуется сообщение в очередь `events.created`:

```python
EventCreatedMessage(
    event_id: int,
    user_id: int,
    title: str,
    description: str,
    created_at: datetime,
)
```

### Фоновые задачи (Celery)

- Отложенные задачи (email, уведомления)
- Периодические задачи (очистка кэша, отчёты)
- Долгие задачи (генерация PDF, экспорт)

---

## 🔒 Безопасность

- Пароли хэшируются через bcrypt
- JWT токены с ограниченным временем жизни
- Refresh токены для обновления сессии
- Валидация входных данных через Pydantic

---
