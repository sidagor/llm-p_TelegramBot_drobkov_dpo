# llm-p — Auth Service + Telegram Bot + RabbitMQ + Celery + OpenRouter

##  Описание проекта

Данный проект представляет собой систему из двух независимых сервисов:

Auth Service — отвечает за регистрацию пользователей, аутентификацию и выпуск JWT-токенов.
Bot Service — Telegram-бот, который принимает сообщения пользователей и отправляет запросы к LLM через очередь задач.

Для обработки запросов к языковой модели используется асинхронная очередь задач:
- Telegram Bot публикует задачу в RabbitMQ.
- Celery Worker получает задачу и обращается к OpenRouter API.
- Redis используется для хранения JWT-токенов пользователей и может использоваться как backend Celery.
- После получения ответа Worker отправляет результат пользователю в Telegram.


## Архитектура проекта

Архитектура построена таким образом, что Auth Service и Bot Service не зависят друг от друга напрямую. Bot Service не хранит пользователей и не обращается к базе данных Auth   
Service. Доступ к функционалу бота осуществляется только по валидному JWT-токену, выданному Auth Service.    
  
Auth Service  

User  
 │    
 FastAPI (Auth Service)  
 │  
 ├── POST /auth/register  
 ├── POST /auth/login  
 └── GET  /auth/me  
 │    
 SQLite  
 │    
JWT Token    
  
Auth Service отвечает за:

- регистрацию пользователей;
- хранение пользователей в SQLite;
- хеширование паролей (bcrypt);
- выдачу JWT;
- проверку JWT через endpoint /auth/me.    
  
Bot Service  

Telegram User  
      │    
Telegram Bot (Aiogram)  
      │  
    Redis  
      │  
      └── JWT пользователя  
      │    
JWT Validation  
      │    
RabbitMQ (Broker)  
      │    
 Celery Worker    
   
 Bot Service отвечает за:

приём сообщений Telegram;
- хранение JWT пользователя в Redis;
- проверку подписи и срока действия JWT;
- публикацию задач в RabbitMQ;
- обработку запросов к LLM через Celery Worker;
- отправку ответа пользователю.  

## Структура проекта

```text
llm-p/
├── auth_service/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── usecases/
│   │   └── main.py
│   ├── tests/
│   ├── app.db
│   ├── pytest.ini
│   └── pyproject.toml
│
├── bot_service/
│   ├── app/
│   │   ├── bot/
│   │   ├── core/
│   │   ├── infra/
│   │   ├── services/
│   │   ├── tasks/
│   │   └── main.py
│   ├── tests/
│   ├── pytest.ini
│   └── pyproject.toml
│
├── docker-compose.yml
├── README.md
└── uv.lock
```

### Назначение компонентов

#### Auth Service

* `api/` — HTTP endpoint'ы FastAPI.
* `core/` — настройки, безопасность, JWT, исключения.
* `db/` — модели и подключение к SQLite.
* `repositories/` — работа с базой данных.
* `usecases/` — бизнес-логика авторизации.
* `tests/` — unit и integration тесты.

#### Bot Service

* `bot/` — Telegram-хендлеры и запуск aiogram.
* `core/` — JWT-проверка и исключения.
* `infra/` — Redis и Celery инфраструктура.
* `services/` — клиент OpenRouter.
* `tasks/` — Celery задачи.
* `tests/` — unit, mock и integration тесты.

```
```


## Основные возможности:

### Auth Service
- Регистрация пользователей
- Хеширование паролей (bcrypt)
- JWT-аутентификация
- Endpoint получения информации о текущем пользователе
- Проверка ролей пользователей
- SQLite база данных  

### Bot Service
- Telegram-бот на Aiogram
- Авторизация через JWT
- Привязка JWT к Telegram User ID
- Проверка подписи и срока действия токена
- Асинхронная обработка запросов через Celery
- Очередь задач RabbitMQ
- Хранение JWT в Redis
- Интеграция с OpenRouter API  

---

## Технологии

### Auth Service
- FastAPI
- SQLAlchemy Async
- SQLite
- JWT (python-jose)
- Passlib (bcrypt)
- Pydantic  

### Bot Service
- Aiogram
- Celery
- RabbitMQ
- Redis
- OpenRouter API
- HTTPX  

### Тестирование
- Pytest
- Fakeredis
- Pytest-Mock
- RESPX

---

## Установка и запуск

### 1. Установка uv

```bash
pip install uv
```

---  
  
### 2. Клонирование проекта
```bash
git clone <repository_url>
```

cd llm-p  
---  
  

### 3. Настройка Auth Service

```bash
cd auth_service
```

- Cоздание виртуального окружения:
```bash
uv venv
```
---

