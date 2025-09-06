#!/bin/bash
# TT-FizMehdia Raspberry Pi Setup Script
# Скрипт для налаштування Raspberry Pi

echo "🍓 Налаштування TT-FizMehdia на Raspberry Pi..."

# Оновлення системи
echo "📦 Оновлення системи..."
sudo apt update && sudo apt upgrade -y

# Встановлення Python залежностей
echo "🐍 Встановлення Python залежностей..."
sudo apt install -y python3-pip python3-venv python3-dev

# Встановлення системних залежностей
echo "🔧 Встановлення системних залежностей..."
sudo apt install -y git i2c-tools libi2c-dev

# Встановлення залежностей для GPIO
echo "⚡ Встановлення GPIO залежностей..."
sudo apt install -y python3-rpi.gpio

# Встановлення залежностей для камери
echo "📷 Встановлення залежностей для камери..."
sudo apt install -y python3-picamera

# Встановлення залежностей для звуку
echo "🔊 Встановлення залежностей для звуку..."
sudo apt install -y python3-pygame

# Встановлення залежностей для LED стрічок
echo "💡 Встановлення залежностей для NeoPixel..."
sudo pip3 install adafruit-circuitpython-neopixel

# Встановлення MQTT
echo "📡 Встановлення MQTT..."
sudo apt install -y mosquitto mosquitto-clients
sudo pip3 install paho-mqtt

# Створення віртуального середовища
echo "🌐 Створення віртуального середовища..."
python3 -m venv venv
source venv/bin/activate

# Встановлення Python пакетів
echo "📚 Встановлення Python пакетів..."
pip install -r requirements_pi.txt

# Створення папок
echo "📁 Створення папок..."
mkdir -p photos sounds logs templates static

# Налаштування GPIO
echo "⚙️ Налаштування GPIO..."
sudo usermod -a -G gpio $USER
sudo usermod -a -G i2c $USER

# Налаштування I2C
echo "🔌 Налаштування I2C..."
sudo raspi-config nonint do_i2c 0

# Налаштування SPI
echo "🔌 Налаштування SPI..."
sudo raspi-config nonint do_spi 0

# Налаштування камери
echo "📷 Налаштування камери..."
sudo raspi-config nonint do_camera 0

# Створення systemd сервісу
echo "🚀 Створення systemd сервісу..."
sudo tee /etc/systemd/system/tt-fizmehdia.service > /dev/null <<EOF
[Unit]
Description=TT-FizMehdia Raspberry Pi Controller
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python tt_fizmehdia_pi.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Перезавантаження systemd
sudo systemctl daemon-reload
sudo systemctl enable tt-fizmehdia

# Створення звукових файлів (заглушки)
echo "🎵 Створення звукових файлів..."
mkdir -p sounds
touch sounds/rose.wav sounds/heart.wav sounds/star.wav sounds/crown.wav
touch sounds/diamond.wav sounds/rocket.wav sounds/unicorn.wav

# Налаштування прав доступу
echo "🔐 Налаштування прав доступу..."
chmod +x tt_fizmehdia_pi.py
chmod 755 photos sounds logs

# Створення конфігураційного файлу
echo "⚙️ Створення конфігураційного файлу..."
cat > .env <<EOF
# TT-FizMehdia Raspberry Pi Configuration
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

# MQTT (опціонально)
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC=tt-fizmehdia/gift

# Логування
LOG_LEVEL=INFO
LOG_FILE=logs/pi_controller.log
EOF

echo "✅ Налаштування завершено!"
echo ""
echo "🚀 Для запуску сервісу:"
echo "   sudo systemctl start tt-fizmehdia"
echo ""
echo "📊 Для перегляду статусу:"
echo "   sudo systemctl status tt-fizmehdia"
echo ""
echo "📝 Для перегляду логів:"
echo "   sudo journalctl -u tt-fizmehdia -f"
echo ""
echo "🌐 Веб-інтерфейс буде доступний за адресою:"
echo "   http://$(hostname -I | awk '{print $1}'):5001"
echo ""
echo "⚠️  Не забудьте перезавантажити Raspberry Pi для застосування всіх змін!"
echo "   sudo reboot"
