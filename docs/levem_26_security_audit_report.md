# Аудит и разбор внедрения мер безопасности в Levem

## Аутентификация и хеширование паролей

В проекте Levem реализована система регистрации и авторизации пользователей с использованием безопасного хеширования паролей через алгоритм bcrypt. Пароли никогда не хранятся в открытом виде.

### Регистрация пользователя:

```python
class RegistrationAndAuthorization:
    def add_user(self) -> bool:
        if self.user_exists(user_name, input_email):
            logging.warning(f'Пользователь с логином {user_name} или почтой уже существует.')
            return False
            
        if not self.check_password_strength(password):
            logging.warning('Пароль не соответствует требованиям.')
            return False
            
        new_user = User(
            username=user_name,
            password_hash=self.hash_password(password),
            email=input_email,
            role='User'
        )
        self.session.add(new_user)
        self.session.commit()
        return True
        
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
```

• Пароль хешируется с использованием bcrypt и соли
• Проверяется сложность пароля (минимум 10 символов, 2 заглавные буквы, 3 буквы)
• Проверяется уникальность логина и email

### Аутентификация (вход):

```python
def login_account(self) -> bool:
    user = self.session.query(User).filter(User.username == username).first()
    
    if user is None:
        logging.warning(f'Попытка входа с несуществующим логином: {username}.')
        return False
        
    if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        self.current_user_id = user.user_id
        return True
```

• Сравнение пароля происходит через bcrypt.checkpw()
• Сохраняется ID текущего пользователя для контроля доступа

## Контроль доступа к мероприятиям

Добавлено поле organizer_id в модель Event для связи события с создателем. Пользователи могут видеть и изменять только свои мероприятия.

### Создание мероприятия с привязкой к владельцу:

```python
class OrganizerInterface:
    def create_event(self, organizer_id: int, title: str, description: str, start_date, end_date, location: str):
        organizer = self.session.query(User).filter(User.user_id == organizer_id).first()
        if not organizer:
            print("Ошибка: Пользователь не найден.")
            return False
            
        new_event = Event(
            organizer_id=organizer_id,
            title=title,
            description=description,
            start_date=datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S'),
            end_date=datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S'),
            location=location
        )
        self.session.add(new_event)
        self.session.commit()
        return True
```

### Фильтрация мероприятий по владельцу:

```python
def view_my_events(self, user_id: int):
    events = self.session.query(Event).filter(Event.organizer_id == user_id).all()
    if not events:
        print("У вас нет созданных мероприятий.")
        return []
        
    print("Ваши мероприятия:")
    for event in events:
        print(f"ID: {event.event_id}, Название: {event.title}, Место: {event.location}")
    return events
```

### Проверка владельца при операциях:

```python
def update_event(self, user_id: int, event_id: int, title: str = None, description: str = None, location: str = None):
    event = self.session.query(Event).filter(
        Event.event_id == event_id, 
        Event.organizer_id == user_id
    ).first()
    
    if not event:
        print("Ошибка: Мероприятие не найдено или у вас нет прав доступа.")
        return False
```

• Каждое мероприятие привязано к creator-у через organizer_id
• Запросы фильтруются по владельцу
• При отсутствии совпадения возвращается ошибка доступа

## Контроль доступа к билетам

Пользователи видят только свои билеты, а организаторы могут просматривать статистику по своим мероприятиям.

### Просмотр личных билетов:

```python
def view_my_tickets(self, user_id: int):
    tickets = self.session.query(Ticket).filter(Ticket.user_id == user_id).all()
    if not tickets:
        print("У вас нет приобретенных билетов.")
        return []
        
    print("Ваши билеты:")
    for ticket in tickets:
        event = self.session.query(Event).filter(Event.event_id == ticket.event_id).first()
        event_title = event.title if event else "Неизвестное мероприятие"
        print(f"Билет ID: {ticket.ticket_id}, Мероприятие: {event_title}, Цена: {ticket.price}")
    return tickets
```

### Доступ к статистике мероприятия:

```python
def view_event_tickets(self, user_id: int, event_id: int):
    event = self.session.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        print("Ошибка: Мероприятие не найдено.")
        return []
        
    if event.organizer_id != user_id:
        print("Ошибка 403: У вас нет прав доступа к этой информации.")
        return []
```

• Билеты фильтруются по user_id владельца
• Статистика доступна только владельцу мероприятия
• Возвращается ошибка 403 при попытке доступа к чужим данным

## Защита от несанкционированного доступа

В главном меню добавлена проверка авторизации перед доступом к функциям.

### Главное меню с проверками:

```python
def main():
    app = RegistrationAndAuthorization()
    
    if not app.registration_menu():
        return
        
    org_app = OrganizerInterface(app.session)
    buy_app = TicketPurchaseInterface(app.session)
    
    while True:
        print(f"\\nДобро пожаловать, пользователь ID: {app.current_user_id}")
        print("1 - создать мероприятие")
        print("2 - купить билет")
        print("3 - мои мероприятия")
        print("4 - мои билеты")
        print("5 - выход")
```

• Без успешной авторизации пользователь не может использовать приложение
• Все операции требуют аутентификации
• current_user_id сохраняется в сессии

## Результаты тестирования

Проведено комплексное тестирование всех функций безопасности:

```
=== Тестирование системы безопасности Levem ===

✓ Создание тестовых пользователей: test1, test2
✓ Контроль доступа к мероприятиям: пользователи видят только свои события
✓ Защита от несанкционированных операций: попытки изменения чужих данных блокируются
✓ Контроль доступа к билетам: пользователи видят только свои билеты
✓ Ошибка 403: возникает при попытке доступа к чужим мероприятиям
```

• Тесты подтвердили корректную работу всех мер безопасности
• Все попытки несанкционированного доступа блокируются
• Пользователи могут выполнять операции только со своими данными

## Вывод

В проекте Levem реализованы все базовые меры безопасности:

• Хеширование паролей с использованием bcrypt
• Аутентификация и авторизация пользователей
• Контроль доступа к мероприятиям по владельцу
• Контроль доступа к билетам по владельцу
• Защита от несанкционированных операций
• Возврат ошибки 403 при попытке доступа к чужим данным

Это обеспечивает защиту аккаунтов и данных пользователей от несанкционированного доступа.