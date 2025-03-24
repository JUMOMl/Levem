import logging
from sqlalchemy.exc import SQLAlchemyError
from mydatabase import Ticket, Event, User
class TicketPurchaseInterface:
    def __init__(self, session):
        """
        Инициализация интерфейса для покупки билетов.
        ООП: Инкапсуляция - сохранение сессии базы данных внутри объекта.

        Args:
            session: Сессия базы данных SQLAlchemy.
        """
        self.session = session

    def view_available_events(self):
        """
        Вывод списка доступных мероприятий с ценами билетов.
        ООП: Полиморфизм - метод адаптирован для работы с различными наборами данных.

        Returns:
            list: Список доступных мероприятий.
        """
        events = self.session.query(Event).all()
        if not events:
            print("Нет доступных мероприятий.")
            return []

        print("Доступные мероприятия:")
        for event in events:
            ticket_prices = self.session.query(Ticket.price).filter(Ticket.event_id == event.event_id).all()
            price_list = [float(price[0]) for price in ticket_prices] if ticket_prices else [0.0]
            min_price = min(price_list) if price_list else "N/A"
            print(f"ID: {event.event_id}, Название: {event.title}, Место: {event.location}, Минимальная цена билета: {min_price}")
        return events
    
    
    
    def purchase_ticket(self, user_id: int, event_id: int, price: float):
        """
        Покупка билета на мероприятие.
        ООП: Инкапсуляция - метод скрывает внутренние операции покупки билета.

        Args:
            user_id (int): ID пользователя.
            event_id (int): ID мероприятия.
            price (float): Цена билета.

        Returns:
            bool: True, если билет успешно приобретен, иначе False.
        """
        
        if price < 0:
            logging.warning(f"Отрицательная цена билета.")
            print("Ошибка: Отрицательная цена билета.")
            return False
        try:
            # Проверяем, существует ли пользователь
            user = self.session.query(User).filter(User.user_id == user_id).first()
            if not user:
                logging.warning(f"Пользователь с ID {user_id} не найден.")
                print("Ошибка: Пользователь не найден.")
                return False

            # Проверяем, существует ли мероприятие
            event = self.session.query(Event).filter(Event.event_id == event_id).first()
            if not event:
                logging.warning(f"Мероприятие с ID {event_id} не найдено.")
                print("Ошибка: Мероприятие не найдено.")
                return False

            # Создаем запись о покупке билета
            ticket = Ticket(user_id=user_id, event_id=event_id, price=price)
            self.session.add(ticket)
            self.session.commit()

            logging.info(f"Пользователь с ID {user_id} успешно приобрел билет на мероприятие ID {event_id}.")
            print("Билет успешно приобретен!")
            return True

        except SQLAlchemyError as e:
            logging.error(f"Ошибка при покупке билета: {e}")
            self.session.rollback()
            print("Ошибка: Не удалось приобрести билет.")
            return False