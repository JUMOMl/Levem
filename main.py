from organizerInterface import OrganizerInterface
from TicketPurchaseInterface import TicketPurchaseInterface
from RegistrationAndAuthorization import RegistrationAndAuthorization

def main():
    app = RegistrationAndAuthorization()
    
    if not app.registration_menu():
        return
        
    org_app = OrganizerInterface(app.session)
    buy_app = TicketPurchaseInterface(app.session)
    
    while True:
        print(f"\nДобро пожаловать, пользователь ID: {app.current_user_id}")
        print("1 - создать мероприятие")
        print("2 - купить билет")
        print("3 - мои мероприятия")
        print("4 - мои билеты")
        print("5 - выход")
        
        choice = input("выберите опцию (1-5): ")
        
        if choice == '1':
            title = input("Введите название мероприятия: ")
            description = input("Введите описание мероприятия: ")
            start_date = input("Введите дату мероприятия (YYYY-MM-DD HH:MM:SS): ")
            end_date = input("Введите дату окончания (YYYY-MM-DD HH:MM:SS): ")
            location = input("Введите место проведения: ")
            
            org_app.create_event(
                app.current_user_id,
                title,
                description,
                start_date,
                end_date,
                location
            )
            
        elif choice == '2':
            buy_app.view_available_events()
            try:
                event_id = int(input("Введите ID мероприятия: "))
                price = float(input("Введите цену билета: "))
                
                buy_app.purchase_ticket(
                    app.current_user_id,
                    event_id,
                    price
                )
            except ValueError:
                print("Ошибка: Неверный формат данных.")
                
        elif choice == '3':
            org_app.view_my_events(app.current_user_id)
            
        elif choice == '4':
            buy_app.view_my_tickets(app.current_user_id)
            
        elif choice == '5':
            print("Выход из системы.")
            break
            
        else:
            print("Некорректный выбор. Пожалуйста, выберите 1-5.")

if __name__ == "__main__":
    main()