import os
import requests
import logging
from typing import Optional

def send_telegram_message(message: str) -> bool:
    """
    Отправляет сообщение в Telegram
    
    Args:
        message (str): Текст сообщения для отправки
    
    Returns:
        bool: True если сообщение отправлено успешно, False иначе
    """
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        logging.error("Ошибка: Переменные окружения TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не установлены")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('ok'):
                logging.info("Сообщение успешно отправлено в Telegram")
                return True
            else:
                logging.error(f"Ошибка от Telegram API: {response_data.get('description', 'Unknown error')}")
                return False
        else:
            logging.error(f"HTTP ошибка при отправке сообщения: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Сетевая ошибка при отправке сообщения в Telegram: {e}")
        return False
    except Exception as e:
        logging.error(f"Неожиданная ошибка при отправке сообщения: {e}")
        return False

def format_event_created_message(title: str, location: str, date: str, organizer: str) -> str:
    """
    Форматирует сообщение о создании нового мероприятия
    
    Args:
        title (str): Название мероприятия
        location (str): Место проведения
        date (str): Дата и время
        organizer (str): Организатор
    
    Returns:
        str: Отформатированное сообщение
    """
    message = f"""🎉 <b>Новое мероприятие создано!</b>

📝 <b>Название:</b> {title}
📍 <b>Место:</b> {location}
📅 <b>Дата:</b> {date}
👤 <b>Организатор:</b> {organizer}

Следите за новостями!"""
    return message

def format_ticket_purchased_message(event_title: str, price: float, buyer: str) -> str:
    """
    Форматирует сообщение о покупке билета
    
    Args:
        event_title (str): Название мероприятия
        price (float): Цена билета
        buyer (str): Покупатель
    
    Returns:
        str: Отформатированное сообщение
    """
    message = f"""🎟️ <b>Новый билет приобретен!</b>

🎪 <b>Мероприятие:</b> {event_title}
💰 <b>Цена:</b> {price} ₽
👤 <b>Покупатель:</b> {buyer}

Отличный выбор! Приятного мероприятия!"""
    return message