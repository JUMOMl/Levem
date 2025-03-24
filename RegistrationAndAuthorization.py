import logging
import bcrypt
import re
from sqlalchemy.orm import sessionmaker
from mydatabase import User, create_database
from mydatabase import Ticket, Event, User
class RegistrationAndAuthorization:
    def __init__(self, database_url='sqlite:///main_database.db'):
        """
        Инициализация класса для регистрации и авторизации пользователей.
        ООП: Инкапсуляция - объект содержит все функции, связанные с управлением пользователями.

        Args:
            database_url (str, optional): URL для подключения к базе данных. 
                                          По умолчанию 'sqlite:///main_database.db'.
        """             
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("app.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

        self.engine = create_database(database_url)  # Создание базы данных и таблиц
        self.Session = sessionmaker(bind=self.engine)  # ООП: Инкапсуляция - сессия управляет доступом к базе данных
        self.session = self.Session()  # Создаю новую сессию
        self.current_user_id = None

    def user_exists(self, username: str, email: str) -> bool:
        """
        Проверка существования пользователя по логину или электронной почте.
        ООП: Полиморфизм - метод работает с несколькими условиями поиска.

        Args:
            username (str): Логин пользователя.
            email (str): Электронная почта пользователя.

        Returns:
            bool: True, если пользователь существует, иначе False.
        """   
        return self.session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).count() > 0

    def add_user(self) -> bool:
        """
        Добавление нового пользователя.
        ООП: Инкапсуляция - метод скрывает логику регистрации.

        Returns:
            bool: True, если регистрация успешна, иначе False.
        """
        user_name = input('Введите логин: ')
        password = input('Введите пароль: ')
        input_email = input('Введите почту: ')

        # Проверяю, существует ли пользователь с таким логином или почтой
        if self.user_exists(user_name, input_email):
            logging.warning(f'Пользователь с логином {user_name} или почтой уже существует.')
            print('Ошибка: Пользователь с таким логином или почтой уже существует.')
            return False

        # Проверяю надежность пароля
        if not self.check_password_strength(password):
            logging.warning('Пароль не соответствует требованиям.')
            print('Ошибка: Пароль должен содержать минимум 10 символов, 2 из которых должны быть заглавными, и минимум 3 буквы.')
            return False

        # Проверяю корректность формата электронной почты
        if not self.check_email_format(input_email):
            logging.warning('Некорректный формат электронной почты.')
            print('Ошибка: Некорректный формат почты.')
            return False

        # Создаю нового пользователя и добавляю его в БД
        new_user = User(
            username=user_name,
            password_hash=self.hash_password(password),  # ООП: Инкапсуляция - скрытие процесса хеширования
            email=input_email,
            role='User'
        )
        self.session.add(new_user)
        self.session.commit()
        logging.info(f'Пользователь {user_name} успешно зарегистрирован.')
        return True

    def hash_password(self, password: str) -> str:
        """
        Хеширование пароля с использованием bcrypt.
        ООП: Инкапсуляция - метод скрывает процесс создания безопасного хеша пароля.

        Args:
            password (str): Пароль, который нужно хешировать.

        Returns:
            str: Хешированный пароль в виде строки.
        """      
        salt = bcrypt.gensalt()  # Генерирую соль для хеширования пароля.
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Хеширую пароль с солью.
        return hashed_password.decode('utf-8')  # Возвращаю хешированный пароль в виде строки.

    def check_password_strength(self, password: str) -> bool:
        """
        Проверка надежности пароля.
        ООП: Полиморфизм - метод проверяет несколько условий с разными критериями.

        Args:
            password (str): Пароль для проверки.

        Returns:
            bool: True, если пароль соответствует требованиям, иначе False.
        """  
        if len(password) < 10:  # Проверяю длину пароля.
            return False
        
        uppercase_count = sum(1 for char in password if char.isupper())  # Считаю количество заглавных букв.
        if uppercase_count < 2:
            return False
        
        letter_count = sum(1 for char in password if char.isalpha())  # Считаю количество букв в пароле.
        if letter_count < 3:
            return False
        
        return True

    def check_email_format(self, email: str) -> bool:
        """
        Проверка корректности формата электронной почты.
        ООП: Полиморфизм - использование регулярного выражения для проверки разных форматов.

        Args:
            email (str): Электронная почта для проверки.

        Returns:
            bool: True, если формат почты корректен, иначе False.
        """      
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # Регулярное выражение для проверки формата почты.
        return re.match(email_pattern, email) is not None

    def login_account(self) -> bool:
        """
        Вход в систему для зарегистрированного пользователя.
        ООП: Инкапсуляция - метод скрывает детали авторизации пользователя.

        Returns:
            bool: True, если вход успешен, иначе False.
        """       
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
                self.current_user_id = user.user_id  # Сохраняем ID текущего пользователя.
                return True
            else:
                logging.warning(f'Неверный пароль для пользователя {username}.')
                print('Ошибка: Неверный пароль.')
                if input('Хотите попробовать снова? (да/нет): ').lower() != 'да':
                    return False
    def registration_menu(self) -> bool:
        """
        Меню для регистрации и входа в систему.
        ООП: Инкапсуляция - метод предоставляет единый интерфейс для работы с регистрацией и авторизацией.

        Returns:
            bool: True, если пользователь успешно зарегистрирован или вошел в систему, иначе False.
        """       
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