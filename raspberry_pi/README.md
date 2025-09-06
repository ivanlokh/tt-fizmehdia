# 🍓 TT-FizMehdia Raspberry Pi Controller

**Потужний контролер для Raspberry Pi з підтримкою GPIO, камери, звуку та мережі**

---

## 🎯 Огляд

Raspberry Pi контролер для TT-FizMehdia надає розширені можливості для створення інтерактивних ефектів на основі TikTok-подарунків. Він підтримує GPIO, камеру, звук, LED стрічки та мережеве керування.

---

## ✨ Можливості

### 🔌 GPIO підтримка
- **LED стрічки** (NeoPixel/WS2812B)
- **Сервоприводи** (PWM керування)
- **Бузери** та звукові сигнали
- **Кнопки** та датчики
- **Датчики руху** (PIR)

### 📷 Камера
- **Автоматична зйомка** при отриманні подарунків
- **Високоякісні фото** (до 4K)
- **Збереження з timestamp** та інформацією про подарунок

### 🔊 Звук
- **Відтворення звукових файлів** для кожного типу подарунка
- **Pygame підтримка** для якісного звуку
- **GPIO бузер** як резервний варіант

### 🌐 Мережеве керування
- **Flask веб-сервер** для віддаленого керування
- **MQTT підтримка** для IoT інтеграції
- **REST API** для програмування

### 💡 LED ефекти
- **Кольорові ефекти** для кожного подарунка
- **Анімації**: пульсація, блимання, радуга
- **Ефекти переслідування** та унікальні патерни

---

## 🛠️ Встановлення

### Автоматичне встановлення
```bash
# Клонування репозиторію
git clone https://github.com/your-username/tt-fizmehdia.git
cd tt-fizmehdia/raspberry_pi

# Запуск скрипта налаштування
chmod +x setup_pi.sh
./setup_pi.sh
```

### Ручне встановлення
```bash
# Оновлення системи
sudo apt update && sudo apt upgrade -y

# Встановлення залежностей
sudo apt install -y python3-pip python3-venv python3-dev
sudo apt install -y git i2c-tools libi2c-dev
sudo apt install -y python3-rpi.gpio python3-picamera python3-pygame
sudo apt install -y mosquitto mosquitto-clients

# Встановлення NeoPixel
sudo pip3 install adafruit-circuitpython-neopixel

# Створення віртуального середовища
python3 -m venv venv
source venv/bin/activate

# Встановлення Python пакетів
pip install -r requirements_pi.txt
```

---

## 🔌 Підключення компонентів

### LED стрічка (WS2812B/NeoPixel)
```
Raspberry Pi    WS2812B
GPIO 18    →    DIN
5V         →    VCC
GND        →    GND
```

### Сервопривід
```
Raspberry Pi    Servo
GPIO 12    →    Signal (PWM)
5V         →    VCC
GND        →    GND
```

### Бузер
```
Raspberry Pi    Buzzer
GPIO 13    →    Positive
GND        →    Negative
```

### Кнопка
```
Raspberry Pi    Button
GPIO 16    →    One side
3.3V       →    Other side (with pull-up)
```

### Датчик руху (PIR)
```
Raspberry Pi    PIR Sensor
GPIO 17    →    Output
5V         →    VCC
GND        →    GND
```

---

## 🚀 Запуск

### Ручний запуск
```bash
# Активація віртуального середовища
source venv/bin/activate

# Запуск контролера
python tt_fizmehdia_pi.py
```

### Автоматичний запуск (systemd)
```bash
# Запуск сервісу
sudo systemctl start tt-fizmehdia

# Автозапуск при завантаженні
sudo systemctl enable tt-fizmehdia

# Перегляд статусу
sudo systemctl status tt-fizmehdia

# Перегляд логів
sudo journalctl -u tt-fizmehdia -f
```

---

## 🌐 Веб-інтерфейс

Після запуску контролер буде доступний за адресою:
```
http://[IP_ADDRESS]:5001
```

### Основні сторінки:
- **/** - Головна сторінка з керуванням
- **/api/status** - Статус системи
- **/api/test** - Тестування компонентів

---

## 📚 API Документація

### Статус системи
```http
GET /api/status
```

**Відповідь:**
```json
{
  "gpio_available": true,
  "camera_available": true,
  "sound_available": true,
  "neopixel_available": true,
  "mqtt_available": true,
  "connected": true,
  "last_gift": {
    "type": "ROSE",
    "sender": "username",
    "timestamp": "2024-01-01T12:00:00Z"
  },
  "gift_count": 42
}
```

### Обробка подарунка
```http
POST /api/gift
Content-Type: application/json

{
  "type": "ROSE",
  "sender": "username"
}
```

### Керування LED стрічкою
```http
POST /api/led
Content-Type: application/json

{
  "action": "set_color",
  "params": {
    "color": "#ff69b4",
    "brightness": 0.5
  }
}
```

### Керування сервоприводом
```http
POST /api/servo
Content-Type: application/json

{
  "angle": 90
}
```

### Відтворення звуку
```http
POST /api/sound
Content-Type: application/json

{
  "type": "rose"
}
```

### Зйомка фото
```http
POST /api/camera
Content-Type: application/json

{
  "filename": "gift_photo.jpg"
}
```

### Тестування компонентів
```http
POST /api/test
```

---

