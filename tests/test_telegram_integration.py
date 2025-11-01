import os
import sys
import logging
from sqlalchemy.orm import sessionmaker
from mydatabase import engine, User, Event, Ticket
from organizerInterface import OrganizerInterface
from TicketPurchaseInterface import TicketPurchaseInterface

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_telegram_integration():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print("=== Тестирование интеграции с Telegram ===\n")
        
        print("1. Создание тестового пользователя...")
        test_user = User(username="test_organizer", email="test@example.com")
        test_user.set_password("password123")
        session.add(test_user)
        session.commit()
        print(f"Пользователь создан с ID: {test_user.user_id}")
        
        print("\n2. Тестирование создания мероприятия...")
        org_interface = OrganizerInterface(session)
        
        success = org_interface.create_event(
            organizer_id=test_user.user_id,
            title="Тестовое мероприятие с Telegram",
            description="Мероприятие для тестирования интеграции с Telegram ботом",
            start_date="2025-12-25 10:00:00",
            end_date="2025-12-25 18:00:00",
            location="Тестовый зал, Москва"
        )
        
        if success:
            print("✅ Мероприятие создано успешно!")
        else:
            print("❌ Ошибка при создании мероприятия")
            return False
            
        print("\n3. Тестирование покупки билета...")
        
        buyer = User(username="test_buyer", email="buyer@example.com")
        buyer.set_password("password123")
        session.add(buyer)
        session.commit()
        print(f"Покупатель создан с ID: {buyer.user_id}")
        
        buy_interface = TicketPurchaseInterface(session)
        event = session.query(Event).first()
        
        if event:
            success = buy_interface.purchase_ticket(
                user_id=buyer.user_id,
                event_id=event.event_id,
                price=500.0
            )
            
            if success:
                print("✅ Билет приобретен успешно!")
            else:
                print("❌ Ошибка при покупке билета")
                return False
        else:
            print("❌ Нет доступных мероприятий для покупки билета")
            return False
            
        print("\n4. Очистка тестовых данных...")
        session.query(Ticket).filter(Ticket.user_id.in_([test_user.user_id, buyer.user_id])).delete()
        session.query(Event).filter(Event.organizer_id == test_user.user_id).delete()
        session.query(User).filter(User.user_id.in_([test_user.user_id, buyer.user_id])).delete()
        session.commit()
        print("Тестовые данные удалены")
        
        print("\n=== Тестирование завершено успешно! ===")
        return True
        
    except Exception as e:
        logging.error(f"Ошибка при тестировании: {e}")
        print(f"❌ Ошибка при тестировании: {e}")
        return False
        
    finally:
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    print("Внимание: Для работы тестирования необходимо настроить переменные окружения:")
    print("- TELEGRAM_BOT_TOKEN")
    print("- TELEGRAM_CHAT_ID")
    print("\nПроверьте файл .env.example для примера конфигурации.")
    print("\n" + "="*60 + "\n")
    
    test_telegram_integration()