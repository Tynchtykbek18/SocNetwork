FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENV_FILE=.env

WORKDIR /manasgramback

RUN pip install --upgrade pip \
    && apt-get update

COPY requirements.txt /manasgramback/
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000

# Очищаем кэш pip и временные файлы
RUN pip cache purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/*

CMD ["/manasgramback/entrypoint.sh"]
