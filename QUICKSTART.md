# Levem API - Краткая инструкция

## Быстрый запуск

1. **Установите зависимости:**
   ```bash
   pip install flask==2.3.3 sqlalchemy==1.4.46
   ```

2. **Инициализируйте базу данных:**
   ```bash
   python create_test_db.py
   ```

3. **Запустите API:**
   ```bash
   python api.py
   ```

API будет доступен на http://localhost:5000

## API-ключ
`levem_api_key_2024`

## Основные команды

### Создать мероприятие:
```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -H "X-API-Key: levem_api_key_2024" \
  -d '{
    "organizer_id": 3,
    "title": "Новое мероприятие",
    "description": "Описание",
    "start_date": "2024-12-01 10:00:00",
    "end_date": "2024-12-01 18:00:00",
    "location": "Москва"
  }'
```

### Получить все мероприятия:
```bash
curl -X GET http://localhost:5000/api/events \
  -H "X-API-Key: levem_api_key_2024"
```

### Удалить мероприятие:
```bash
curl -X DELETE http://localhost:5000/api/events/1 \
  -H "Content-Type: application/json" \
  -H "X-API-Key: levem_api_key_2024" \
  -d '{"user_id": 3}'
```

### Проверить состояние:
```bash
curl -X GET http://localhost:5000/api/health
```

## Файлы проекта

- `api.py` - основной API файл
- `README_API.md` - подробная документация
- `test_report.md` - отчет о тестировании
- `create_test_db.py` - скрипт создания БД
- `test_levem.db` - тестовая база данных

**Все задания выполнены согласно требованиям!**