FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN mkdir -p /app/celery-results

# Define environment variables for AWS

EXPOSE 5000

CMD ["bash", "-c", "celery -A worker worker --loglevel=info & python app.py"]