## 🎨 Ефекти для подарунків

### 🌹 Роза (1 монета)
- М'яке рожеве світло
- Звук "rose.wav"
- Яскравість: 30%

### ❤️ Серце (5 монет)
- Пульсуюче червоне світло
- Рух сервоприводу (45°)
- Тривалість: 3 секунди

### ⭐ Зірка (10 монет)
- Блимаюче золоте світло
- Звук "star.wav"
- Тривалість: 2 секунди

### 👑 Корона (50 монет)
- Радужний ефект
- Повний поворот сервоприводу (180°)
- Тривалість: 3 секунди

### 💎 Діамант (100 монет)
- Яскраве блакитне світло
- Автоматична зйомка фото
- Яскравість: 100%

### 🚀 Ракета (200 монет)
- Ефект переслідування (помаранчевий)
- Сервопривід: 0° → 180°
- Тривалість: 2 секунди

### 🦄 Єдиноріг (500 монет)
- Унікальний фіолетово-радужний ефект
- Звук "unicorn.wav"
- Автоматична зйомка фото
- Тривалість: 5 секунд

---

## ⚙️ Конфігурація

### Змінні середовища (.env)
```env
# Налаштування сервера
HOST=0.0.0.0
PORT=5001
DEBUG=False

# GPIO налаштування
LED_PIN=18
SERVO_PIN=12
BUZZER_PIN=13
BUTTON_PIN=16
MOTION_SENSOR_PIN=17

# LED стрічка
LED_COUNT=60
LED_BRIGHTNESS=0.5

# Камера
CAMERA_RESOLUTION_WIDTH=640
CAMERA_RESOLUTION_HEIGHT=480

# MQTT
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC=tt-fizmehdia/gift

# Логування
LOG_LEVEL=INFO
LOG_FILE=logs/pi_controller.log
```

---

## 🔧 Налаштування Raspberry Pi

### Увімкнення інтерфейсів
```bash
# Запуск raspi-config
sudo raspi-config

# Увімкніть:
# - I2C
# - SPI
# - Camera
# - SSH (для віддаленого доступу)
```

### Налаштування через командний рядок
```bash
# I2C
sudo raspi-config nonint do_i2c 0

# SPI
sudo raspi-config nonint do_spi 0

# Камера
sudo raspi-config nonint do_camera 0

# SSH
sudo raspi-config nonint do_ssh 0
```

---

## 🎵 Звукові файли

Створіть папку `sounds/` та додайте звукові файли:
```
sounds/
├── rose.wav      # Звук для рози
├── heart.wav     # Звук для серця
├── star.wav      # Звук для зірки
├── crown.wav     # Звук для корони
├── diamond.wav   # Звук для діаманта
├── rocket.wav    # Звук для ракети
└── unicorn.wav   # Звук для єдинорога
```

**Рекомендації:**
- Формат: WAV або MP3
- Тривалість: 1-3 секунди
- Якість: 44.1 kHz, 16-bit

---

## 📸 Фото

Фото автоматично зберігаються в папці `photos/` з назвами:
```
photos/
├── diamond_gift_1704067200.jpg
├── unicorn_gift_1704067300.jpg
└── test_photo.jpg
```

---

## 🔍 Відладка

### Перевірка GPIO
```bash
# Список доступних GPIO
gpio readall

# Тест GPIO пінів
gpio mode 18 out
gpio write 18 1
gpio write 18 0
```

### Перевірка I2C
```bash
# Список I2C пристроїв
sudo i2cdetect -y 1
```

### Перевірка камери
```bash
# Тест камери
raspistill -o test.jpg
```

### Перевірка звуку
```bash
# Тест звуку
speaker-test -t wav -c 2
```

---

## 🚨 Вирішення проблем

### GPIO не працює
```bash
# Перевірте права доступу
sudo usermod -a -G gpio $USER

# Перезавантажте систему
sudo reboot
```

### Камера не працює
```bash
# Перевірте увімкнення камери
sudo raspi-config nonint do_camera 0

# Перезавантажте систему
sudo reboot
```

### LED стрічка не працює
```bash
# Перевірте підключення
# Переконайтеся що використовується GPIO 18
# Перевірте живлення (5V)
```

### Звук не працює
```bash
# Перевірте налаштування звуку
sudo raspi-config

# Тест звуку
aplay /usr/share/sounds/alsa/Front_Left.wav
```

---

## 📈 Моніторинг

### Логи системи
```bash
# Логи сервісу
sudo journalctl -u tt-fizmehdia -f

# Логи додатку
tail -f logs/pi_controller.log
```

### Моніторинг ресурсів
```bash
# Використання CPU та пам'яті
htop

# Температура
vcgencmd measure_temp

# Напруга
vcgencmd measure_volts
```

---

## 🔄 Оновлення

```bash
# Оновлення коду
git pull origin main

# Перезапуск сервісу
sudo systemctl restart tt-fizmehdia
```

---

## 🤝 Внесок у розробку

1. Fork репозиторій
2. Створіть feature branch
3. Commit зміни
4. Push до branch
5. Відкрийте Pull Request

---

## 📄 Ліцензія

MIT License - дивіться файл [LICENSE](../../LICENSE) для деталей.

---

**Зроблено з ❤️ для Raspberry Pi спільноти**

*Потужні можливості в компактному корпусі!* 🍓✨
