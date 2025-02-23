import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from mydatabase import User, Event, Ticket

# Создаем тестовую базу данных
@pytest.fixture
def test_db():
    engine = create_engine('sqlite:///:memory:')  # Используем SQLite в памяти
    from mydatabase import Base
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

# Тест создания пользователя
def test_create_user(test_db):
    new_user = User(username="testuser", password_hash="hashed_password", email="test@example.com")
    test_db.add(new_user)
    test_db.commit()
    user = test_db.query(User).filter_by(username="testuser").first()
    assert user is not None

# Тест создания мероприятия
def test_create_event(test_db):
    new_event = Event(title="Test Event", description="A test event", start_date="2023-10-01 10:00:00", end_date="2023-10-01 12:00:00", location="Test Location")
    test_db.add(new_event)
    test_db.commit()
    event = test_db.query(Event).filter_by(title="Test Event").first()
    assert event is not None

# Тест покупки билета
def test_purchase_ticket(test_db):
    user = User(username="ticketuser", password_hash="hashed_password", email="ticket@example.com")
    test_db.add(user)
    event = Event(title="Ticket Event", description="An event with tickets", start_date="2023-10-01 10:00:00", end_date="2023-10-01 12:00:00", location="Test Location")
    test_db.add(event)
    test_db.commit()

    ticket = Ticket(user_id=user.user_id, event_id=event.event_id, price=100.0)
    test_db.add(ticket)
    test_db.commit()

    purchased_ticket = test_db.query(Ticket).filter_by(user_id=user.user_id, event_id=event.event_id).first()
    assert purchased_ticket is not None