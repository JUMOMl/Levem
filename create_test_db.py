
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mydatabase import create_database, User, Event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

def init_database():
    try:
        DATABASE_URL = 'sqlite:///test_levem.db'
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        from mydatabase import Base
        Base.metadata.create_all(engine)
        
        test_user = User(
            username='test_organizer',
            password_hash='hash_placeholder',
            email='test@example.com',
            role='Organizer'
        )
        session.add(test_user)
        session.commit()
        print(f"Создан тестовый пользователь с ID: {test_user.user_id}")
        
        test_event = Event(
            organizer_id=test_user.user_id,
            title='Тестовое мероприятие',
            description='Описание тестового мероприятия',
            start_date=datetime.strptime('2024-12-01 10:00:00', '%Y-%m-%d %H:%M:%S'),
            end_date=datetime.strptime('2024-12-01 18:00:00', '%Y-%m-%d %H:%M:%S'),
            location='Москва, Тестовая улица, 1'
        )
        session.add(test_event)
        session.commit()
        print(f"Создано тестовое мероприятие с ID: {test_event.event_id}")
        
        session.close()
        print("База данных создана успешно!")
        
        with open('api.py', 'r') as f:
            content = f.read()
        
        content = content.replace('sqlite:///main_database.db', 'sqlite:///test_levem.db')
        
        with open('api.py', 'w') as f:
            f.write(content)
            
        print("API настроен для использования тестовой БД")
        
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_database()