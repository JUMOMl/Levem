from organizerInterface import OrganizerInterface
from TicketPurchaseInterface import TicketPurchaseInterface
from RegistrationAndAuthorization import RegistrationAndAuthorization

app = RegistrationAndAuthorization()
org_app = OrganizerInterface(app.session)  
buy_app = TicketPurchaseInterface(app.session) 

if __name__ == "__main__":
    if app.registration_menu():  
        print("1 - создать, 2 - купить")
        choice = input("выберите опцию (1-2): ")
        if choice == '1':
            org_app.create_event(
                app.current_user_id,
                input("Введите название мероприятия: "),
                input("Введите описание мероприятия: "),
                input("Введите дату мероприятия: "),
                input("Введите дату окончания: "),
                input("Введите место проведения: ")
            )
        elif choice == '2':
            buy_app.purchase_ticket(
                app.current_user_id,
                int(input("Введите ID мероприятия: ")),
                int(input("Введите цену билета: "))
            )

