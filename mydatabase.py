from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import func

# Создание базового класса для декларативного объявления
Base = declarative_base()

# Основная база данных
class User(Base):
    __tablename__ = 'users'
    
    # ООП: Инкапсуляция - свойства объекта (поля таблицы) определены внутри класса
    user_id = Column(Integer, primary_key=True, autoincrement=True)  # ООП: Идентификация - уникальный ключ определяет объект
    username = Column(String(50), nullable=False, unique=True)  # ООП: Инкапсуляция - поле для хранения имени пользователя
    password_hash = Column(String(255), nullable=False)  # ООП: Инкапсуляция - защищенные данные (пароли)
    email = Column(String(100), nullable=False, unique=True)  # ООП: Инкапсуляция - уникальный идентификатор для пользователя
    created_at = Column(DateTime, server_default=func.now())  # ООП: Полиморфизм - использование SQLAlchemy для автоматизации
    role = Column(String(50), default='User')  # ООП: Наследование - базовая роль задается по умолчанию

class Event(Base):
    __tablename__ = 'events'
    
    # ООП: Инкапсуляция - класс хранит данные, связанные с событиями
    event_id = Column(Integer, primary_key=True, autoincrement=True)  # ООП: Идентификация - уникальный идентификатор события
    title = Column(String(100), nullable=False)  # ООП: Инкапсуляция - название события
    description = Column(Text)  # ООП: Инкапсуляция - текстовое описание
    start_date = Column(DateTime)  # ООП: Полиморфизм - универсальная обработка типов времени
    end_date = Column(DateTime)
    location = Column(String(100))  # ООП: Инкапсуляция - атрибут местоположения события

class Ticket(Base):
    __tablename__ = 'tickets'
    
    # ООП: Ассоциация - связь между пользователями и событиями через ForeignKey
    ticket_id = Column(Integer, primary_key=True, autoincrement=True)  # ООП: Идентификация - уникальный идентификатор билета
    user_id = Column(Integer, ForeignKey('users.user_id'))  # ООП: Ассоциация - связь с пользователем
    event_id = Column(Integer, ForeignKey('events.event_id'))  # ООП: Ассоциация - связь с событием
    purchase_date = Column(DateTime, server_default=func.now())  # ООП: Полиморфизм - автоматизация дат
    price = Column(DECIMAL(10, 2))  # ООП: Инкапсуляция - хранение цены билета

class Profile(Base):
    __tablename__ = 'profiles'
    
    # ООП: Инкапсуляция - данные профиля связаны с пользователем
    profile_id = Column(Integer, primary_key=True, autoincrement=True)  # ООП: Идентификация - уникальный идентификатор профиля
    user_id = Column(Integer, ForeignKey('users.user_id'))  # ООП: Ассоциация - связь с пользователем
    interests = Column(Text)  # ООП: Инкапсуляция - интересы пользователя
    age = Column(Integer)  # ООП: Инкапсуляция - возраст пользователя
    history = Column(Text)  # ООП: Инкапсуляция - хранение истории взаимодействий

class ContactInfo(Base):
    __tablename__ = 'contact_info'
    
    # ООП: Инкапсуляция - контактная информация пользователя
    contact_id = Column(Integer, primary_key=True, autoincrement=True)  # ООП: Идентификация - уникальный идентификатор контакта
    user_id = Column(Integer, ForeignKey('users.user_id'))  # ООП: Ассоциация - связь с пользователем
    contact_type = Column(String(50))  # ООП: Инкапсуляция - тип контакта (телефон, email и т. д.)
    value = Column(String(150))  # ООП: Инкапсуляция - значение контакта (номер телефона или адрес)

# База данных для геймификации
class XP(Base):
    __tablename__ = 'xp'
    
    # ООП: Инкапсуляция - управление данными опыта пользователя
    xp_id = Column(Integer, primary_key=True, autoincrement=True)  # ООП: Идентификация - уникальный идентификатор
    user_id = Column(Integer, ForeignKey('users.user_id'))  # ООП: Ассоциация - связь опыта с пользователем
    points = Column(Integer)  # ООП: Инкапсуляция - количество баллов опыта
    reason = Column(String(255))  # ООП: Инкапсуляция - причина начисления баллов
    date = Column(DateTime, server_default=func.now())  # ООП: Полиморфизм - автоматизация даты начисления

class Level(Base):
    __tablename__ = 'levels'
    
    # ООП: Инкапсуляция - управление уровнями пользователей
    level_id = Column(Integer, primary_key=True, autoincrement=True)  # ООП: Идентификация - уникальный идентификатор уровня
    level_name = Column(String(50))  # ООП: Инкапсуляция - название уровня
    min_xp = Column(Integer)  # ООП: Инкапсуляция - минимальный опыт для уровня
    max_xp = Column(Integer)  # ООП: Инкапсуляция - максимальный опыт для уровня

class Badge(Base):
    __tablename__ = 'badges'
    
    # ООП: Инкапсуляция - хранение данных о значках
    badge_id = Column(Integer, primary_key=True, autoincrement=True)  # ООП: Идентификация - уникальный идентификатор значка
    badge_name = Column(String(50))  # ООП: Инкапсуляция - название значка
    description = Column(Text)  # ООП: Инкапсуляция - описание значка
    criteria = Column(String(255))  # ООП: Инкапсуляция - условия получения значка

class UserBadge(Base):
    __tablename__ = 'user_badges'
    
    # ООП: Ассоциация - связь между пользователем и значком
    user_badge_id = Column(Integer, primary_key=True, autoincrement=True)  # ООП: Идентификация - уникальный идентификатор
    user_id = Column(Integer, ForeignKey('users.user_id'))  # ООП: Ассоциация - связь с пользователем
    badge_id = Column(Integer, ForeignKey('badges.badge_id'))  # ООП: Ассоциация - связь со значком
    date_awarded = Column(DateTime, server_default=func.now())  # ООП: Полиморфизм - автоматизация даты награждения

# Создание базы данных и таблиц
def create_database(db_url):
    # ООП: Полиморфизм - единый подход к созданию базы данных независимо от URL
    engine = create_engine(db_url)  # Создание движка базы данных
    Base.metadata.create_all(engine)  # Создание всех таблиц из моделей
    return engine
