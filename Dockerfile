FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN mkdir -p /app/celery-results

EXPOSE 5000

CMD ["bash", "-c", "celery -A worker worker --loglevel=info --concurrency=1 & python app.py"]
