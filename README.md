# 🎁⚡ TT-FizMehdia

**Система перетворення TikTok-подарунків на дії пристрою**

Python + Arduino інтеграція для створення інтерактивних ефектів на основі TikTok-подарунків у реальному часі.

---

## 📋 Зміст

- [Огляд проекту](#-огляд-проекту)
- [Архітектура](#-архітектура)
- [Технологічний стек](#-технологічний-стек)
- [Встановлення](#-встановлення)
- [Налаштування](#-налаштування)
- [Використання](#-використання)
- [Arduino інтеграція](#-arduino-інтеграція)
- [API документація](#-api-документація)
- [Приклади використання](#-приклади-використання)
- [Розробка](#-розробка)
- [Внесок у проект](#-внесок-у-проект)

---

## 🎯 Огляд проекту

TT-FizMehdia - це інноваційна система, яка дозволяє перетворювати віртуальні подарунки від глядачів TikTok на реальні фізичні дії пристроїв. Коли ваші глядачі надсилають подарунки під час прямого ефіру, система автоматично виконує налаштовані дії на підключених пристроях.

### ✨ Основні можливості

- **🔄 Реальний час**: Миттєва реакція на TikTok-подарунки
- **🔌 Arduino підтримка**: Повна інтеграція з Arduino/ESP32/ESP8266
- **🎨 Гнучкі ефекти**: Налаштування унікальних дій для кожного типу подарунка
- **🌐 Веб-інтерфейс**: Зручне керування через браузер
- **📡 WebSocket**: Оновлення в реальному часі
- **🔒 Безпека**: Захист та валідація всіх операцій

---

## 🏗️ Архітектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   TikTok Live   │───▶│  Python Server  │───▶│  Arduino Device │
│                 │    │                 │    │                 │
│ • Подарунки     │    │ • Flask API     │    │ • LED стрічки   │
│ • Коментарі     │    │ • WebSocket     │    │ • Сервоприводи  │
│ • Події         │    │ • Моніторинг    │    │ • Звук          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Веб-інтерфейс  │
                       │                 │
                       │ • Налаштування  │
                       │ • Моніторинг    │
                       │ • Тестування    │
                       └─────────────────┘
```

### Компоненти системи

1. **Python Backend** - Основний сервер на Flask
2. **Arduino Manager** - Менеджер для роботи з Arduino пристроями
3. **TikTok Monitor** - Моніторинг подій TikTok
4. **Device Manager** - Управління підключеними пристроями
5. **Gift Processor** - Обробка подарунків та виконання дій
6. **Web Interface** - Веб-інтерфейс для налаштування

---

## 🛠️ Технологічний стек

### Backend
- **Python 3.8+** - Основний мова програмування
- **Flask** - Веб-фреймворк
- **Flask-SocketIO** - WebSocket підтримка
- **PySerial** - Комунікація з Arduino
- **Selenium** - Веб-скрапінг TikTok
- **Requests** - HTTP клієнт

### Frontend
- **HTML5/CSS3** - Структура та стилі
- **JavaScript** - Інтерактивність
- **Socket.IO** - Реальний час
- **Bootstrap** - UI компоненти

### Hardware
- **Arduino Uno/Nano** - Базовий мікроконтролер
- **ESP32/ESP8266** - WiFi підтримка
- **WS2812B LED** - Адресовані LED стрічки
- **Сервоприводи** - Рухомі частини
- **Бузери** - Звукові ефекти

---

## 🚀 Встановлення

### Вимоги
- Python 3.8 або новіша версія
- Arduino IDE
- Arduino/ESP32/ESP8266 пристрій
- USB кабель для підключення Arduino

### Крок 1: Клонування репозиторію
```bash
git clone https://github.com/your-username/tt-fizmehdia.git
cd tt-fizmehdia
```

### Крок 2: Створення віртуального середовища
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Крок 3: Встановлення залежностей
```bash
pip install -r requirements.txt
```

### Крок 4: Налаштування змінних середовища
```bash
cp .env.example .env
# Відредагуйте .env файл з вашими налаштуваннями
```

### Крок 5: Запуск сервера
```bash
python main.py
```

Сервер буде доступний за адресою: `http://localhost:5000`

---

## ⚙️ Налаштування

### Змінні середовища (.env)
```env
# Налаштування сервера
HOST=0.0.0.0
PORT=5000
DEBUG=False
SECRET_KEY=your-secret-key-here

# Налаштування Arduino
ARDUINO_BAUDRATE=9600
ARDUINO_TIMEOUT=5
ARDUINO_RETRY_COUNT=3

# Налаштування TikTok
TIKTOK_MONITORING_INTERVAL=2
TIKTOK_TIMEOUT=30

# Налаштування пристроїв
DEVICE_HEARTBEAT_INTERVAL=30
MAX_DEVICES=10

# Налаштування логування
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Конфігурація пристроїв
```python
# src/config.py
GIFT_VALUES = {
    'ROSE': 1,
    'HEART': 5,
    'STAR': 10,
    'CROWN': 50,
    'DIAMOND': 100,
    'ROCKET': 200,
    'UNICORN': 500
}

GIFT_COLORS = {
    'ROSE': '#ff69b4',
    'HEART': '#ff0000',
    'STAR': '#ffd700',
    'CROWN': '#ff8c00',
    'DIAMOND': '#00bfff',
    'ROCKET': '#ff4500',
    'UNICORN': '#9370db'
}
```

---

## 🎮 Використання

### 1. Підключення Arduino
1. Підключіть Arduino до комп'ютера через USB
2. Відкрийте веб-інтерфейс
3. Перейдіть до розділу "Arduino"
4. Виберіть порт та натисніть "Підключити"

### 2. Налаштування пристроїв
```json
{
  "name": "LED Controller",
  "type": "arduino",
  "port": "COM3",
  "baudrate": 9600,
  "actions": [
    {
      "gift_type": "ROSE",
      "action": "set_color",
      "params": {
        "color": "#ff69b4",
        "brightness": 50,
        "duration": 3000
      }
    }
  ]
}
```

### 3. Налаштування дій для подарунків
- **🌹 Роза** → М'яке рожеве світло
- **❤️ Серце** → Пульсуюче червоне світло
- **⭐ Зірка** → Блимаюче золоте світло
- **👑 Корона** → Помаранчеве світло з ефектом
- **💎 Діамант** → Яскраве блакитне світло
- **🚀 Ракета** → Червоно-помаранчевий ефект
- **🦄 Єдиноріг** → Фіолетовий з радужним ефектом

### 4. Запуск моніторингу TikTok
1. Введіть ваш TikTok username
2. Натисніть "Почати моніторинг"
3. Запустіть прямий ефір у TikTok
4. Насолоджуйтесь реакцією пристроїв на подарунки!

---

## 🔌 Arduino інтеграція

### Підтримувані платформи
- **Arduino Uno/Nano** - Базові проекти
- **ESP32** - WiFi підтримка, більше можливостей
- **ESP8266** - Компактний WiFi модуль

### Підключення компонентів

#### LED стрічка (WS2812B)
```
Arduino    WS2812B
Pin 2  →   DIN
5V     →   VCC
GND    →   GND
```

#### Сервоприводи
```
Arduino    Servo
Pin 3  →   Signal (Servo 1)
Pin 4  →   Signal (Servo 2)
5V     →   VCC
GND    →   GND
```

#### Бузер
```
Arduino    Buzzer
Pin 5  →   Positive
GND    →   Negative
```

### Приклад Arduino коду
```cpp
// arduino/tt_fizmehdia_controller.ino
#include <FastLED.h>

#define LED_PIN 2
#define NUM_LEDS 60
CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(50);
  Serial.println("TT-FizMehdia Ready!");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    processCommand(command);
  }
}

void processCommand(String command) {
  if (command.startsWith("GIFT:")) {
    String giftType = command.substring(5);
    playGiftEffect(giftType);
  }
  else if (command.startsWith("LED:COLOR:")) {
    // Обробка кольору LED
    setLEDColor(command);
  }
  else if (command == "LED:CLEAR") {
    clearLEDs();
  }
}

void playGiftEffect(String giftType) {
  if (giftType == "ROSE") {
    setLEDColor("#ff69b4", 30, 2000);
  }
  else if (giftType == "DIAMOND") {
    setLEDColor("#00bfff", 100, 3000);
  }
  // ... інші ефекти
}
```

---

## 📚 API документація

### Статус системи
```http
GET /api/status
```

**Відповідь:**
```json
{
  "status": "online",
  "timestamp": "2024-01-01T12:00:00Z",
  "connected_devices": 2,
  "active_streams": 1,
  "arduino_connected": true,
  "tiktok_monitoring": true
}
```

### Управління пристроями
```http
GET /api/devices
POST /api/devices
DELETE /api/devices/{device_id}
```

### Arduino управління
```http
GET /api/arduino/ports
POST /api/arduino/connect
POST /api/arduino/test
```

### TikTok моніторинг
```http
POST /api/tiktok/start_monitoring
POST /api/tiktok/stop_monitoring
```

### Симуляція подарунків
```http
POST /api/simulate/gift
Content-Type: application/json

{
  "gift_type": "ROSE",
  "sender": "Test User"
}
```

### WebSocket події
```javascript
// Підключення
const socket = io();

// Отримання подарунка
socket.on('gift_received', (gift) => {
  console.log('Отримано подарунок:', gift);
});

// Виконання дії
socket.on('action_executed', (action) => {
  console.log('Виконано дію:', action);
});
```

---

## 💡 Приклади використання

### Проект 1: LED Dance Floor
```python
# Налаштування для танцювальної підлоги
dance_floor_config = {
    "name": "Dance Floor LED",
    "type": "arduino",
    "port": "COM3",
    "actions": {
        "ROSE": {
            "action": "set_color",
            "params": {"color": "#ff69b4", "brightness": 30}
        },
        "DIAMOND": {
            "action": "led_rainbow",
            "params": {"duration": 5000}
        }
    }
}
```

### Проект 2: Робот-танцюрист
```python
# Налаштування для робота
robot_config = {
    "name": "Dance Robot",
    "type": "arduino",
    "port": "COM4",
    "actions": {
        "HEART": {
            "action": "servo_move",
            "params": {"servo": 1, "angle": 45}
        },
        "ROCKET": {
            "action": "servo_move",
            "params": {"servo": 1, "angle": 180}
        }
    }
}
```

### Проект 3: Звукова система
```python
# Налаштування для звуку
sound_config = {
    "name": "Gift Sound System",
    "type": "arduino",
    "port": "COM5",
    "actions": {
        "STAR": {
            "action": "play_sound",
            "params": {"sound": "chime", "duration": 1000}
        },
        "UNICORN": {
            "action": "play_sound",
            "params": {"sound": "magic", "duration": 2000}
        }
    }
}
```

---

## 🔧 Розробка

### Структура проекту
```
tt-fizmehdia/
├── main.py                 # Головний файл
├── requirements.txt        # Залежності Python
├── .env.example           # Приклад змінних середовища
├── src/                   # Вихідний код
│   ├── config.py          # Конфігурація
│   ├── arduino_manager.py # Менеджер Arduino
│   ├── tiktok_monitor.py  # Моніторинг TikTok
│   ├── device_manager.py  # Управління пристроями
│   └── gift_processor.py  # Обробка подарунків
├── templates/             # HTML шаблони
├── static/               # Статичні файли
├── logs/                 # Логи
└── arduino/              # Код для Arduino
    ├── tt_fizmehdia_controller.ino
    └── simple_led_controller.ino
```

### Запуск в режимі розробки
```bash
# Встановлення залежностей для розробки
pip install -r requirements.txt

# Запуск з автоперезавантаженням
export FLASK_ENV=development
python main.py
```

### Тестування
```bash
# Запуск тестів
pytest tests/

# Перевірка коду
flake8 src/
black src/
```

### Логування
```python
import logging

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Повідомлення для логу")
```

---

## 🤝 Внесок у проект

### Як внести внесок
1. Fork репозиторій
2. Створіть feature branch (`git checkout -b feature/amazing-feature`)
3. Commit зміни (`git commit -m 'Add amazing feature'`)
4. Push до branch (`git push origin feature/amazing-feature`)
5. Відкрийте Pull Request

### Стандарти коду
- Дотримуйтесь PEP 8
- Додавайте docstrings до функцій
- Покривайте код тестами
- Оновлюйте документацію

### Звіти про помилки
- Використовуйте GitHub Issues
- Додавайте детальний опис проблеми
- Включайте логи та скріншоти

---

## 📄 Ліцензія

Цей проект ліцензовано під MIT License - дивіться файл [LICENSE](LICENSE) для деталей.

---

## 🆘 Підтримка

- 📧 **Email**: support@tt-fizmehdia.com
- 💬 **Discord**: [Приєднуйтесь до нашого серверу](https://discord.gg/tt-fizmehdia)
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-username/tt-fizmehdia/issues)
- 📖 **Wiki**: [Документація](https://github.com/your-username/tt-fizmehdia/wiki)

---

## 🙏 Подяки

- **TikTok** за створення платформи
- **Arduino** спільнота за інструменти
- **Python** спільнота за бібліотеки
- Всі **контент-кріейтори**, які тестують систему

---

**Зроблено з ❤️ для TikTok спільноти**

*Перетворюйте віртуальні подарунки на реальну магію!* ✨

---

## 📊 Статистика проекту

![GitHub stars](https://img.shields.io/github/stars/your-username/tt-fizmehdia)
![GitHub forks](https://img.shields.io/github/forks/your-username/tt-fizmehdia)
![GitHub issues](https://img.shields.io/github/issues/your-username/tt-fizmehdia)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Arduino](https://img.shields.io/badge/arduino-compatible-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg) 