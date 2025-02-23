import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mydatabase import Base, User, Event, Ticket

# Используем SQLite in-memory для тестов
TEST_DATABASE_URL = "sqlite:///:memory:"

# Создаем движок для тестов
engine = create_engine(TEST_DATABASE_URL)

# Создаем фабрику сессий
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

@pytest.fixture(scope="function")
def db_session():
    """Фикстура для создания тестовой базы данных и сессии"""
    # Создаем таблицы в памяти
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    yield session  # Передаем сессию в тест

    # Очищаем БД после теста
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(db_session):
    """Проверяем создание пользователя"""
    new_user = User(username="testuser", email="test@example.com", password_hash="hashedpassword")
    db_session.add(new_user)
    db_session.commit()

    user_from_db = db_session.query(User).filter_by(username="testuser").first()
    assert user_from_db is not None
    assert user_from_db.email == "test@example.com"

def test_create_event(db_session):
    """Проверяем создание мероприятия"""
    new_event = Event(title="Test Event", description="This is a test event")
    db_session.add(new_event)
    db_session.commit()

    event_from_db = db_session.query(Event).filter_by(title="Test Event").first()
    assert event_from_db is not None
    assert event_from_db.description == "This is a test event"
