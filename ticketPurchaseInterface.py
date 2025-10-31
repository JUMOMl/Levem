import logging
from sqlalchemy.exc import SQLAlchemyError
from mydatabase import Ticket, Event, User

class TicketPurchaseInterface:
    def __init__(self, session):
        self.session = session
        
    def view_available_events(self):
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
        
    def view_my_tickets(self, user_id: int):
        try:
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
            
        except SQLAlchemyError as e:
            logging.error(f"Ошибка при просмотре билетов: {e}")
            print("Ошибка: Не удалось загрузить билеты.")
            return []
            
    def purchase_ticket(self, user_id: int, event_id: int, price: float):
        if price < 0:
            logging.warning(f"Отрицательная цена билета.")
            print("Ошибка: Отрицательная цена билета.")
            return False
            
        try:
            user = self.session.query(User).filter(User.user_id == user_id).first()
            if not user:
                logging.warning(f"Пользователь с ID {user_id} не найден.")
                print("Ошибка: Пользователь не найден.")
                return False
                
            event = self.session.query(Event).filter(Event.event_id == event_id).first()
            if not event:
                logging.warning(f"Мероприятие с ID {event_id} не найдено.")
                print("Ошибка: Мероприятие не найдено.")
                return False
                
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
            
    def view_event_tickets(self, user_id: int, event_id: int):
        try:
            event = self.session.query(Event).filter(Event.event_id == event_id).first()
            if not event:
                print("Ошибка: Мероприятие не найдено.")
                return []
                
            if event.organizer_id != user_id:
                print("Ошибка 403: У вас нет прав доступа к этой информации.")
                return []
                
            tickets = self.session.query(Ticket).filter(Ticket.event_id == event_id).all()
            if not tickets:
                print("На это мероприятие пока не продано ни одного билета.")
                return []
                
            print(f"Билеты на мероприятие '{event.title}':")
            total_revenue = 0
            for ticket in tickets:
                user = self.session.query(User).filter(User.user_id == ticket.user_id).first()
                username = user.username if user else "Неизвестный пользователь"
                print(f"Билет ID: {ticket.ticket_id}, Пользователь: {username}, Цена: {ticket.price}")
                total_revenue += float(ticket.price)
                
            print(f"Общий доход: {total_revenue}")
            return tickets
            
        except SQLAlchemyError as e:
            logging.error(f"Ошибка при просмотре билетов мероприятия: {e}")
            print("Ошибка: Не удалось загрузить информацию о билетах.")
            return []