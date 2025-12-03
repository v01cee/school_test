# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости (если нужны для pandas/openpyxl)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем директории для файлов и данных
RUN mkdir -p /app/files /app/data

# Устанавливаем переменные окружения по умолчанию (можно переопределить)
ENV PYTHONUNBUFFERED=1

# Команда запуска
CMD ["python", "bot_main.py"]

