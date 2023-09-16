# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.11
FROM python:3.11-slim

# Встановимо змінну середовища

ENV APP_HOME /app 

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

# Скопіюємо інші файли в робочу директорію контейнера
COPY . .

# Встановимо залежності всередині контейнера

RUN pip inistall -r requirements.txt 

RUN python hw_05\server_websoket.py &
# RUN python hw_05\server_http_async.py

EXPOSE 8000/tcp

VOLUME $APP_HOME/logs


# Запустимо наш застосунок всередині контейнера
ENTRYPOINT [ "python", "hw_05\server_http_async.py" ]

