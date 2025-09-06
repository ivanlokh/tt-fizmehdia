"""
Конфігурація системи TT-FizMehdia
"""

import os
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Config:
    """Основна конфігурація системи"""
    
    # Налаштування сервера
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', 5000))
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Налаштування Arduino
    ARDUINO_BAUDRATE: int = int(os.getenv('ARDUINO_BAUDRATE', 9600))
    ARDUINO_TIMEOUT: int = int(os.getenv('ARDUINO_TIMEOUT', 5))
    ARDUINO_RETRY_COUNT: int = int(os.getenv('ARDUINO_RETRY_COUNT', 3))
    
    # Налаштування TikTok
    TIKTOK_MONITORING_INTERVAL: int = int(os.getenv('TIKTOK_MONITORING_INTERVAL', 2))
    TIKTOK_TIMEOUT: int = int(os.getenv('TIKTOK_TIMEOUT', 30))
    
    # Налаштування пристроїв
    DEVICE_HEARTBEAT_INTERVAL: int = int(os.getenv('DEVICE_HEARTBEAT_INTERVAL', 30))
    MAX_DEVICES: int = int(os.getenv('MAX_DEVICES', 10))
    
    # Типи подарунків TikTok та їх вартість
    GIFT_VALUES: Dict[str, int] = {
        'ROSE': 1,
        'HEART': 5,
        'STAR': 10,
        'CROWN': 50,
        'DIAMOND': 100,
        'ROCKET': 200,
        'UNICORN': 500
    }
    
    # Кольори подарунків
    GIFT_COLORS: Dict[str, str] = {
        'ROSE': '#ff69b4',
        'HEART': '#ff0000',
        'STAR': '#ffd700',
        'CROWN': '#ff8c00',
        'DIAMOND': '#00bfff',
        'ROCKET': '#ff4500',
        'UNICORN': '#9370db'
    }
    
    # Назви подарунків
    GIFT_NAMES: Dict[str, str] = {
        'ROSE': 'Роза',
        'HEART': 'Серце',
        'STAR': 'Зірка',
        'CROWN': 'Корона',
        'DIAMOND': 'Діамант',
        'ROCKET': 'Ракета',
        'UNICORN': 'Єдиноріг'
    }
    
    # Типи пристроїв
    DEVICE_TYPES: List[str] = [
        'arduino',
        'esp32',
        'esp8266',
        'raspberry_pi',
        'light',
        'sound',
        'motor',
        'display',
        'camera',
        'gpio',
        'neopixel',
        'servo',
        'buzzer',
        'pir_sensor',
        'custom'
    ]
    
    # Дії пристроїв
    DEVICE_ACTIONS: List[str] = [
        'turn_on',
        'turn_off',
        'toggle',
        'set_color',
        'set_brightness',
        'set_volume',
        'play_sound',
        'move',
        'rotate',
        'show_text',
        'take_photo',
        'servo_move',
        'led_rainbow',
        'led_clear',
        'motor_start',
        'motor_stop',
        'buzzer_beep',
        'display_message',
        'gift_effect',
        # Raspberry Pi специфічні дії
        'gpio_control',
        'neopixel_effect',
        'camera_capture',
        'sound_play',
        'pir_detect',
        'pulse_effect',
        'twinkle_effect',
        'chase_effect',
        'unicorn_effect',
        'custom'
    ]
    
    # Налаштування логування
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'logs/app.log')
    LOG_MAX_SIZE: int = int(os.getenv('LOG_MAX_SIZE', 10485760))  # 10MB
    LOG_BACKUP_COUNT: int = int(os.getenv('LOG_BACKUP_COUNT', 5))
    
    # Налаштування безпеки
    RATE_LIMIT_REQUESTS: int = int(os.getenv('RATE_LIMIT_REQUESTS', 100))
    RATE_LIMIT_WINDOW: int = int(os.getenv('RATE_LIMIT_WINDOW', 900))  # 15 хвилин
    
    # Налаштування бази даних (якщо потрібно)
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///tt_fizmehdia.db')
    
    # Налаштування веб-скрапінгу
    SELENIUM_HEADLESS: bool = os.getenv('SELENIUM_HEADLESS', 'True').lower() == 'true'
    SELENIUM_TIMEOUT: int = int(os.getenv('SELENIUM_TIMEOUT', 30))
    
    # Налаштування MQTT (якщо потрібно)
    MQTT_BROKER: str = os.getenv('MQTT_BROKER', 'localhost')
    MQTT_PORT: int = int(os.getenv('MQTT_PORT', 1883))
    MQTT_USERNAME: str = os.getenv('MQTT_USERNAME', '')
    MQTT_PASSWORD: str = os.getenv('MQTT_PASSWORD', '')
    
    def get_gift_info(self, gift_type: str) -> Dict[str, any]:
        """Отримання інформації про подарунок"""
        return {
            'type': gift_type,
            'name': self.GIFT_NAMES.get(gift_type, gift_type),
            'value': self.GIFT_VALUES.get(gift_type, 1),
            'color': self.GIFT_COLORS.get(gift_type, '#ffffff')
        }
    
    def is_valid_device_type(self, device_type: str) -> bool:
        """Перевірка валідності типу пристрою"""
        return device_type in self.DEVICE_TYPES
    
    def is_valid_action(self, action: str) -> bool:
        """Перевірка валідності дії"""
        return action in self.DEVICE_ACTIONS
    
    def get_default_gift_action(self, gift_type: str) -> Dict[str, any]:
        """Отримання дії за замовчуванням для подарунка"""
        gift_info = self.get_gift_info(gift_type)
        
        # Прості дії за замовчуванням
        if gift_type == 'ROSE':
            return {
                'action': 'set_color',
                'params': {
                    'color': gift_info['color'],
                    'brightness': 30,
                    'duration': 2000
                }
            }
        elif gift_type == 'HEART':
            return {
                'action': 'led_rainbow',
                'params': {
                    'duration': 3000
                }
            }
        elif gift_type == 'DIAMOND':
            return {
                'action': 'set_color',
                'params': {
                    'color': gift_info['color'],
                    'brightness': 100,
                    'duration': 5000
                }
            }
        else:
            return {
                'action': 'set_color',
                'params': {
                    'color': gift_info['color'],
                    'brightness': 50,
                    'duration': 3000
                }
            }
