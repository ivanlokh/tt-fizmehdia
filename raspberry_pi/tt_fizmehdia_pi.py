#!/usr/bin/env python3
"""
TT-FizMehdia Raspberry Pi Controller
Контролер для Raspberry Pi з підтримкою GPIO, камери, звуку та мережі
"""

import os
import sys
import time
import json
import logging
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any

# Flask для веб-сервера
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# GPIO для Raspberry Pi
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("GPIO не доступний. Встановіть RPi.GPIO для роботи з Raspberry Pi")

# Камера
try:
    from picamera import PiCamera
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False
    print("PiCamera не доступний. Встановіть picamera для роботи з камерою")

# Звук
try:
    import pygame
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False
    print("Pygame не доступний. Встановіть pygame для роботи зі звуком")

# LED стрічки
try:
    import neopixel
    import board
    NEOPIXEL_AVAILABLE = True
except ImportError:
    NEOPIXEL_AVAILABLE = False
    print("Neopixel не доступний. Встановіть neopixel для роботи з LED стрічками")

# MQTT для мережевого керування
try:
    import paho.mqtt.client as mqtt
    MQTT_AVAILABLE = True
except ImportError:
    MQTT_AVAILABLE = False
    print("MQTT не доступний. Встановіть paho-mqtt для мережевого керування")

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TTFizMehdiaPi:
    """Головний клас контролера Raspberry Pi"""
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Налаштування GPIO
        self.gpio_pins = {
            'led': 18,
            'servo': 12,
            'buzzer': 13,
            'button': 16,
            'motion_sensor': 17
        }
        
        # Налаштування LED стрічки
        self.led_strip = None
        self.led_count = 60
        self.led_brightness = 0.5
        
        # Налаштування камери
        self.camera = None
        self.camera_resolution = (640, 480)
        
        # Налаштування звуку
        self.sound_files = {
            'rose': 'sounds/rose.wav',
            'heart': 'sounds/heart.wav',
            'star': 'sounds/star.wav',
            'crown': 'sounds/crown.wav',
            'diamond': 'sounds/diamond.wav',
            'rocket': 'sounds/rocket.wav',
            'unicorn': 'sounds/unicorn.wav'
        }
        
        # Статус системи
        self.status = {
            'gpio_available': GPIO_AVAILABLE,
            'camera_available': CAMERA_AVAILABLE,
            'sound_available': SOUND_AVAILABLE,
            'neopixel_available': NEOPIXEL_AVAILABLE,
            'mqtt_available': MQTT_AVAILABLE,
            'connected': False,
            'last_gift': None,
            'gift_count': 0
        }
        
        # Ініціалізація компонентів
        self.init_gpio()
        self.init_led_strip()
        self.init_camera()
        self.init_mqtt()
        self.setup_routes()
        
        logger.info("TT-FizMehdia Raspberry Pi Controller ініціалізовано")
    
    def init_gpio(self):
        """Ініціалізація GPIO"""
        if not GPIO_AVAILABLE:
            return
        
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            # Налаштування пінів
            GPIO.setup(self.gpio_pins['led'], GPIO.OUT)
            GPIO.setup(self.gpio_pins['buzzer'], GPIO.OUT)
            GPIO.setup(self.gpio_pins['button'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.gpio_pins['motion_sensor'], GPIO.IN)
            
            # PWM для сервоприводу
            GPIO.setup(self.gpio_pins['servo'], GPIO.OUT)
            self.servo_pwm = GPIO.PWM(self.gpio_pins['servo'], 50)
            self.servo_pwm.start(0)
            
            logger.info("GPIO ініціалізовано успішно")
            
        except Exception as e:
            logger.error(f"Помилка ініціалізації GPIO: {e}")
    
    def init_led_strip(self):
        """Ініціалізація LED стрічки"""
        if not NEOPIXEL_AVAILABLE:
            return
        
        try:
            self.led_strip = neopixel.NeoPixel(
                board.D18,  # GPIO пін
                self.led_count,
                brightness=self.led_brightness,
                auto_write=False
            )
            logger.info("LED стрічка ініціалізована успішно")
            
        except Exception as e:
            logger.error(f"Помилка ініціалізації LED стрічки: {e}")
    
    def init_camera(self):
        """Ініціалізація камери"""
        if not CAMERA_AVAILABLE:
            return
        
        try:
            self.camera = PiCamera()
            self.camera.resolution = self.camera_resolution
            self.camera.framerate = 30
            logger.info("Камера ініціалізована успішно")
            
        except Exception as e:
            logger.error(f"Помилка ініціалізації камери: {e}")
    
    def init_mqtt(self):
        """Ініціалізація MQTT"""
        if not MQTT_AVAILABLE:
            return
        
        try:
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.on_connect = self.on_mqtt_connect
            self.mqtt_client.on_message = self.on_mqtt_message
            
            # Підключення до брокера (якщо потрібно)
            # self.mqtt_client.connect("localhost", 1883, 60)
            # self.mqtt_client.loop_start()
            
            logger.info("MQTT ініціалізовано успішно")
            
        except Exception as e:
            logger.error(f"Помилка ініціалізації MQTT: {e}")
    
    def setup_routes(self):
        """Налаштування маршрутів Flask"""
        
        @self.app.route('/')
        def index():
            return render_template('pi_controller.html')
        
        @self.app.route('/api/status')
        def get_status():
            return jsonify(self.status)
        
        @self.app.route('/api/gift', methods=['POST'])
        def handle_gift():
            data = request.get_json()
            gift_type = data.get('type', 'ROSE')
            sender = data.get('sender', 'Unknown')
            
            result = self.process_gift(gift_type, sender)
            return jsonify(result)
        
        @self.app.route('/api/led', methods=['POST'])
        def control_led():
            data = request.get_json()
            action = data.get('action')
            params = data.get('params', {})
            
            result = self.control_led_strip(action, params)
            return jsonify(result)
        
        @self.app.route('/api/servo', methods=['POST'])
        def control_servo():
            data = request.get_json()
            angle = data.get('angle', 90)
            
            result = self.control_servo_motor(angle)
            return jsonify(result)
        
        @self.app.route('/api/sound', methods=['POST'])
        def play_sound():
            data = request.get_json()
            sound_type = data.get('type', 'beep')
            
            result = self.play_sound_effect(sound_type)
            return jsonify(result)
        
        @self.app.route('/api/camera', methods=['POST'])
        def take_photo():
            data = request.get_json()
            filename = data.get('filename', f'gift_photo_{int(time.time())}.jpg')
            
            result = self.take_photo(filename)
            return jsonify(result)
        
        @self.app.route('/api/test', methods=['POST'])
        def test_components():
            result = self.test_all_components()
            return jsonify(result)
    
    def process_gift(self, gift_type: str, sender: str) -> Dict[str, Any]:
        """Обробка подарунка"""
        logger.info(f"Отримано подарунок {gift_type} від {sender}")
        
        # Оновлення статусу
        self.status['last_gift'] = {
            'type': gift_type,
            'sender': sender,
            'timestamp': datetime.now().isoformat()
        }
        self.status['gift_count'] += 1
        
        # Виконання дій для подарунка
        result = {'success': True, 'actions': []}
        
        try:
            if gift_type == 'ROSE':
                # Роза - м'яке рожеве світло
                self.control_led_strip('set_color', {'color': '#ff69b4', 'brightness': 0.3})
                self.play_sound_effect('rose')
                result['actions'].append('led_color_rose')
                result['actions'].append('sound_rose')
                
            elif gift_type == 'HEART':
                # Серце - пульсуюче червоне світло
                self.control_led_strip('pulse', {'color': '#ff0000', 'duration': 3})
                self.control_servo_motor(45)
                result['actions'].append('led_pulse_red')
                result['actions'].append('servo_move')
                
            elif gift_type == 'STAR':
                # Зірка - блимаюче золоте світло
                self.control_led_strip('twinkle', {'color': '#ffd700', 'duration': 2})
                self.play_sound_effect('star')
                result['actions'].append('led_twinkle_gold')
                result['actions'].append('sound_star')
                
            elif gift_type == 'CROWN':
                # Корона - помаранчеве світло з ефектом
                self.control_led_strip('rainbow', {'duration': 3})
                self.control_servo_motor(180)
                result['actions'].append('led_rainbow')
                result['actions'].append('servo_full_rotation')
                
            elif gift_type == 'DIAMOND':
                # Діамант - яскраве блакитне світло
                self.control_led_strip('set_color', {'color': '#00bfff', 'brightness': 1.0})
                self.take_photo(f'diamond_gift_{int(time.time())}.jpg')
                result['actions'].append('led_bright_blue')
                result['actions'].append('photo_taken')
                
            elif gift_type == 'ROCKET':
                # Ракета - червоно-помаранчевий ефект з рухом
                self.control_led_strip('chase', {'color': '#ff4500', 'duration': 2})
                self.control_servo_motor(0)
                time.sleep(0.5)
                self.control_servo_motor(180)
                result['actions'].append('led_chase_orange')
                result['actions'].append('servo_rocket_effect')
                
            elif gift_type == 'UNICORN':
                # Єдиноріг - фіолетовий з радужним ефектом
                self.control_led_strip('unicorn', {'duration': 5})
                self.play_sound_effect('unicorn')
                self.take_photo(f'unicorn_gift_{int(time.time())}.jpg')
                result['actions'].append('led_unicorn_effect')
                result['actions'].append('sound_unicorn')
                result['actions'].append('photo_unicorn')
            
            else:
                # Невідомий тип подарунка
                self.control_led_strip('set_color', {'color': '#ffffff', 'brightness': 0.5})
                result['actions'].append('led_default_white')
            
        except Exception as e:
            logger.error(f"Помилка обробки подарунка: {e}")
            result['success'] = False
            result['error'] = str(e)
        
        return result
    
    def control_led_strip(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Керування LED стрічкою"""
        if not self.led_strip:
            return {'success': False, 'error': 'LED стрічка не доступна'}
        
        try:
            if action == 'set_color':
                color = params.get('color', '#ffffff')
                brightness = params.get('brightness', 0.5)
                
                # Конвертація hex в RGB
                color_rgb = self.hex_to_rgb(color)
                
                # Встановлення яскравості
                self.led_strip.brightness = brightness
                
                # Встановлення кольору для всіх LED
                for i in range(self.led_count):
                    self.led_strip[i] = color_rgb
                
                self.led_strip.show()
                return {'success': True, 'action': 'set_color', 'color': color}
            
            elif action == 'pulse':
                color = params.get('color', '#ff0000')
                duration = params.get('duration', 3)
                
                color_rgb = self.hex_to_rgb(color)
                
                # Пульсуючий ефект
                for _ in range(int(duration * 10)):
                    for brightness in [0.1, 0.3, 0.5, 0.7, 1.0, 0.7, 0.5, 0.3, 0.1]:
                        self.led_strip.brightness = brightness
                        for i in range(self.led_count):
                            self.led_strip[i] = color_rgb
                        self.led_strip.show()
                        time.sleep(0.1)
                
                return {'success': True, 'action': 'pulse', 'color': color}
            
            elif action == 'twinkle':
                color = params.get('color', '#ffd700')
                duration = params.get('duration', 2)
                
                color_rgb = self.hex_to_rgb(color)
                
                # Блимаючий ефект
                for _ in range(int(duration * 5)):
                    # Випадкові LED блимають
                    for i in range(self.led_count):
                        if i % 3 == 0:  # Кожен третій LED
                            self.led_strip[i] = color_rgb
                        else:
                            self.led_strip[i] = (0, 0, 0)
                    self.led_strip.show()
                    time.sleep(0.2)
                    
                    # Всі LED вимкнені
                    self.led_strip.fill((0, 0, 0))
                    self.led_strip.show()
                    time.sleep(0.2)
                
                return {'success': True, 'action': 'twinkle', 'color': color}
            
            elif action == 'rainbow':
                duration = params.get('duration', 3)
                
                # Радужний ефект
                for _ in range(int(duration * 10)):
                    for i in range(self.led_count):
                        hue = (i * 360 / self.led_count + time.time() * 50) % 360
                        color_rgb = self.hsv_to_rgb(hue, 1.0, 1.0)
                        self.led_strip[i] = color_rgb
                    self.led_strip.show()
                    time.sleep(0.1)
                
                return {'success': True, 'action': 'rainbow'}
            
            elif action == 'chase':
                color = params.get('color', '#ff4500')
                duration = params.get('duration', 2)
                
                color_rgb = self.hex_to_rgb(color)
                
                # Ефект переслідування
                for _ in range(int(duration * 5)):
                    for pos in range(self.led_count):
                        self.led_strip.fill((0, 0, 0))
                        self.led_strip[pos] = color_rgb
                        if pos > 0:
                            self.led_strip[pos-1] = tuple(int(c * 0.5) for c in color_rgb)
                        if pos < self.led_count - 1:
                            self.led_strip[pos+1] = tuple(int(c * 0.5) for c in color_rgb)
                        self.led_strip.show()
                        time.sleep(0.05)
                
                return {'success': True, 'action': 'chase', 'color': color}
            
            elif action == 'unicorn':
                duration = params.get('duration', 5)
                
                # Унікальний ефект для єдинорога
                for _ in range(int(duration * 10)):
                    for i in range(self.led_count):
                        # Фіолетовий з радужними відтінками
                        hue = (240 + i * 120 / self.led_count + time.time() * 30) % 360
                        color_rgb = self.hsv_to_rgb(hue, 0.8, 1.0)
                        self.led_strip[i] = color_rgb
                    self.led_strip.show()
                    time.sleep(0.1)
                
                return {'success': True, 'action': 'unicorn'}
            
            else:
                return {'success': False, 'error': f'Невідома дія: {action}'}
                
        except Exception as e:
            logger.error(f"Помилка керування LED стрічкою: {e}")
            return {'success': False, 'error': str(e)}
    
    def control_servo_motor(self, angle: int) -> Dict[str, Any]:
        """Керування сервоприводом"""
        if not GPIO_AVAILABLE:
            return {'success': False, 'error': 'GPIO не доступний'}
        
        try:
            # Конвертація кута в duty cycle
            duty = 2 + (angle / 18)
            self.servo_pwm.ChangeDutyCycle(duty)
            time.sleep(0.5)
            self.servo_pwm.ChangeDutyCycle(0)  # Зупинка PWM
            
            return {'success': True, 'angle': angle}
            
        except Exception as e:
            logger.error(f"Помилка керування сервоприводом: {e}")
            return {'success': False, 'error': str(e)}
    
    def play_sound_effect(self, sound_type: str) -> Dict[str, Any]:
        """Відтворення звукового ефекту"""
        if not SOUND_AVAILABLE:
            return {'success': False, 'error': 'Звук не доступний'}
        
        try:
            sound_file = self.sound_files.get(sound_type)
            if sound_file and os.path.exists(sound_file):
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
                return {'success': True, 'sound': sound_type}
            else:
                # Простий звук через GPIO бузер
                if GPIO_AVAILABLE:
                    self.buzzer_beep()
                return {'success': True, 'sound': 'beep'}
                
        except Exception as e:
            logger.error(f"Помилка відтворення звуку: {e}")
            return {'success': False, 'error': str(e)}
    
    def buzzer_beep(self):
        """Простий звук через бузер"""
        if not GPIO_AVAILABLE:
            return
        
        try:
            # Простий beep
            for _ in range(3):
                GPIO.output(self.gpio_pins['buzzer'], GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(self.gpio_pins['buzzer'], GPIO.LOW)
                time.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Помилка бузера: {e}")
    
    def take_photo(self, filename: str) -> Dict[str, Any]:
        """Зйомка фото"""
        if not self.camera:
            return {'success': False, 'error': 'Камера не доступна'}
        
        try:
            photo_path = f'photos/{filename}'
            os.makedirs('photos', exist_ok=True)
            
            self.camera.capture(photo_path)
            return {'success': True, 'photo': photo_path}
            
        except Exception as e:
            logger.error(f"Помилка зйомки фото: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_all_components(self) -> Dict[str, Any]:
        """Тестування всіх компонентів"""
        results = {}
        
        # Тест LED стрічки
        if self.led_strip:
            try:
                self.control_led_strip('set_color', {'color': '#00ff00', 'brightness': 0.5})
                time.sleep(1)
                self.control_led_strip('set_color', {'color': '#000000', 'brightness': 0})
                results['led'] = {'success': True, 'message': 'LED стрічка працює'}
            except Exception as e:
                results['led'] = {'success': False, 'error': str(e)}
        else:
            results['led'] = {'success': False, 'error': 'LED стрічка не доступна'}
        
        # Тест сервоприводу
        if GPIO_AVAILABLE:
            try:
                self.control_servo_motor(90)
                results['servo'] = {'success': True, 'message': 'Сервопривід працює'}
            except Exception as e:
                results['servo'] = {'success': False, 'error': str(e)}
        else:
            results['servo'] = {'success': False, 'error': 'GPIO не доступний'}
        
        # Тест звуку
        if SOUND_AVAILABLE:
            try:
                self.play_sound_effect('beep')
                results['sound'] = {'success': True, 'message': 'Звук працює'}
            except Exception as e:
                results['sound'] = {'success': False, 'error': str(e)}
        else:
            results['sound'] = {'success': False, 'error': 'Звук не доступний'}
        
        # Тест камери
        if self.camera:
            try:
                self.take_photo('test_photo.jpg')
                results['camera'] = {'success': True, 'message': 'Камера працює'}
            except Exception as e:
                results['camera'] = {'success': False, 'error': str(e)}
        else:
            results['camera'] = {'success': False, 'error': 'Камера не доступна'}
        
        return results
    
    def hex_to_rgb(self, hex_color: str) -> tuple:
        """Конвертація hex кольору в RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def hsv_to_rgb(self, h: float, s: float, v: float) -> tuple:
        """Конвертація HSV в RGB"""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h/360, s, v)
        return (int(r*255), int(g*255), int(b*255))
    
    def on_mqtt_connect(self, client, userdata, flags, rc):
        """Callback для MQTT підключення"""
        logger.info(f"MQTT підключено з кодом {rc}")
        client.subscribe("tt-fizmehdia/gift")
    
    def on_mqtt_message(self, client, userdata, msg):
        """Callback для MQTT повідомлень"""
        try:
            data = json.loads(msg.payload.decode())
            gift_type = data.get('type')
            sender = data.get('sender')
            
            if gift_type:
                self.process_gift(gift_type, sender)
                
        except Exception as e:
            logger.error(f"Помилка обробки MQTT повідомлення: {e}")
    
    def run(self, host='0.0.0.0', port=5001, debug=False):
        """Запуск сервера"""
        logger.info(f"Запуск TT-FizMehdia Raspberry Pi Controller на {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)
    
    def cleanup(self):
        """Очищення ресурсів"""
        if GPIO_AVAILABLE:
            GPIO.cleanup()
        
        if self.camera:
            self.camera.close()
        
        if MQTT_AVAILABLE and hasattr(self, 'mqtt_client'):
            self.mqtt_client.disconnect()
        
        logger.info("Ресурси очищено")

if __name__ == '__main__':
    try:
        controller = TTFizMehdiaPi()
        controller.run(debug=True)
    except KeyboardInterrupt:
        logger.info("Зупинка контролера...")
    finally:
        if 'controller' in locals():
            controller.cleanup()
