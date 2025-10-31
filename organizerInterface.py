from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from mydatabase import Event, User
import logging
from datetime import datetime

class OrganizerInterface:
    def __init__(self, session):
        self.session = session
        
    def create_event(self, organizer_id: int, title: str, description: str, start_date, end_date, location: str):
        try:
            organizer = self.session.query(User).filter(User.user_id == organizer_id).first()
            if not organizer:
                logging.warning(f"Пользователь с ID {organizer_id} не найден.")
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
            logging.info(f"Мероприятие '{title}' успешно создано организатором с ID {organizer_id}.")
            print("Мероприятие успешно создано!")
            return True
            
        except SQLAlchemyError as e:
            logging.error(f"Ошибка при создании мероприятия: {e}")
            self.session.rollback()
            print("Ошибка: Не удалось создать мероприятие.")
            return False
            
    def view_my_events(self, user_id: int):
        try:
            events = self.session.query(Event).filter(Event.organizer_id == user_id).all()
            if not events:
                print("У вас нет созданных мероприятий.")
                return []
                
            print("Ваши мероприятия:")
            for event in events:
                print(f"ID: {event.event_id}, Название: {event.title}, Место: {event.location}")
            return events
            
        except SQLAlchemyError as e:
            logging.error(f"Ошибка при просмотре мероприятий: {e}")
            print("Ошибка: Не удалось загрузить мероприятия.")
            return []
            
    def update_event(self, user_id: int, event_id: int, title: str = None, description: str = None, 
                    location: str = None):
        try:
            event = self.session.query(Event).filter(
                Event.event_id == event_id, 
                Event.organizer_id == user_id
            ).first()
            
            if not event:
                print("Ошибка: Мероприятие не найдено или у вас нет прав доступа.")
                return False
                
            if title:
                event.title = title
            if description:
                event.description = description
            if location:
                event.location = location
                
            self.session.commit()
            logging.info(f"Мероприятие ID {event_id} успешно обновлено.")
            print("Мероприятие успешно обновлено!")
            return True
            
        except SQLAlchemyError as e:
            logging.error(f"Ошибка при обновлении мероприятия: {e}")
            self.session.rollback()
            print("Ошибка: Не удалось обновить мероприятие.")
            return False
            
    def delete_event(self, user_id: int, event_id: int):
        try:
            event = self.session.query(Event).filter(
                Event.event_id == event_id, 
                Event.organizer_id == user_id
            ).first()
            
            if not event:
                print("Ошибка: Мероприятие не найдено или у вас нет прав доступа.")
                return False
                
            self.session.delete(event)
            self.session.commit()
            logging.info(f"Мероприятие ID {event_id} успешно удалено.")
            print("Мероприятие успешно удалено!")
            return True
            
        except SQLAlchemyError as e:
            logging.error(f"Ошибка при удалении мероприятия: {e}")
            self.session.rollback()
            print("Ошибка: Не удалось удалить мероприятие.")
            return False