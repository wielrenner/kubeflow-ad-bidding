FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

CMD exec gunicorn --bind :8080 --workers 1 --threads 8 wsgi:app