- Активация:
```bash
source .venv/bin/activate
```
---

- Установка зависимостей:
```bash
uv pip install -r <(uv pip compile pyproject.toml)
```

---

- Запуск сервиса:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

- Swagger:

После запуска откройте:

```
http://localhost:8000/docs
```

---

### 4.Запуск инфраструктуры

- Из корня проекта:

```bash
docker compose up -d
```
---

- Проверить контейнеры:

```bash
docker ps
```
---

После запуска будут доступны:

- RabbitMQ Broker — localhost:5672
- RabbitMQ Management UI — http://localhost:15672
- Redis — localhost:6379

- Открыть панель управления RabbitMQ:

http://localhost:15672

Стандартные учётные данные:  

username: guest  
password: guest  

После входа можно:
- просматривать очереди (Queues)
- отслеживать задачи Celery
- контролировать подключения (Connections)
- просматривать обменники (Exchanges)
- мониторить нагрузку брокера

### 5. Настройка Bot Service

```bash
cd ../bot_service
```
---
- Cоздание виртуального окружения:
```bash
uv venv
```
---

- Активация:
```bash
source .venv/bin/activate
```
---

- Установка зависимостей:
```bash
uv pip install -r <(uv pip compile pyproject.toml)
```

---

- Настройка .env

В файле `.env.example` найдите строчку OPENROUTER_API_KEY, вставьте туда ваш API ключ, который можно получить здесь: https://openrouter.ai/.  

Затем создайте Telegram-бота через @BotFather и вставьте полученный токен в переменную TELEGRAM_BOT_TOKEN.  

Если для доступа к Telegram вам требуется VPN или прокси, укажите адрес прокси в переменной TELEGRAM_PROXY.  
Если Telegram доступен напрямую, оставьте это поле пустым.  
  
После заполнения всех необходимых переменных переименуйте файл .env.example в .env.  
---

- Запуск Telegram Bot

Из директории bot_service:
```bash
uv run python -m app.bot.run
```
---
- Запуск Celery Worker

Из директории bot_service:
```bash
uv run celery \
  -A app.infra.celery_app.celery_app worker \
  --loglevel=info
```  
---

## Использование

### Получение JWT  

1. Откройте Swagger:  
http://localhost:8000/docs  

2. Зарегистрируйтесь через:  
POST /auth/register  

3. Выполните вход через:  
POST /auth/login  

4. Скопируйте полученный JWT.  

### Авторизация в Telegram

1. Отправьте боту:

/start

Бот вас поприветсвует и попросит ваш JWT токен. 


2. Вставьте его с помощью команды:

/token <jwt>  

Например:  

/token eyJhbGciOiJIUzI1NiIs...  

После успешной авторизации бот сохранит токен в Redis.

### Работа с LLM

После авторизации отправьте любое текстовое сообщение боту.  

Бот:
- Проверит JWT.
- Отправит задачу в RabbitMQ.
- Celery Worker выполнит запрос к OpenRouter.
- Ответ будет отправлен пользователю в Telegram.

## Запуск тестов  

###  Auth Service  

cd auth_service  
uv run pytest -v  

### Bot Service  

cd bot_service  
uv run pytest -v

## Реализованные тесты  

### Auth Service  

Unit Tests
- Хеширование паролей
- Проверка паролей
- Генерация JWT
- Проверка JWT
- Проверка истёкших токенов  

Integration Tests
- Регистрация пользователя
- Логин пользователя
- Получение профиля через JWT  

Negative Tests
- Повторная регистрация
- Неверный пароль
- Отсутствие JWT
- Некорректный JWT  

### Bot Service  

Unit Tests
- Проверка JWT
- Проверка невалидного JWT  

Mock Tests
- Сохранение JWT в Redis
- Обработка сообщений без JWT
- Публикация задачи в Celery  

Integration Tests
- OpenRouter Client через RESPX
- Проверка обработки ответов OpenRouter
- Проверка обработки ошибок OpenRouter




## Демонстрация работы API

---

### Регистрация пользователя

```

```

---

### Логин и получение JWT

```

```

---

### Авторизация в Swagger

Нажать кнопку **Authorize** и вставить:

```
Bearer <ваш_токен>
```

```

```

---

### POST /chat

Отправка запроса к LLM:


```

```

---

### GET /chat/history

Получение истории сообщений:

```

```

---

### DELETE /chat/history

Очистка истории:

```

```

---

## Примечание

В проекте использован openrouter/free, который автоматически выбирает самую доступную из бесплатных моделей. В процессе работы над проектом stepfun/step-3.5-flash перестала быть бесплатной, поэтому было решено использовать другие модели.

```

```

---

