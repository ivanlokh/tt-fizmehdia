"""
Менеджер для роботи з Arduino пристроями
"""

import serial
import serial.tools.list_ports
import time
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ArduinoDevice:
    """Клас для представлення Arduino пристрою"""
    port: str
    baudrate: int
    connection: Optional[serial.Serial] = None
    last_seen: Optional[float] = None
    status: str = 'disconnected'

class ArduinoManager:
    """Менеджер для роботи з Arduino пристроями"""
    
    def __init__(self, default_baudrate: int = 9600, timeout: int = 5):
        self.default_baudrate = default_baudrate
        self.timeout = timeout
        self.connected_devices: Dict[str, ArduinoDevice] = {}
        self.retry_count = 3
        
    def get_available_ports(self) -> List[Dict[str, str]]:
        """Отримання списку доступних портів"""
        ports = []
        for port in serial.tools.list_ports.comports():
            port_info = {
                'device': port.device,
                'description': port.description,
                'hwid': port.hwid,
                'manufacturer': port.manufacturer,
                'product': port.product,
                'serial_number': port.serial_number
            }
            ports.append(port_info)
        
        logger.info(f"Знайдено {len(ports)} доступних портів")
        return ports
    
    def connect(self, port: str, baudrate: Optional[int] = None) -> bool:
        """Підключення до Arduino"""
        if baudrate is None:
            baudrate = self.default_baudrate
        
        try:
            # Закриття існуючого з'єднання якщо є
            if port in self.connected_devices:
                self.disconnect(port)
            
            # Створення нового з'єднання
            connection = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=self.timeout,
                write_timeout=self.timeout
            )
            
            # Очікування ініціалізації Arduino
            time.sleep(2)
            
            # Тестування з'єднання
            if self._test_connection(connection):
                device = ArduinoDevice(
                    port=port,
                    baudrate=baudrate,
                    connection=connection,
                    last_seen=time.time(),
                    status='connected'
                )
                self.connected_devices[port] = device
                logger.info(f"Підключено до Arduino на порту {port}")
                return True
            else:
                connection.close()
                logger.error(f"Не вдалося підключитися до Arduino на порту {port}")
                return False
                
        except Exception as e:
            logger.error(f"Помилка підключення до Arduino: {e}")
            return False
    
    def disconnect(self, port: str) -> bool:
        """Відключення від Arduino"""
        try:
            if port in self.connected_devices:
                device = self.connected_devices[port]
                if device.connection and device.connection.is_open:
                    device.connection.close()
                del self.connected_devices[port]
                logger.info(f"Відключено від Arduino на порту {port}")
                return True
            return False
        except Exception as e:
            logger.error(f"Помилка відключення: {e}")
            return False
    
    def disconnect_all(self):
        """Відключення від всіх пристроїв"""
        for port in list(self.connected_devices.keys()):
            self.disconnect(port)
    
    def is_connected(self, port: Optional[str] = None) -> bool:
        """Перевірка підключення"""
        if port:
            return port in self.connected_devices and self.connected_devices[port].status == 'connected'
        return len(self.connected_devices) > 0
    
    def send_command(self, command: str, port: Optional[str] = None) -> Optional[str]:
        """Відправка команди до Arduino"""
        try:
            # Якщо порт не вказано, використовуємо перший підключений
            if port is None:
                if not self.connected_devices:
                    logger.error("Немає підключених пристроїв")
                    return None
                port = list(self.connected_devices.keys())[0]
            
            if port not in self.connected_devices:
                logger.error(f"Пристрій на порту {port} не підключений")
                return None
            
            device = self.connected_devices[port]
            if not device.connection or not device.connection.is_open:
                logger.error(f"З'єднання з портом {port} не активне")
                return None
            
            # Відправка команди
            command_bytes = f"{command}\n".encode('utf-8')
            device.connection.write(command_bytes)
            device.connection.flush()
            
            # Очікування відповіді
            response = device.connection.readline().decode('utf-8').strip()
            
            # Оновлення часу останнього звернення
            device.last_seen = time.time()
            
            logger.info(f"Команда '{command}' відправлена до {port}, відповідь: '{response}'")
            return response
            
        except Exception as e:
            logger.error(f"Помилка відправки команди: {e}")
            return None
    
    def send_gift_command(self, gift_type: str, port: Optional[str] = None) -> Optional[str]:
        """Відправка команди для подарунка"""
        command = f"GIFT:{gift_type}"
        return self.send_command(command, port)
    
    def send_led_command(self, action: str, params: Dict[str, Any], port: Optional[str] = None) -> Optional[str]:
        """Відправка команди для LED"""
        if action == 'set_color':
            color = params.get('color', '#ffffff')
            brightness = params.get('brightness', 50)
            duration = params.get('duration', 3000)
            command = f"LED:COLOR:{color}:{brightness}:{duration}"
        elif action == 'rainbow':
            duration = params.get('duration', 5000)
            command = f"LED:RAINBOW:{duration}"
        elif action == 'clear':
            command = "LED:CLEAR"
        else:
            logger.error(f"Невідома LED дія: {action}")
            return None
        
        return self.send_command(command, port)
    
    def send_servo_command(self, servo_num: int, angle: int, port: Optional[str] = None) -> Optional[str]:
        """Відправка команди для сервоприводу"""
        command = f"SERVO:{servo_num}:{angle}"
        return self.send_command(command, port)
    
    def send_sound_command(self, sound_type: str, duration: int = 1000, port: Optional[str] = None) -> Optional[str]:
        """Відправка команди для звуку"""
        command = f"SOUND:{sound_type}:{duration}"
        return self.send_command(command, port)
    
    def send_display_command(self, text: str, duration: int = 5000, port: Optional[str] = None) -> Optional[str]:
        """Відправка команди для дисплею"""
        command = f"DISPLAY:{text}:{duration}"
        return self.send_command(command, port)
    
    def get_device_status(self, port: str) -> Optional[Dict[str, Any]]:
        """Отримання статусу пристрою"""
        if port not in self.connected_devices:
            return None
        
        device = self.connected_devices[port]
        return {
            'port': device.port,
            'baudrate': device.baudrate,
            'status': device.status,
            'last_seen': device.last_seen,
            'connected': device.connection and device.connection.is_open
        }
    
    def get_all_devices_status(self) -> Dict[str, Dict[str, Any]]:
        """Отримання статусу всіх пристроїв"""
        status = {}
        for port, device in self.connected_devices.items():
            status[port] = self.get_device_status(port)
        return status
    
    def _test_connection(self, connection: serial.Serial) -> bool:
        """Тестування з'єднання з Arduino"""
        try:
            # Відправка тестової команди
            connection.write(b"TEST\n")
            connection.flush()
            
            # Очікування відповіді
            response = connection.readline().decode('utf-8').strip()
            
            # Arduino повинен відповісти "OK" або "READY"
            return response.upper() in ['OK', 'READY', 'ARDUINO READY']
            
        except Exception as e:
            logger.error(f"Помилка тестування з'єднання: {e}")
            return False
    
    def heartbeat_check(self):
        """Перевірка heartbeat всіх пристроїв"""
        current_time = time.time()
        for port, device in list(self.connected_devices.items()):
            try:
                # Відправка heartbeat команди
                response = self.send_command("HEARTBEAT", port)
                if response:
                    device.last_seen = current_time
                    device.status = 'connected'
                else:
                    device.status = 'error'
                    logger.warning(f"Heartbeat не пройшов для {port}")
            except Exception as e:
                logger.error(f"Помилка heartbeat для {port}: {e}")
                device.status = 'error'
    
    def __del__(self):
        """Деструктор - закриття всіх з'єднань"""
        self.disconnect_all()
