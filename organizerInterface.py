from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from mydatabase import Event, User
import logging
from datetime import datetime
class OrganizerInterface:
    def __init__(self, session):
        """
        Инициализация интерфейса для работы организаторов.
        ООП: Инкапсуляция - объект содержит сессию базы данных и методы для работы организатора.

        Args:
            session: Сессия базы данных SQLAlchemy.
        """
        self.session = session

    def create_event(self, organizer_id: int, title: str, description: str, start_date, end_date, location: str):
        """
        Создание нового мероприятия организатором.
        ООП: Инкапсуляция - метод скрывает логику проверки и создания события.
        ООП: Полиморфизм - метод обрабатывает разные входные данные и работает с объектами базы данных.

        Args:
            organizer_id (int): ID пользователя-организатора.
            title (str): Название мероприятия.
            description (str): Описание мероприятия.
            start_date (datetime): Дата начала мероприятия.
            end_date (datetime): Дата окончания мероприятия.
            location (str): Место проведения мероприятия.

        Returns:
            bool: True, если мероприятие успешно создано, иначе False.
        """
        try:
            # Проверяем, является ли пользователь организатором.
            # ООП: Ассоциация - проверка роли пользователя через связь с базой данных.
            organizer = self.session.query(User).filter(User.user_id == organizer_id).first()
            if not organizer or organizer.role != 'organizer':
                logging.warning(f"Пользователь с ID {organizer_id} не является организатором.")
                print("Ошибка: Только организаторы могут создавать мероприятия.")
                return False

            # Создаем новое мероприятие.
            # ООП: Инкапсуляция - управление созданием объекта Event.
            new_event = Event(
                title=title,
                description=description,
                start_date= datetime.strptime(start_date , '%Y-%m-%d %H:%M:%S'),
                end_date= datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S'),
                location=location
            )
            self.session.add(new_event)
            self.session.commit()

            # ООП: Полиморфизм - обработка и логирование результата создания мероприятия.
            logging.info(f"Мероприятие '{title}' успешно создано организатором с ID {organizer_id}.")
            print("Мероприятие успешно создано!")
            return True

        except SQLAlchemyError as e:
            # ООП: Инкапсуляция - обработка ошибок внутри метода.
            logging.error(f"Ошибка при создании мероприятия: {e}")
            self.session.rollback()
            print("Ошибка: Не удалось создать мероприятие.")
            return False
