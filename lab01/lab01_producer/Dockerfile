FROM python:3.9-alpine

WORKDIR /app

ADD ../lab01/lab01_producer/lab01_producer.py /app

RUN pip install azure-eventhub

CMD ["python", "lab01_producer.py"]