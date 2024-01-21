FROM python:3.9-alpine

WORKDIR /app

COPY ../lab01/lab01_consumer/requirements.txt .

RUN pip install -r requirements.txt

ADD ../lab01/lab01_consumer/lab01_consumer.py /app

CMD ["python", "lab01_consumer.py"]