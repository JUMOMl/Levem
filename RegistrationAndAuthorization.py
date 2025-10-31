import logging
import bcrypt
import re
from sqlalchemy.orm import sessionmaker
from mydatabase import User, create_database

class RegistrationAndAuthorization:
    def __init__(self, database_url='sqlite:///main_database.db'):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("app.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.engine = create_database(database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.current_user_id = None
        
    def user_exists(self, username: str, email: str) -> bool:
        return self.session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).count() > 0
        
    def add_user(self) -> bool:
        user_name = input('Введите логин: ')
        password = input('Введите пароль: ')
        input_email = input('Введите почту: ')
        
        if self.user_exists(user_name, input_email):
            logging.warning(f'Пользователь с логином {user_name} или почтой уже существует.')
            print('Ошибка: Пользователь с таким логином или почтой уже существует.')
            return False
            
        if not self.check_password_strength(password):
            logging.warning('Пароль не соответствует требованиям.')
            print('Ошибка: Пароль должен содержать минимум 10 символов, 2 из которых должны быть заглавными, и минимум 3 буквы.')
            return False
            
        if not self.check_email_format(input_email):
            logging.warning('Некорректный формат электронной почты.')
            print('Ошибка: Некорректный формат почты.')
            return False
            
        new_user = User(
            username=user_name,
            password_hash=self.hash_password(password),
            email=input_email,
            role='User'
        )
        self.session.add(new_user)
        self.session.commit()
        logging.info(f'Пользователь {user_name} успешно зарегистрирован.')
        return True
        
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
        
    def check_password_strength(self, password: str) -> bool:
        if len(password) < 10:
            return False
        uppercase_count = sum(1 for char in password if char.isupper())
        if uppercase_count < 2:
            return False
        letter_count = sum(1 for char in password if char.isalpha())
        if letter_count < 3:
            return False
        return True
        
    def check_email_format(self, email: str) -> bool:
        email_pattern = r'^[a-zA-Z0-9.%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
        
    def login_account(self) -> bool:
        while True:
            username = input('Введите логин: ')
            password = input('Введите пароль: ')
            user = self.session.query(User).filter(User.username == username).first()
            
            if user is None:
                logging.warning(f'Попытка входа с несуществующим логином: {username}.')
                print('Ошибка: Пользователь с таким логином не найден.')
                if input('Хотите попробовать снова? (да/нет): ').lower() != 'да':
                    return False
                continue
                
            if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                logging.info(f'Пользователь {username} успешно вошел в систему.')
                print("Вы успешно вошли в систему.")
                self.current_user_id = user.user_id
                return True
            else:
                logging.warning(f'Неверный пароль для пользователя {username}.')
                print('Ошибка: Неверный пароль.')
                if input('Хотите попробовать снова? (да/нет): ').lower() != 'да':
                    return False
                    
    def registration_menu(self) -> bool:
        while True:
            print("\nМеню:")
            print("1. Регистрация пользователя")
            print("2. Вход в систему")
            print("3. Выход")
            choice = input("Выберите опцию (1-3): ")
            
            if choice == '1':
                if self.add_user():
                    print("Пользователь успешно зарегистрирован.")
                    return True
                else:
                    print("Не удалось зарегистрировать пользователя.")
                    return False
            elif choice == '2':
                if self.login_account():
                    return True
                else:
                    print("Не удалось войти в систему.")
                    return False
            elif choice == '3':
                print("Выход из программы.")
                break
            else:
                print("Некорректный выбор. Пожалуйста, выберите 1, 2 или 3.")