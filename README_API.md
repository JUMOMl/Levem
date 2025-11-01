# Levem API

REST API для управления мероприятиями в системе Levem.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите API сервер:
```bash
python api.py
```

API будет доступен на http://localhost:5000

## Авторизация

Для доступа к API используется API-ключ: `levem_api_key_2024`

Ключ должен передаваться в заголовке `X-API-Key`.

## Эндпоинты

### 1. Создание мероприятия
- **Метод:** POST
- **URL:** `/api/events`
- **Заголовки:** `X-API-Key: levem_api_key_2024`
- **Тело запроса (JSON):**
```json
{
    "organizer_id": 1,
    "title": "IT Конференция 2024",
    "description": "Ежегодная конференция по информационным технологиям",
    "start_date": "2024-12-01 10:00:00",
    "end_date": "2024-12-01 18:00:00",
    "location": "Москва, ул. Примерная, 1"
}
```

### 2. Получение всех мероприятий
- **Метод:** GET
- **URL:** `/api/events`
- **Заголовки:** `X-API-Key: levem_api_key_2024`

### 3. Получение мероприятий пользователя
- **Метод:** GET
- **URL:** `/api/events/my/{user_id}`
- **Заголовки:** `X-API-Key: levem_api_key_2024`

### 4. Удаление мероприятия
- **Метод:** DELETE
- **URL:** `/api/events/{event_id}`
- **Заголовки:** `X-API-Key: levem_api_key_2024`
- **Тело запроса (JSON):**
```json
{
    "user_id": 1
}
```

### 5. Проверка состояния API
- **Метод:** GET
- **URL:** `/api/health`

## Тестирование с curl

### Создание мероприятия:
```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -H "X-API-Key: levem_api_key_2024" \
  -d '{
    "organizer_id": 1,
    "title": "IT Конференция 2024",
    "description": "Ежегодная конференция по IT",
    "start_date": "2024-12-01 10:00:00",
    "end_date": "2024-12-01 18:00:00",
    "location": "Москва"
  }'
```

### Получение всех мероприятий:
```bash
curl -X GET http://localhost:5000/api/events \
  -H "X-API-Key: levem_api_key_2024"
```

### Получение мероприятий пользователя:
```bash
curl -X GET http://localhost:5000/api/events/my/1 \
  -H "X-API-Key: levem_api_key_2024"
```

### Удаление мероприятия:
```bash
curl -X DELETE http://localhost:5000/api/events/1 \
  -H "Content-Type: application/json" \
  -H "X-API-Key: levem_api_key_2024" \
  -d '{"user_id": 1}'
```

### Проверка состояния:
```bash
curl -X GET http://localhost:5000/api/health
```

## Примеры ошибок

### Отсутствие API-ключа:
```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{"title": "Тест"}'
# Ответ: 401 Unauthorized
```

### Невалидные данные:
```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -H "X-API-Key: levem_api_key_2024" \
  -d '{"description": "Без title"}'
# Ответ: 400 Bad Request
```

### Удаление несуществующего мероприятия:
```bash
curl -X DELETE http://localhost:5000/api/events/999 \
  -H "Content-Type: application/json" \
  -H "X-API-Key: levem_api_key_2024" \
  -d '{"user_id": 1}'
# Ответ: 404 Not Found
```

### Нет прав доступа:
```bash
curl -X DELETE http://localhost:5000/api/events/1 \
  -H "Content-Type: application/json" \
  -H "X-API-Key: levem_api_key_2024" \
  -d '{"user_id": 999}'
# Ответ: 404 Event not found or access denied
```

## Формат ответа

### Успешное создание мероприятия:
```json
{
  "message": "Event created successfully",
  "event": {
    "event_id": 1,
    "organizer_id": 1,
    "title": "IT Конференция 2024",
    "description": "Ежегодная конференция по IT",
    "start_date": "2024-12-01T10:00:00",
    "end_date": "2024-12-01T18:00:00",
    "location": "Москва"
  }
}
```

### Список мероприятий:
```json
{
  "events": [
    {
      "event_id": 1,
      "organizer_id": 1,
      "title": "IT Конференция 2024",
      "description": "Ежегодная конференция по IT",
      "start_date": "2024-12-01T10:00:00",
      "end_date": "2024-12-01T18:00:00",
      "location": "Москва"
    }
  ],
  "total": 1
}
```