import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mydatabase import Base, User, Ticket, Event
from main import RegistrationAndAuthorization, TicketPurchaseInterface
from datetime import datetime

# Создаем тестовую базу данных
engine = create_engine('sqlite:///test_database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class TestTicketPurchaseInterface(unittest.TestCase):

    def setUp(self):
        # Очищаем таблицы перед каждым тестом
        self.session = Session()
        self.session.query(Ticket).delete()
        self.session.query(Event).delete()
        self.session.query(User).delete()
        self.session.commit()

        # Создаем тестовые данные
        self.user = User(username="testuser", password_hash="hash", email="test@example.com", role="User")
        self.event1 = Event(
            title="Концерт группы XYZ",
            description="Не пропустите концерт группы XYZ в этом месяце!",
            start_date=datetime(2023, 11, 15, 20, 0, 0),
            end_date=datetime(2023, 11, 15, 23, 0, 0),
            location="Городской стадион"
        )
        self.event2 = Event(
            title="Выставка современного искусства",
            description="Не пропустите уникальную выставку современных художников!",
            start_date=datetime(2023, 12, 1, 10, 0, 0),
            end_date=datetime(2023, 12, 1, 18, 0, 0),
            location="Галерея искусств"
        )
        self.session.add(self.user)
        self.session.add(self.event1)
        self.session.add(self.event2)
        self.session.commit()

        self.ticket_purchase = TicketPurchaseInterface(self.session)

    def tearDown(self):
        # Очищаем таблицы после каждого теста
        self.session.query(Ticket).delete()
        self.session.query(Event).delete()
        self.session.query(User).delete()
        self.session.commit()
        self.session.close()

    def test_purchase_ticket_success(self):
        # Тестирование успешной покупки билета
        user_id = self.user.user_id
        event_id = self.event1.event_id
        price = 100.0

        result = self.ticket_purchase.purchase_ticket(user_id, event_id, price)
        self.assertTrue(result)

        # Проверяем, что билет создан в базе данных
        ticket = self.session.query(Ticket).filter_by(user_id=user_id, event_id=event_id).first()
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.price, price)

    def test_purchase_ticket_invalid_user(self):
        # Тестирование попытки купить билет с несуществующим пользователем
        user_id = 999  # Несуществующий ID пользователя
        event_id = self.event1.event_id
        price = 100.0
        result = self.ticket_purchase.purchase_ticket(user_id, event_id, price)
        self.assertFalse(result)

        # Проверяем, что билет не создан
        ticket = self.session.query(Ticket).filter_by(user_id=user_id, event_id=event_id).first()
        self.assertIsNone(ticket)

    def test_purchase_ticket_invalid_event(self):
        # Тестирование попытки купить билет на несуществующее мероприятие
        user_id = self.user.user_id
        event_id = 999  # Несуществующий ID мероприятия
        price = 100.0

        result = self.ticket_purchase.purchase_ticket(user_id, 
                                                      event_id, price)
        self.assertFalse(result)

        # Проверяем, что билет не создан
        ticket = self.session.query(Ticket).filter_by(user_id=user_id, 
        event_id=event_id).first()
        self.assertIsNone(ticket)


if __name__ == '__main__':
    unittest.main()