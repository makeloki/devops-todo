FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY app.py .

# Создаем директорию для базы данных
RUN mkdir -p /data

# Запускаем приложение
CMD ["python", "app.py"]
