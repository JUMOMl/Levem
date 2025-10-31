from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    role = Column(String(50), default='User')

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    organizer_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    location = Column(String(100))

class Ticket(Base):
    __tablename__ = 'tickets'
    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    event_id = Column(Integer, ForeignKey('events.event_id'))
    purchase_date = Column(DateTime, server_default=func.now())
    price = Column(DECIMAL(10, 2))

class Profile(Base):
    __tablename__ = 'profiles'
    profile_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    interests = Column(Text)
    age = Column(Integer)
    history = Column(Text)

class ContactInfo(Base):
    __tablename__ = 'contact_info'
    contact_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    contact_type = Column(String(50))
    value = Column(String(150))

class XP(Base):
    __tablename__ = 'xp'
    xp_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    points = Column(Integer)
    reason = String(255)
    date = Column(DateTime, server_default=func.now())

class Level(Base):
    __tablename__ = 'levels'
    level_id = Column(Integer, primary_key=True, autoincrement=True)
    level_name = Column(String(50))
    min_xp = Column(Integer)
    max_xp = Column(Integer)

class Badge(Base):
    __tablename__ = 'badges'
    badge_id = Column(Integer, primary_key=True, autoincrement=True)
    badge_name = Column(String(50))
    description = Column(Text)
    criteria = Column(String(255))

class UserBadge(Base):
    __tablename__ = 'user_badges'
    user_badge_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    badge_id = Column(Integer, ForeignKey('badges.badge_id'))
    date_awarded = Column(DateTime, server_default=func.now())

def create_database(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine