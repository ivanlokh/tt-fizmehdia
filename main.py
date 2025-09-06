#!/usr/bin/env python3
"""
TT-FizMehdia - Система перетворення TikTok-подарунків на дії пристрою
Python версія з Arduino інтеграцією
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# Flask та веб-компоненти
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room

# Робота з Arduino
import serial
import serial.tools.list_ports

# HTTP запити та веб-скрапінг
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Конфігурація
from dotenv import load_dotenv

# Локальні модулі
from src.arduino_manager import ArduinoManager
from src.tiktok_monitor import TikTokMonitor
from src.device_manager import DeviceManager
from src.gift_processor import GiftProcessor
from src.config import Config

# Завантаження змінних середовища
load_dotenv()

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Створення Flask додатку
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Глобальні менеджери
config = Config()
arduino_manager = ArduinoManager()
tiktok_monitor = TikTokMonitor()
device_manager = DeviceManager()
gift_processor = GiftProcessor()

# Глобальні змінні
connected_devices: Dict[str, dict] = {}
gift_actions: Dict[str, dict] = {}
active_streams: Dict[str, dict] = {}

@app.route('/')
def index():
    """Головна сторінка"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Отримання статусу системи"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'connected_devices': len(connected_devices),
        'active_streams': len(active_streams),
        'arduino_connected': arduino_manager.is_connected(),
        'tiktok_monitoring': tiktok_monitor.is_monitoring()
    })

@app.route('/api/devices', methods=['GET'])
def get_devices():
    """Отримання списку пристроїв"""
    return jsonify({
        'devices': list(connected_devices.values()),
        'count': len(connected_devices)
    })

@app.route('/api/devices', methods=['POST'])
def add_device():
    """Додавання нового пристрою"""
    try:
        data = request.get_json()
        device_id = device_manager.add_device(data)
        connected_devices[device_id] = data
        connected_devices[device_id]['id'] = device_id
        connected_devices[device_id]['status'] = 'connected'
        connected_devices[device_id]['last_seen'] = datetime.now().isoformat()
        
        logger.info(f"Додано пристрій: {data.get('name', 'Unknown')}")
        return jsonify({'success': True, 'device_id': device_id})
    
    except Exception as e:
        logger.error(f"Помилка додавання пристрою: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/devices/<device_id>', methods=['DELETE'])
def remove_device(device_id):
    """Видалення пристрою"""
    if device_id in connected_devices:
        del connected_devices[device_id]
        logger.info(f"Видалено пристрій: {device_id}")
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Пристрій не знайдено'}), 404

@app.route('/api/gifts/actions', methods=['GET'])
def get_gift_actions():
    """Отримання налаштувань дій для подарунків"""
    return jsonify({
        'actions': list(gift_actions.values()),
        'count': len(gift_actions)
    })

@app.route('/api/gifts/actions', methods=['POST'])
def set_gift_action():
    """Налаштування дії для подарунка"""
    try:
        data = request.get_json()
        gift_type = data.get('gift_type')
        device_id = data.get('device_id')
        action = data.get('action')
        params = data.get('params', {})
        
        if not all([gift_type, device_id, action]):
            return jsonify({'success': False, 'error': 'Необхідні поля: gift_type, device_id, action'}), 400
        
        if device_id not in connected_devices:
            return jsonify({'success': False, 'error': 'Пристрій не знайдено'}), 404
        
        gift_actions[gift_type] = {
            'gift_type': gift_type,
            'device_id': device_id,
            'action': action,
            'params': params,
            'enabled': data.get('enabled', True),
            'created_at': datetime.now().isoformat()
        }
        
        logger.info(f"Налаштовано дію для подарунка {gift_type}: {action}")
        return jsonify({'success': True})
    
    except Exception as e:
        logger.error(f"Помилка налаштування дії: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/arduino/connect', methods=['POST'])
def connect_arduino():
    """Підключення до Arduino"""
    try:
        data = request.get_json()
        port = data.get('port')
        baudrate = data.get('baudrate', 9600)
        
        if arduino_manager.connect(port, baudrate):
            logger.info(f"Підключено до Arduino на порту {port}")
            return jsonify({'success': True, 'port': port})
        else:
            return jsonify({'success': False, 'error': 'Не вдалося підключитися до Arduino'}), 400
    
    except Exception as e:
        logger.error(f"Помилка підключення до Arduino: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/arduino/ports', methods=['GET'])
def get_arduino_ports():
    """Отримання списку доступних портів"""
    ports = arduino_manager.get_available_ports()
    return jsonify({'ports': ports})

@app.route('/api/arduino/test', methods=['POST'])
def test_arduino():
    """Тестування Arduino"""
    try:
        data = request.get_json()
        command = data.get('command', 'test')
        
        result = arduino_manager.send_command(command)
        return jsonify({'success': True, 'result': result})
    
    except Exception as e:
        logger.error(f"Помилка тестування Arduino: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/tiktok/start_monitoring', methods=['POST'])
def start_tiktok_monitoring():
    """Запуск моніторингу TikTok"""
    try:
        data = request.get_json()
        username = data.get('username')
        
        if not username:
            return jsonify({'success': False, 'error': 'Ім\'я користувача обов\'язкове'}), 400
        
        if tiktok_monitor.start_monitoring(username, on_gift_received):
            logger.info(f"Запущено моніторинг TikTok для {username}")
            return jsonify({'success': True, 'username': username})
        else:
            return jsonify({'success': False, 'error': 'Не вдалося запустити моніторинг'}), 400
    
    except Exception as e:
        logger.error(f"Помилка запуску моніторингу: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/tiktok/stop_monitoring', methods=['POST'])
def stop_tiktok_monitoring():
    """Зупинка моніторингу TikTok"""
    try:
        tiktok_monitor.stop_monitoring()
        logger.info("Зупинено моніторинг TikTok")
        return jsonify({'success': True})
    
    except Exception as e:
        logger.error(f"Помилка зупинки моніторингу: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/simulate/gift', methods=['POST'])
def simulate_gift():
    """Симуляція отримання подарунка"""
    try:
        data = request.get_json()
        gift_type = data.get('gift_type', 'ROSE')
        sender = data.get('sender', 'Test User')
        
        gift_event = {
            'type': gift_type,
            'sender': sender,
            'timestamp': datetime.now().isoformat(),
            'value': config.GIFT_VALUES.get(gift_type, 1)
        }
        
        # Обробка подарунка
        asyncio.create_task(process_gift_async(gift_event))
        
        return jsonify({'success': True, 'gift': gift_event})
    
    except Exception as e:
        logger.error(f"Помилка симуляції подарунка: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# WebSocket події
@socketio.on('connect')
def handle_connect():
    """Підключення клієнта"""
    logger.info(f"Клієнт підключився: {request.sid}")
    emit('status', {'message': 'Підключено до сервера'})

@socketio.on('disconnect')
def handle_disconnect():
    """Відключення клієнта"""
    logger.info(f"Клієнт відключився: {request.sid}")

@socketio.on('join_room')
def handle_join_room(data):
    """Приєднання до кімнати"""
    room = data.get('room', 'default')
    join_room(room)
    emit('status', {'message': f'Приєднано до кімнати {room}'})

# Обробка подарунків
async def process_gift_async(gift_event):
    """Асинхронна обробка подарунка"""
    try:
        # Відправка події через WebSocket
        socketio.emit('gift_received', gift_event)
        
        # Пошук налаштованої дії
        gift_type = gift_event['type']
        if gift_type in gift_actions:
            action_config = gift_actions[gift_type]
            
            if action_config['enabled']:
                device_id = action_config['device_id']
                if device_id in connected_devices:
                    device = connected_devices[device_id]
                    action = action_config['action']
                    params = action_config['params']
                    
                    # Виконання дії
                    result = await execute_device_action(device, action, params, gift_event)
                    
                    # Сповіщення про виконання
                    socketio.emit('action_executed', {
                        'gift': gift_event,
                        'action': action_config,
                        'device': device['name'],
                        'result': result,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    logger.info(f"Виконано дію {action} для подарунка {gift_type}")
                else:
                    logger.warning(f"Пристрій {device_id} не знайдено")
            else:
                logger.info(f"Дія для подарунка {gift_type} відключена")
        else:
            logger.info(f"Дія для подарунка {gift_type} не налаштована")
    
    except Exception as e:
        logger.error(f"Помилка обробки подарунка: {e}")

async def execute_device_action(device, action, params, gift_event):
    """Виконання дії на пристрої"""
    try:
        device_type = device.get('type', 'arduino')
        
        if device_type == 'arduino':
            # Відправка команди до Arduino
            command = f"{action}:{params.get('value', '')}"
            result = arduino_manager.send_command(command)
            return result
        
        elif device_type == 'http':
            # HTTP запит до пристрою
            url = f"http://{device['ip']}:{device.get('port', 80)}/api/command"
            response = requests.post(url, json={
                'action': action,
                'params': params,
                'gift': gift_event
            }, timeout=5)
            return response.json()
        
        else:
            logger.warning(f"Невідомий тип пристрою: {device_type}")
            return None
    
    except Exception as e:
        logger.error(f"Помилка виконання дії: {e}")
        return None

def on_gift_received(gift_event):
    """Callback для отримання подарунка від TikTok"""
    asyncio.create_task(process_gift_async(gift_event))

# Ініціалізація
def init_app():
    """Ініціалізація додатку"""
    # Створення папки для логів
    Path('logs').mkdir(exist_ok=True)
    
    # Створення папки для шаблонів
    Path('templates').mkdir(exist_ok=True)
    
    # Створення папки для статичних файлів
    Path('static').mkdir(exist_ok=True)
    
    logger.info("TT-FizMehdia ініціалізовано")

if __name__ == '__main__':
    init_app()
    
    # Запуск сервера
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Запуск сервера на порту {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)
