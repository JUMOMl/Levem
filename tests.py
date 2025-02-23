import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mydatabase import Base, Event, User, Ticket
from ticketPurchaseInterface import TicketPurchaseInterface

DATABASE_URL = "sqlite:///:memory:"  # Используем временную базу в памяти для тестов

@pytest.fixture
def session():
    """Создает тестовую сессию базы данных."""
    engine = create_engine(DATABASE_URL)
    TestingSession = sessionmaker(bind=engine)
    session = TestingSession()
    
    Base.metadata.create_all(engine)  # Создаем таблицы

    yield session  # Передаем управление тесту

    session.close()
    Base.metadata.drop_all(engine)  # Удаляем таблицы после тестов

@pytest.fixture
def ticket_interface(session):
    """Создает объект TicketPurchaseInterface с тестовой сессией."""
    return TicketPurchaseInterface(session)

@pytest.fixture
def sample_data(session):
    """Добавляет тестовые данные в базу."""
    user = User(user_id=1, name="Тестовый пользователь")
    event = Event(event_id=1, title="Концерт", location="Москва")
    session.add_all([user, event])
    session.commit()

def test_view_available_events(ticket_interface, session, sample_data):
    """Тест просмотра доступных мероприятий."""
    events = ticket_interface.view_available_events()
    assert len(events) == 1
    assert events[0].title == "Концерт"

def test_purchase_ticket_success(ticket_interface, session, sample_data):
    """Тест успешной покупки билета."""
    success = ticket_interface.purchase_ticket(user_id=1, event_id=1, price=500)
    assert success
    assert session.query(Ticket).count() == 1

def test_purchase_ticket_invalid_user(ticket_interface, session, sample_data):
    """Тест покупки билета с несуществующим пользователем."""
    success = ticket_interface.purchase_ticket(user_id=99, event_id=1, price=500)
    assert not success
    assert session.query(Ticket).count() == 0

def test_purchase_ticket_invalid_event(ticket_interface, session, sample_data):
    """Тест покупки билета на несуществующее мероприятие."""
    success = ticket_interface.purchase_ticket(user_id=1, event_id=99, price=500)
    assert not success
    assert session.query(Ticket).count() == 0
