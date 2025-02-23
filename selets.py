from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mydatabase import User, Event, Ticket, Base  # Убедитесь, что вы импортируете необходимые классы

DATABASE_URL = 'sqlite:///main_database.db'

# Создание движка базы данных
engine = create_engine(DATABASE_URL)

# Создание фабрики сессий
Session = sessionmaker(bind=engine)

# Создание новой сессии
session = Session()

# Выполнение SELECT запроса для получения всех пользователей
users = session.query(User).all()

# Вывод информации о пользователях
print("Пользователи:")
for user in users:
    print(f'ID: {user.user_id}, Username: {user.username}, Email: {user.email}, Created At: {user.created_at}, Role: {user.role}')

# Выполнение SELECT запроса для получения всех мероприятий
events = session.query(Event).all()

# Вывод информации о мероприятиях
print("\nМероприятия:")
for event in events:
    print(f'ID: {event.event_id}, Title: {event.title}, Description: {event.description}, Start Date: {event.start_date}, End Date: {event.end_date}, Location: {event.location}')

# Выполнение SELECT запроса для получения всех билетов
tickets = session.query(Ticket).all()

# Вывод информации о билетах
print("\nБилеты:")
for ticket in tickets:
    print(f'Ticket ID: {ticket.ticket_id}, User ID: {ticket.user_id}, Event ID: {ticket.event_id}, Purchase Date: {ticket.purchase_date}, Price: {ticket.price}')

# Закрытие сессии
session.close()