FROM python:3.9-alpine

WORKDIR /app

ADD lab01_consumer/lab01_consumer.py /app

RUN pip install azure-eventhub

CMD ["python", "lab01_consumer.py"]