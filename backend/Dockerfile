FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV NEW_RELIC_CONFIG_FILE=/app/newrelic.ini

CMD ["newrelic-admin", "run-program", "python", "app.py"]
